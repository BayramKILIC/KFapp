#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moteur vidéo générique pour les modules « DELF A1 Hazırlık » de Kolay Fransızca.

Un scénario de module (ex. modul_01_video.py) décrit des scènes composées de « beats ».
Un beat = un état visuel (éléments affichés) + ce qu'on entend pendant ce temps.
Le moteur :
  1. récupère chaque audio (fichiers déjà générés pour le site, ou synthèse ElevenLabs avec cache) ;
  2. calcule la durée de chaque beat à partir des audios ;
  3. dessine les images (Pillow), avec transitions, flèches qui se tracent, lettres qui changent de couleur ;
  4. assemble la vidéo et le son avec ffmpeg, et écrit les chapitres YouTube.

Utilisation :
    python video_engine.py modul_01_video.py                 # rendu complet (clé ElevenLabs requise pour le turc)
    python video_engine.py modul_01_video.py --draft         # sans ElevenLabs : silence à la place des voix manquantes
    python video_engine.py modul_01_video.py --scenes 3      # une seule scène (aperçu rapide)
    python video_engine.py modul_01_video.py --scenes 2-4

Dépendances : pip install pillow requests openpyxl   + ffmpeg et ffprobe dans le PATH.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# =============================================================================
# CONFIGURATION (à adapter si besoin)
# =============================================================================
HERE = Path(__file__).resolve().parent
SITE_ROOT = Path(os.environ.get("KF_SITE_ROOT", str(Path.home() / "KFapp")))  # dépôt du site (audios, images, manifestes)
CACHE = HERE / "cache"
OUT = HERE / "out"

W, H, FPS = 1920, 1080, 30
TRANS = 0.35            # durée d'une transition (s)
SR = 44100              # fréquence audio de travail

VOICES = {
    "TR": {"id": "NNn9dv8zq2kUo7d3JSGG", "name": "Derya"},                 # voix turque : id prioritaire, sinon recherche par nom
    "F1": {"id": "QbsdzCokdlo98elkq4Pc", "name": "Koraly"},
    "M1": {"id": "69ujSsYIBOGW4duCBBSW", "name": "Bastien"},
    "F2": {"id": "ZtJvTSnGgAdhWKQBViA1", "name": "Alice"},
}
MODEL_ID = "eleven_v4"
TR_SETTINGS = {"stability": 0.50}
FR_SETTINGS = {"stability": 0.50}
FR_PREFIX, FR_SUFFIX, FR_SPEED = "[articulated] ", " [short pause]", 0.90   # identique aux audios du site

PALETTE = {
    "paper": (250, 249, 245), "card": (255, 255, 255), "ink": (29, 26, 51), "soft": (92, 88, 115),
    "line": (228, 225, 238), "brand": (91, 76, 196), "brand_dark": (63, 51, 150), "tint": (238, 235, 251),
    "gold": (233, 181, 59), "gold_tint": (251, 243, 221), "gold_ink": (122, 86, 7),
    "ok": (30, 138, 90), "ok_tint": (227, 244, 236), "no": (194, 65, 45), "no_tint": (251, 233, 229),
    "mute": (176, 171, 196), "white": (255, 255, 255), "night": (29, 26, 51),
}
# styles utilisables dans le texte : "Salu[t|mute]" ou "[Bonjour|hl] !"
BG_TOP = (252, 249, 242)      # crème chaud (haut gauche)
BG_BOTTOM = (238, 235, 251)   # lavande très claire (bas droite)

STYLES = {
    "hl": {"color": "brand"},
    "hl2": {"color": "brand", "under": True},
    "gold": {"color": "gold_ink", "bg": "gold_tint"},
    "mark": {"color": "brand_dark", "bg": "tint"},
    "ok": {"color": "ok"},
    "no": {"color": "no"},
    "mute": {"color": "mute", "strike": True},
    "soft": {"color": "soft"},
    "white": {"color": "white"},
}
FONT_CANDIDATES = {
    "display": ["fonts/BricolageGrotesque-Bold.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "bold": ["fonts/PlusJakartaSans-Bold.ttf", "C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/segoeuib.ttf",
             "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "regular": ["fonts/PlusJakartaSans-Regular.ttf", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
}

# =============================================================================
# CONSTRUCTEURS D'ÉLÉMENTS (utilisés par les scénarios de module)
# =============================================================================
def T(id, text, x, y, size=40, font="bold", color="ink", align="left", max_w=None, line_h=1.3, alpha=1.0):
    """Texte riche. Balisage : [segment|style] ; plusieurs styles : [seg|hl+gold]."""
    return dict(type="text", id=id, text=text, x=x, y=y, size=size, font=font, color=color,
                align=align, max_w=max_w, line_h=line_h, alpha=alpha)


def Box(id, x, y, w, h, fill="card", outline="line", radius=24, width=2, alpha=1.0):
    return dict(type="box", id=id, x=x, y=y, w=w, h=h, fill=fill, outline=outline, radius=radius, width=width, alpha=alpha)


def Img(id, path, x, y, w, h, radius=24):
    return dict(type="image", id=id, path=path, x=x, y=y, w=w, h=h, radius=radius)


def Arrow(id, frm, to, color="gold", width=7, curve=0, head=24):
    """frm / to : (x, y) ou {"id": "elem", "char": 4, "side": "top"} ou {"id": "elem", "side": "left"}."""
    return dict(type="arrow", id=id, frm=frm, to=to, color=color, width=width, curve=curve, head=head)


def Badge(id, text, x, y, size=30, fill="gold", color="ink", align="left", pad=(22, 10)):
    return dict(type="badge", id=id, text=text, x=x, y=y, size=size, fill=fill, color=color, align=align, pad=pad)


def Countdown(id, x, y, w, label="", seconds=None, color="brand"):
    """seconds=None : le compte à rebours dure tout le beat."""
    return dict(type="countdown", id=id, x=x, y=y, w=w, label=label, seconds=seconds, color=color)


def TR(text):
    return {"tr": text}


def FR(text, voice="F1"):
    return {"fr": text, "voice": voice}


def beat(show=None, hide=None, say=None, clear=False, pause=0.45, lead=0.25, wait=0.0, repeat=None):
    """
    show   : élément ou liste d'éléments (ajout ou remplacement par id)
    hide   : id ou liste d'ids à retirer
    say    : utterance ou liste (TR("..."), FR("...", "M1"), {"file": "a1/audio/..."})
    clear  : retire tout avant d'afficher
    wait   : durée minimale du beat (utile sans audio, ou pour un compte à rebours)
    repeat : facteur ; le beat dure alors facteur × durée de l'audio du beat précédent (pause « Tekrar et »)
    """
    as_list = lambda v: [] if v is None else (v if isinstance(v, list) else [v])
    return dict(show=as_list(show), hide=as_list(hide), say=as_list(say), clear=clear,
                pause=pause, lead=lead, wait=wait, repeat=repeat)


def scene(title, beats):
    return dict(title=title, beats=beats)

# =============================================================================
# POLICES ET TEXTE
# =============================================================================
_font_paths, _fonts = {}, {}


def font(kind, size):
    if kind not in _font_paths:
        for c in FONT_CANDIDATES[kind]:
            p = Path(c) if Path(c).is_absolute() else HERE / c
            if p.exists():
                _font_paths[kind] = str(p)
                break
        else:
            sys.exit(f"Aucune police trouvée pour « {kind} ». Ajoute un fichier .ttf dans FONT_CANDIDATES.")
    key = (kind, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(_font_paths[kind], size)
    return _fonts[key]


def col(c):
    return PALETTE[c] if isinstance(c, str) else tuple(c)


def parse_markup(text):
    """'Salu[t|mute] !' -> (texte brut, liste de styles par caractère)"""
    plain, styles = [], []
    for m in re.finditer(r"\[([^\[\]|]+)\|([a-z0-9+_]+)\]|([^\[]+|\[)", text):
        if m.group(1) is not None:
            for ch in m.group(1):
                plain.append(ch); styles.append(m.group(2))
        else:
            for ch in m.group(3):
                plain.append(ch); styles.append(None)
    return "".join(plain), styles


def wrap_lines(plain, fnt, max_w):
    if not max_w:
        max_w = 10 ** 9  # pas de limite de largeur, mais on respecte les retours à la ligne « \n »
    lines, start, last_space, i = [], 0, None, 0
    while i < len(plain):
        if plain[i] == "\n":
            lines.append((start, i)); start = i + 1; last_space = None
        elif plain[i] == " ":
            # espaces typographiques français : pas de coupure avant ? ! : ; » ni après «
            nxt = plain[i + 1] if i + 1 < len(plain) else ""
            prv = plain[i - 1] if i > 0 else ""
            if nxt not in "?!:;»" and prv != "«":
                last_space = i
        if fnt.getlength(plain[start:i + 1]) > max_w and last_space is not None and last_space > start:
            lines.append((start, last_space)); start = last_space + 1; last_space = None
        i += 1
    lines.append((start, len(plain)))
    return lines


def layout_text(el):
    fnt = font(el["font"], el["size"])
    plain, styles = parse_markup(el["text"])
    lines = wrap_lines(plain, fnt, el.get("max_w"))
    lh = el["size"] * el["line_h"]
    asc = fnt.getmetrics()[0]
    chars = [None] * len(plain)
    out_lines, maxw = [], 0
    for li, (a, b) in enumerate(lines):
        line = plain[a:b]
        lw = fnt.getlength(line)
        maxw = max(maxw, lw)
        x0 = el["x"] - (lw / 2 if el["align"] == "center" else lw if el["align"] == "right" else 0)
        y0 = el["y"] + li * lh
        for k in range(a, b):
            cx = x0 + fnt.getlength(plain[a:k])
            chars[k] = (cx, y0, cx + fnt.getlength(plain[k]), y0 + el["size"] * 1.05)
        out_lines.append((a, b, x0, y0))
    total_h = len(lines) * lh
    bx0 = el["x"] - (maxw / 2 if el["align"] == "center" else maxw if el["align"] == "right" else 0)
    return dict(plain=plain, styles=styles, lines=out_lines, chars=chars, font=fnt, asc=asc,
                bbox=(bx0, el["y"], bx0 + maxw, el["y"] + total_h))


def style_of(name, base_color):
    st = {"color": base_color, "bg": None, "strike": False, "under": False}
    if name:
        for part in name.split("+"):
            s = STYLES.get(part, {})
            for k, v in s.items():
                st[k] = col(v) if k in ("color", "bg") else v
    return st

# =============================================================================
# DESSIN
# =============================================================================
def draw_text(img, el, lay, dy=0, alpha=1.0):
    a_ = alpha * el.get("alpha", 1.0)
    layer = img if a_ >= 0.999 else Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    base = col(el["color"])
    fnt = lay["font"]
    for a, b, x0, y0 in lay["lines"]:
        k = a
        while k < b:
            sname = lay["styles"][k]
            j = k
            while j < b and lay["styles"][j] == sname:
                j += 1
            seg = lay["plain"][k:j]
            st = style_of(sname, base)
            sx = x0 + fnt.getlength(lay["plain"][a:k])
            sw = fnt.getlength(seg)
            y = y0 + dy
            if st["bg"] is not None and seg.strip():
                pad = el["size"] * 0.14
                d.rounded_rectangle((sx - pad, y - pad * 0.4, sx + sw + pad, y + el["size"] * 1.18), radius=int(pad * 1.6), fill=st["bg"] + (255,))
            d.text((sx, y), seg, font=fnt, fill=st["color"] + (255,))
            if st["strike"] and seg.strip():
                ly = y + el["size"] * 0.62
                d.line((sx - 2, ly, sx + sw + 2, ly), fill=st["color"] + (255,), width=max(3, el["size"] // 12))
            if st["under"] and seg.strip():
                ly = y + el["size"] * 1.12
                d.line((sx, ly, sx + sw, ly), fill=st["color"] + (255,), width=max(3, el["size"] // 14))
            k = j
    if layer is not img:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a_)))
        img.alpha_composite(layer)


_img_cache = {}


def load_image(path, w, h, radius):
    key = (path, w, h, radius)
    if key in _img_cache:
        return _img_cache[key]
    p = SITE_ROOT / path.lstrip("/")
    if p.exists():
        im = Image.open(p).convert("RGBA")
        r = max(w / im.width, h / im.height)
        im = im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)
        l, t = (im.width - w) // 2, (im.height - h) // 2
        im = im.crop((l, t, l + w, t + h))
    else:
        im = Image.new("RGBA", (w, h), PALETTE["tint"] + (255,))
        d = ImageDraw.Draw(im)
        d.text((w / 2, h / 2), "Görsel yok\n" + path, font=font("regular", 26), fill=PALETTE["soft"], anchor="mm", align="center")
    if radius:
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
        im.putalpha(Image.composite(im.getchannel("A"), mask, mask))
    _img_cache[key] = im
    return im


def resolve_point(ref, lays, els):
    if isinstance(ref, (list, tuple)):
        return float(ref[0]), float(ref[1])
    lay = lays.get(ref["id"])
    side = ref.get("side", "top")
    if lay and "char" in ref:
        idx = ref["char"]
        c = lay["chars"][idx if idx >= 0 else len(lay["chars"]) + idx]
        cx = (c[0] + c[2]) / 2
        return (cx, c[1] - 8) if side == "top" else (cx, c[3] + 10)
    if lay:
        x0, y0, x1, y1 = lay["bbox"]
    else:
        e = els[ref["id"]]
        x0, y0, x1, y1 = e["x"], e["y"], e["x"] + e.get("w", 0), e["y"] + e.get("h", 0)
    return {"top": ((x0 + x1) / 2, y0 - 8), "bottom": ((x0 + x1) / 2, y1 + 8),
            "left": (x0 - 12, (y0 + y1) / 2), "right": (x1 + 12, (y0 + y1) / 2)}[side]


def draw_arrow(img, el, lays, els, progress=1.0):
    if progress <= 0:
        return
    p0, p2 = resolve_point(el["frm"], lays, els), resolve_point(el["to"], lays, els)
    mx, my = (p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2
    dx, dy = p2[0] - p0[0], p2[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    p1 = (mx - dy / L * el["curve"], my + dx / L * el["curve"])
    n = 40
    pts = []
    for i in range(int(n * progress) + 1):
        t = i / n
        pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    d = ImageDraw.Draw(img)
    c = col(el["color"]) + (255,)
    if len(pts) > 1:
        d.line(pts, fill=c, width=el["width"], joint="curve")
    if progress > 0.9 and len(pts) > 1:
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        ang = math.atan2(by - ay, bx - ax)
        h = el["head"]
        d.polygon([(bx, by), (bx - h * math.cos(ang - 0.45), by - h * math.sin(ang - 0.45)),
                   (bx - h * math.cos(ang + 0.45), by - h * math.sin(ang + 0.45))], fill=c)


def draw_badge(img, el, dy=0, alpha=1.0):
    fnt = font("bold", el["size"])
    tw = fnt.getlength(el["text"])
    px, py = el["pad"]
    w, h = tw + 2 * px, el["size"] * 1.2 + 2 * py
    x = el["x"] - (w / 2 if el["align"] == "center" else 0)
    y = el["y"] + dy
    layer = img if alpha >= 0.999 else Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x, y, x + w, y + h), radius=int(h / 2), fill=col(el["fill"]) + (255,))
    d.text((x + px, y + py), el["text"], font=fnt, fill=col(el["color"]) + (255,))
    if layer is not img:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
        img.alpha_composite(layer)


def draw_countdown(img, el, frac, total):
    d = ImageDraw.Draw(img)
    x, y, w = el["x"], el["y"], el["w"]
    if el["label"]:
        d.text((x, y), el["label"], font=font("bold", 32), fill=col(el["color"]))
        y += 50
    d.rounded_rectangle((x, y, x + w, y + 18), radius=9, fill=PALETTE["tint"])
    rem = max(0.0, 1 - frac)
    if rem > 0:
        d.rounded_rectangle((x, y, x + max(18, w * rem), y + 18), radius=9, fill=col(el["color"]))
    secs = math.ceil((el["seconds"] or total) * rem - 1e-6)
    d.text((x + w + 24, y - 14), str(max(0, secs)), font=font("display", 40), fill=col(el["color"]))


def make_background():
    """Fond de la vidéo : dégradé crème -> lavande, halos flous violet et or, trame de points discrète."""
    from PIL import ImageFilter
    sw, sh = 64, 36                                          # petit dégradé agrandi ensuite (lisse)
    small = Image.new("RGB", (sw, sh))
    for y in range(sh):
        for x in range(sw):
            t = 0.65 * y / (sh - 1) + 0.35 * x / (sw - 1)    # dégradé en diagonale douce
            small.putpixel((x, y), tuple(int(BG_TOP[c] * (1 - t) + BG_BOTTOM[c] * t) for c in range(3)))
    img = small.resize((W, H), Image.BICUBIC).convert("RGBA")
    # chaque halo sur un calque de sa propre couleur (transparent) : pas de voile gris après le flou
    for color, a, box in ((PALETTE["brand"], 60, (W - 620, -380, W + 380, 520)),     # violet en haut à droite
                          (PALETTE["gold"], 70, (-420, H - 430, 520, H + 420))):     # or en bas à gauche
        halo = Image.new("RGBA", (W, H), color + (0,))
        ImageDraw.Draw(halo).ellipse(box, fill=color + (a,))
        img = Image.alpha_composite(img, halo.filter(ImageFilter.GaussianBlur(140)))
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(dots)
    for y in range(120, H - 40, 36):
        for x in range(24, W, 36):
            d.ellipse((x - 1.6, y - 1.6, x + 1.6, y + 1.6), fill=PALETTE["brand"] + (16,))
    img = Image.alpha_composite(img, dots).convert("RGB")
    # grain très léger : évite les « blocs » de compression vidéo sur les dégradés doux
    from PIL import ImageChops
    grain = Image.effect_noise((W, H), 3).convert("RGB")
    img = ImageChops.add(img, grain, scale=1.0, offset=-128)
    return img.convert("RGBA")


class Renderer:
    def __init__(self, module):
        self.module = module
        self.bg = make_background()

    def chrome(self, img, chapter):
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, W, 84), fill=PALETTE["brand"])
        d.text((48, 22), "Kolay", font=font("display", 36), fill=PALETTE["white"])
        d.text((48 + font("display", 36).getlength("Kolay "), 22), "Fransızca", font=font("display", 36), fill=PALETTE["gold"])
        right = f"{self.module['label']}  ·  {chapter}"
        f = font("bold", 28)
        d.text((W - 48 - f.getlength(right), 28), right, font=f, fill=PALETTE["white"])
        f2 = font("bold", 24)
        d.text((W - 48 - f2.getlength(self.module["url"]), H - 52), self.module["url"], font=f2, fill=PALETTE["soft"])

    def render(self, state, chapter, enter=None, enter_p=1.0, cd_frac=0.0, cd_total=0.0):
        """state : dict id->élément (ordre = ordre d'affichage). enter : ids qui apparaissent (animés par enter_p)."""
        enter = enter or set()
        img = self.bg.copy()
        lays = {i: layout_text(e) for i, e in state.items() if e["type"] == "text"}
        ease = 1 - (1 - enter_p) ** 3
        for i, e in state.items():
            new = i in enter
            dy = (1 - ease) * 24 if new else 0
            a = ease if new else 1.0
            t = e["type"]
            if t == "box":
                full = a >= 0.999 and e["alpha"] >= 0.999
                layer = img if full else Image.new("RGBA", img.size, (0, 0, 0, 0))
                ImageDraw.Draw(layer).rounded_rectangle(
                    (e["x"], e["y"] + dy, e["x"] + e["w"], e["y"] + e["h"] + dy), radius=e["radius"],
                    fill=col(e["fill"]) + (int(255 * a * e["alpha"]),),
                    outline=(col(e["outline"]) + (int(255 * a),)) if e["outline"] else None, width=e["width"])
                if not full:
                    img.alpha_composite(layer)
            elif t == "image":
                im = load_image(e["path"], e["w"], e["h"], e["radius"])
                if a < 1:
                    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
                img.alpha_composite(im, (int(e["x"]), int(e["y"] + dy)))
            elif t == "text":
                draw_text(img, e, lays[i], dy, a)
            elif t == "badge":
                draw_badge(img, e, dy, a)
            elif t == "countdown":
                draw_countdown(img, e, cd_frac, cd_total)
        for i, e in state.items():
            if e["type"] == "arrow":
                draw_arrow(img, e, lays, state, ease if i in enter else 1.0)
        self.chrome(img, chapter)
        return img.convert("RGB")

# =============================================================================
# AUDIO
# =============================================================================
def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Commande échouée : {' '.join(map(str, cmd))}\n{r.stderr[-800:]}")
    return r


def norm_text(t):
    return re.sub(r"\s+", " ", str(t).replace("’", "'").strip())


class AudioBank:
    def __init__(self, draft):
        self.draft = draft
        self.key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        self.manifest = {}
        self._load_manifests()
        (CACHE / "tts").mkdir(parents=True, exist_ok=True)
        (CACHE / "wav").mkdir(parents=True, exist_ok=True)
        self.missing = []

    def _load_manifests(self):
        try:
            from openpyxl import load_workbook
        except ImportError:
            print("openpyxl absent : les audios du site ne seront pas réutilisés.")
            return
        for m in sorted(SITE_ROOT.glob("audio_m*.xlsx")):
            ws = load_workbook(m, read_only=True)["Audio"]
            rows = list(ws.iter_rows(values_only=True))
            head = [str(h) for h in rows[0]]
            iv, it, ip = head.index("Voix"), head.index("Texte"), head.index("Chemin")
            for r in rows[1:]:
                if r and r[it]:
                    t = norm_text(r[it])
                    self.manifest.setdefault((t, r[iv]), r[ip])
                    self.manifest.setdefault((t, None), r[ip])
        print(f"{len(self.manifest)//2} audios du site indexés.")

    def voice_id(self, code):
        v = VOICES[code]
        if v.get("id"):
            return v["id"]
        import requests
        r = requests.get("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": self.key}, timeout=60)
        r.raise_for_status()
        for item in r.json().get("voices", []):
            if v["name"].lower() in item.get("name", "").lower():
                v["id"] = item["voice_id"]
                print(f"Voix « {v['name']} » trouvée : {v['id']}")
                return v["id"]
        sys.exit(f"Voix « {v['name']} » introuvable dans ton compte ElevenLabs. Indique son id dans VOICES['{code}'].")

    def tts(self, text, code, lang):
        settings = TR_SETTINGS if lang == "tr" else FR_SETTINGS
        sent = text if lang == "tr" else FR_PREFIX + text + FR_SUFFIX
        h = hashlib.sha1(json.dumps([code, VOICES[code].get("id") or VOICES[code]["name"], MODEL_ID, settings, sent, lang],
                                    ensure_ascii=False).encode()).hexdigest()[:16]
        out = CACHE / "tts" / f"{lang}-{code}-{h}.mp3"
        if out.exists():
            return out
        if self.draft or not self.key:
            return None
        import requests
        vid = self.voice_id(code)
        for attempt in range(3):
            r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}", params={"output_format": "mp3_44100_128"},
                              headers={"xi-api-key": self.key, "Content-Type": "application/json"},
                              json={"text": sent, "model_id": MODEL_ID, "voice_settings": settings}, timeout=120)
            if r.status_code == 200:
                raw = out.with_suffix(".raw.mp3")
                raw.write_bytes(r.content)
                if lang == "fr" and FR_SPEED != 1:
                    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-filter:a", f"atempo={FR_SPEED}", str(out)])
                    raw.unlink()
                else:
                    raw.rename(out)
                print(f"  synthèse {lang.upper()} : {text[:60]}")
                return out
            if r.status_code not in (429, 500, 502, 503):
                break
        raise RuntimeError(f"ElevenLabs a refusé la synthèse ({r.status_code}) : {r.text[:300]}")

    def source(self, utt):
        if "file" in utt:
            p = SITE_ROOT / utt["file"].lstrip("/")
            return p if p.exists() else None, utt["file"]
        if "fr" in utt:
            t = norm_text(utt["fr"])
            path = self.manifest.get((t, utt.get("voice"))) or self.manifest.get((t, None))
            if path and (SITE_ROOT / path).exists():
                return SITE_ROOT / path, utt["fr"]
            return self.tts(utt["fr"], utt.get("voice", "F1"), "fr"), utt["fr"]
        return self.tts(utt["tr"], "TR", "tr"), utt["tr"]

    def samples(self, utt):
        """Renvoie les échantillons PCM 16 bits mono (bytes) de l'utterance."""
        src, label = self.source(utt)
        if src is None:
            self.missing.append(label)
            est = 0.35 + 0.068 * len(label)                    # estimation pour le mode brouillon
            return b"\x00\x00" * int(est * SR)
        wav = CACHE / "wav" / (hashlib.sha1(str(src).encode()).hexdigest()[:16] + ".wav")
        if not wav.exists() or wav.stat().st_mtime < Path(src).stat().st_mtime:
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", str(wav)])
        with wave.open(str(wav)) as w:
            return w.readframes(w.getnframes())

# =============================================================================
# CONSTRUCTION
# =============================================================================
def silence(sec):
    return b"\x00\x00" * int(round(sec * SR))


def build(module_file, draft=False, scenes_sel=None):
    spec = importlib.util.spec_from_file_location("module_script", module_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    MODULE, SCENES = mod.MODULE, mod.SCENES
    if scenes_sel:
        SCENES = [SCENES[i] for i in scenes_sel]
    name = MODULE["slug"] + ("-brouillon" if draft else "") + (f"-scenes-{scenes_sel[0]+1}-{scenes_sel[-1]+1}" if scenes_sel else "")
    work = CACHE / "frames" / name
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    OUT.mkdir(exist_ok=True)

    bank = AudioBank(draft)
    rnd = Renderer(MODULE)
    audio = bytearray()
    frames = []            # (chemin image, durée)
    chapters = []
    t = 0.0
    fcount = 0
    prev_audio = 0.0

    def emit(img, dur):
        nonlocal fcount
        p = work / f"f{fcount:06d}.png"
        img.save(p, compress_level=1)
        fcount += 1
        frames.append((p, dur))

    total_beats = sum(len(s["beats"]) for s in SCENES)
    done = 0
    for sc in SCENES:
        chapters.append((t, sc["title"]))
        state = {}
        first = True
        for b in sc["beats"]:
            done += 1
            prev_state = dict(state)
            if b["clear"] or first:
                state = {}
            for i in b["hide"]:
                state.pop(i, None)
            enter = set()
            for e in b["show"]:
                if e["id"] not in state or state[e["id"]] != e:
                    enter.add(e["id"])
                state[e["id"]] = e
            first = False

            # --- son du beat
            clip = bytearray(silence(b["lead"] if b["say"] else 0))
            spoken = 0.0
            for k, u in enumerate(b["say"]):
                s = bank.samples(u)
                clip += s
                spoken += len(s) / 2 / SR
                if k < len(b["say"]) - 1:
                    clip += silence(0.3)
            dur = len(clip) / 2 / SR + (b["pause"] if b["say"] else 0)
            if b["repeat"]:
                dur = max(dur, b["repeat"] * prev_audio + 0.6)
            dur = max(dur, b["wait"], TRANS + 0.1)
            clip += silence(dur - len(clip) / 2 / SR)
            audio += clip
            if spoken:
                prev_audio = spoken

            # --- images du beat
            changed = state != prev_state
            ntr = int(round(TRANS * FPS)) if changed else 0
            if ntr:
                old = rnd.render(prev_state, sc["title"]) if prev_state else None
                for f in range(ntr):
                    p = (f + 1) / ntr
                    new = rnd.render(state, sc["title"], enter, p, 0.0, dur)
                    emit(Image.blend(old, new, p) if old is not None else new, 1 / FPS)
            rest = dur - ntr / FPS
            cds = [e for e in state.values() if e["type"] == "countdown"]
            if cds:
                step = 0.1
                n = max(1, int(rest / step))
                for k in range(n):
                    emit(rnd.render(state, sc["title"], cd_frac=(k * step + ntr / FPS) / dur, cd_total=dur), rest / n)
            else:
                emit(rnd.render(state, sc["title"]), rest)
            t += dur
            print(f"\r[{done}/{total_beats}] {sc['title'][:30]:<30} {t/60:5.1f} min", end="", flush=True)
    print()

    # --- écriture
    wav_path = work / "audio.wav"
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(bytes(audio))
    lst = work / "frames.txt"
    with open(lst, "w", encoding="utf-8") as f:
        for p, d in frames:
            f.write(f"file '{p.as_posix()}'\nduration {d:.6f}\n")
        f.write(f"file '{frames[-1][0].as_posix()}'\n")
    out = OUT / f"{name}.mp4"
    print("Encodage de la vidéo...")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(wav_path),
        "-fps_mode", "cfr", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)])
    chap = OUT / f"{name}-chapitres.txt"
    with open(chap, "w", encoding="utf-8") as f:
        for ts, title in chapters:
            f.write(f"{int(ts // 60)}:{int(ts % 60):02d} {title}\n")
    print(f"Vidéo : {out}  ({t/60:.1f} min)")
    print(f"Chapitres YouTube : {chap}")
    if bank.missing:
        print(f"{len(bank.missing)} voix absentes remplacées par du silence (mode brouillon ou clé manquante).")
    return out


def parse_sel(s, n):
    if not s:
        return None
    a, _, b = s.partition("-")
    a = int(a); b = int(b) if b else a
    return list(range(a - 1, min(b, n)))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("module")
    ap.add_argument("--draft", action="store_true", help="aucun appel ElevenLabs, silence à la place des voix manquantes")
    ap.add_argument("--scenes", default="", help="ex. 3 ou 2-4")
    ap.add_argument("--site", default="", help="chemin du dépôt du site (par défaut ~/KFapp)")
    a = ap.parse_args()
    if a.site:
        SITE_ROOT = Path(a.site)
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg introuvable dans le PATH.")
    spec = importlib.util.spec_from_file_location("m", a.module)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    build(a.module, a.draft, parse_sel(a.scenes, len(m.SCENES)))
