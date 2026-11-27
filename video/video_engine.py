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
    # plan de ville (module 6)
    "road": (226, 222, 238), "grass": (211, 235, 219), "grass_ink": (36, 112, 74), "plan": (247, 245, 252),
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
    "fr": {"color": "brand", "bold": True},        # mot français dans un texte turc : violet et gras
    "frok": {"color": "ok", "bold": True},
    "frno": {"color": "no", "bold": True, "strike": True},
}
FONT_CANDIDATES = {
    "display": ["fonts/BricolageGrotesque-Bold.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "bold": ["fonts/PlusJakartaSans-Bold.ttf", "C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/segoeuib.ttf",
             "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "regular": ["fonts/PlusJakartaSans-Regular.ttf", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "symbols": ["fonts/DejaVuSans-Bold.ttf", "C:/Windows/Fonts/seguisym.ttf", "C:/Windows/Fonts/arialbd.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
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


def Img(id, path, x, y, w, h, radius=24, top=False):
    """top=True : dessinée par-dessus les tracés et les pastilles (portrait qui se déplace sur le plan)."""
    return dict(type="image", id=id, path=path, x=x, y=y, w=w, h=h, radius=radius, top=top)


def Arrow(id, frm, to, color="gold", width=7, curve=0, head=24):
    """frm / to : (x, y) ou {"id": "elem", "char": 4, "side": "top"} ou {"id": "elem", "side": "left"}."""
    return dict(type="arrow", id=id, frm=frm, to=to, color=color, width=width, curve=curve, head=head)


def Badge(id, text, x, y, size=30, fill="gold", color="ink", align="left", pad=(22, 10)):
    return dict(type="badge", id=id, text=text, x=x, y=y, size=size, fill=fill, color=color, align=align, pad=pad)


def Bubble(id, x, y, w, h, side="left", fill="card", outline="brand", dim=False):
    """Bulle de dialogue ; side = côté de la queue (vers le portrait). dim : réplique déjà dite, atténuée."""
    return dict(type="bubble", id=id, x=x, y=y, w=w, h=h, side=side, fill=fill, outline=outline, dim=dim)


def Route(id, pts, color="brand", width=8, dash=None, head=0):
    """Tracé (itinéraire) : liste de points (x, y). Dans un beat animé (anim=...), il se dessine progressivement.
    dash=(plein, vide) pour un pointillé ; head>0 : pointe de flèche à l'arrivée."""
    return dict(type="path", id=id, pts=[tuple(p) for p in pts], color=color, width=width, dash=dash, head=head)


def Dot(id, x, y, r=26, fill="gold", outline="white", width=6, label="", lcolor="ink"):
    """Pastille ronde (personnage sur le plan). Dans un beat animé, elle glisse de son ancienne position à la nouvelle."""
    return dict(type="dot", id=id, x=x, y=y, r=r, fill=fill, outline=outline, width=width, label=label, lcolor=lcolor)


def Countdown(id, x, y, w, label="", seconds=None, color="brand"):
    """seconds=None : le compte à rebours dure tout le beat."""
    return dict(type="countdown", id=id, x=x, y=y, w=w, label=label, seconds=seconds, color=color)


def TR(text):
    return {"tr": text}


def FR(text, voice="F1"):
    return {"fr": text, "voice": voice}


def beat(show=None, hide=None, say=None, clear=False, pause=0.45, lead=0.25, wait=0.0, repeat=None, bell=None, anim=None):
    """
    show   : élément ou liste d'éléments (ajout ou remplacement par id)
    hide   : id ou liste d'ids à retirer
    say    : utterance ou liste (TR("..."), FR("...", "M1"), {"file": "a1/audio/..."})
    clear  : retire tout avant d'afficher
    wait   : durée minimale du beat (utile sans audio, ou pour un compte à rebours)
    repeat : facteur ; le beat dure alors facteur × durée de l'audio du beat précédent (pause « Tekrar et »)
    anim   : durée (s) d'une transition animée : les éléments déjà à l'écran dont la position change glissent vers
             leur nouvelle place, et les tracés (Route) se dessinent, au lieu du simple fondu
    bell   : petit son de cloche au début du beat. Un entier 0, 1, 2... = note de plus en plus aiguë
             (crescendo pour une liste) ; "ok" = petit accord de fin de liste.
    """
    as_list = lambda v: [] if v is None else (v if isinstance(v, list) else [v])
    return dict(show=as_list(show), hide=as_list(hide), say=as_list(say), clear=clear,
                pause=pause, lead=lead, wait=wait, repeat=repeat, bell=bell, anim=anim)


def scene(title, beats, fit=True):
    """fit=False : pas de cadrage automatique pour cette scène (écrans composés à la main, comme le plan de ville)."""
    return dict(title=title, beats=beats, fit=fit)

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


_missing = {}


def glyph_missing(kind, ch):
    """Vrai si la police principale n'a pas ce caractère (il sera dessiné avec la police « symbols »).
    Test sans dépendance : le dessin du caractère est identique à celui d'un caractère inexistant."""
    if ord(ch) < 0x250 or ch in "«»…’‘“”–—·•":
        return False
    key = (kind, ch)
    if key not in _missing:
        f = font(kind, 40)
        ref = f.getmask("\U0010FFFD")
        m = f.getmask(ch)
        _missing[key] = (m.size == ref.size and bytes(m) == bytes(ref))
    return _missing[key]


class MixFont:
    """Police principale + police de secours pour les symboles qu'elle n'a pas (↗ ↘ ‿ ⁿ ɛ ə ♥ ✗...)."""
    def __init__(self, kind, size):
        self.kind, self.size = kind, size
        self.main = font(kind, size)
        self.fb = font("symbols", size) if kind != "symbols" else self.main

    def runs(self, text):
        out, cur, cur_fb = [], "", False
        for ch in text:
            fb = glyph_missing(self.kind, ch)
            if fb != cur_fb and cur:
                out.append((cur_fb, cur)); cur = ""
            cur_fb = fb
            cur += ch
        if cur:
            out.append((cur_fb, cur))
        return out

    def getlength(self, text):
        return sum((self.fb if fb else self.main).getlength(t) for fb, t in self.runs(text))

    def getmetrics(self):
        return self.main.getmetrics()

    def draw(self, d, xy, text, fill):
        x, y = xy
        base = y + self.main.getmetrics()[0]
        for fb, t in self.runs(text):
            f = self.fb if fb else self.main
            d.text((x, base), t, font=f, fill=fill, anchor="ls")
            x += f.getlength(t)


_mix = {}


def mfont(kind, size):
    key = (kind, size)
    if key not in _mix:
        _mix[key] = MixFont(kind, size)
    return _mix[key]


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
    fnt = mfont(el["font"], el["size"])
    plain, styles = parse_markup(el["text"])
    lines = el.get("_lines") or wrap_lines(plain, fnt, el.get("max_w"))   # _lines : coupures figées par le cadrage automatique
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
    st = {"color": base_color, "bg": None, "strike": False, "under": False, "bold": False}
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
            fnt.draw(d, (sx, y), seg, st["color"] + (255,))
            if st["bold"]:                                                 # gras simulé : second passage légèrement décalé
                fnt.draw(d, (sx + max(1.0, el["size"] * 0.028), y), seg, st["color"] + (255,))
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


def draw_bubble(img, e, dy=0, alpha=1.0):
    x0, y0, x1, y1 = e["x"], e["y"] + dy, e["x"] + e["w"], e["y"] + e["h"] + dy
    line = col("line" if e["dim"] else e["outline"]) + (255,)
    fill = col("card" if e["dim"] else e["fill"]) + (255,)
    r = min(36, e["h"] / 2)
    ty = y0 + min(62, e["h"] / 2)
    tail = [(x0 + 3, ty - 22), (x0 - 36, ty + 4), (x0 + 3, ty + 20)] if e["side"] == "left" else \
           [(x1 - 3, ty - 22), (x1 + 36, ty + 4), (x1 - 3, ty + 20)]
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if not e["dim"]:                                                      # ombre douce sous la réplique en cours
        d.rounded_rectangle((x0 + 6, y0 + 8, x1 + 6, y1 + 8), radius=r, fill=(91, 76, 196, 40))
    w = 3 if e["dim"] else 5
    d.rounded_rectangle((x0, y0, x1, y1), radius=r, fill=fill, outline=line, width=w)
    d.polygon(tail, fill=fill)
    d.line(tail, fill=line, width=w, joint="curve")
    if alpha < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(layer)


def draw_path(img, el, progress=1.0):
    """Polyligne dessinée jusqu'à la fraction « progress » de sa longueur (pointillé possible)."""
    pts = el["pts"]
    if progress <= 0 or len(pts) < 2:
        return
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    target = sum(segs) * min(1.0, progress)
    d = ImageDraw.Draw(img)
    c = col(el["color"]) + (255,)
    w = el["width"]

    def at(dist):
        for (a, b), L in zip(zip(pts, pts[1:]), segs):
            if dist <= L or (a, b) == (pts[-2], pts[-1]):
                t = min(1.0, dist / L) if L else 0
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            dist -= L

    if el["dash"]:
        on, off = el["dash"]
        pos = 0.0
        while pos < target:
            a, b = at(pos), at(min(target, pos + on))
            d.line([a, b], fill=c, width=w)
            pos += on + off
    else:
        line, run = [pts[0]], 0.0
        for (a, b), L in zip(zip(pts, pts[1:]), segs):
            if run + L <= target:
                line.append(b)
                run += L
            else:
                line.append(at(target))
                break
        d.line(line, fill=c, width=w, joint="curve")
        for p in line:                                                    # extrémités et angles arrondis
            d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=c)
    if el["head"] and progress >= 0.999:
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        ang, h = math.atan2(by - ay, bx - ax), el["head"]
        d.polygon([(bx + h * 0.5 * math.cos(ang), by + h * 0.5 * math.sin(ang)),
                   (bx - h * math.cos(ang - 0.5), by - h * math.sin(ang - 0.5)),
                   (bx - h * math.cos(ang + 0.5), by - h * math.sin(ang + 0.5))], fill=c)


def draw_dot(img, el, alpha=1.0):
    x, y, r = el["x"], el["y"], el["r"]
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((x - r - 2, y - r + 6, x + r + 2, y + r + 10), fill=(29, 26, 51, 46))                 # ombre portée
    d.ellipse((x - r, y - r, x + r, y + r), fill=col(el["fill"]) + (255,),
              outline=col(el["outline"]) + (255,) if el["outline"] else None, width=el["width"])
    if el["label"]:
        f = font("display", int(r * 1.05))
        d.text((x, y - r * 0.04), el["label"], font=f, fill=col(el.get("lcolor", "ink")) + (255,), anchor="mm")
    if alpha < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(layer)


def draw_badge(img, el, dy=0, alpha=1.0):
    fnt = mfont("bold", el["size"])
    tw = fnt.getlength(el["text"])
    px, py = el["pad"]
    w, h = tw + 2 * px, el["size"] * 1.2 + 2 * py
    x = el["x"] - (w / 2 if el["align"] == "center" else 0)
    y = el["y"] + dy
    layer = img if alpha >= 0.999 else Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x, y, x + w, y + h), radius=int(h / 2), fill=col(el["fill"]) + (255,))
    fnt.draw(d, (x + px, y + py), el["text"], col(el["color"]) + (255,))
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

    def render(self, state, chapter, enter=None, enter_p=1.0, cd_frac=0.0, cd_total=0.0, move=None, draw_p=1.0):
        """state : dict id->élément (ordre = ordre d'affichage). enter : ids qui apparaissent (animés par enter_p).
        move : (ancien état, progression 0..1) pour faire glisser les éléments déplacés ; draw_p : avancée des tracés qui entrent."""
        enter = enter or set()
        if move:
            old, mp = move
            mp = mp * mp * (3 - 2 * mp)                                   # départ et arrivée en douceur
            moved = {}
            for i, e in state.items():
                o = old.get(i)
                if o and o["type"] == e["type"] and "x" in e and (o["x"], o["y"]) != (e["x"], e["y"]):
                    moved[i] = dict(e, x=o["x"] + (e["x"] - o["x"]) * mp, y=o["y"] + (e["y"] - o["y"]) * mp)
            state = {i: moved.get(i, e) for i, e in state.items()}
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
            elif t == "image" and not e.get("top"):
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
            elif t == "path":
                draw_path(img, e, draw_p if new else 1.0)
            elif t == "bubble":
                draw_bubble(img, e, dy, a)
        for i, e in state.items():                                       # les pastilles passent au-dessus des tracés
            if e["type"] == "dot":
                draw_dot(img, e, ease if i in enter else 1.0)
        for i, e in state.items():
            if e["type"] == "image" and e.get("top"):
                im = load_image(e["path"], e["w"], e["h"], e["radius"])
                a = ease if i in enter else 1.0
                if a < 1:
                    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
                img.alpha_composite(im, (int(e["x"]), int(e["y"])))
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
        sent = tr_accents(text) if lang == "tr" else FR_PREFIX + text + FR_SUFFIX
        h = hashlib.sha1(json.dumps([code, VOICES[code].get("id") or VOICES[code]["name"], MODEL_ID, settings, sent, lang],
                                    ensure_ascii=False).encode()).hexdigest()[:16]
        out = CACHE / "tts" / f"{lang}-{code}-{h}.mp3"
        if out.exists():
            return out
        if self.draft:
            return None
        if not self.key:
            # vidéo finale : jamais de phrase remplacée par du silence sans le dire
            sys.exit("\nARRÊT : il manque la voix de cette phrase et la clé ElevenLabs n'est pas définie dans ce terminal.\n"
                     f"  Phrase : {text[:90]}\n"
                     "  Tape d'abord :  set ELEVENLABS_API_KEY=ta_cle   puis relance la commande.\n")
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
def tr_accents(text):
    """Narration turque : un passage français écrit entre « » est lu avec l'accent français.
    « mon père » devient « [French accent] mon père [Turkish accent] » (balises comprises par eleven_v4)."""
    return re.sub(r"«\s*(.+?)\s*»", r"[French accent] \1 [Turkish accent]", text)


def silence(sec):
    return b"\x00\x00" * int(round(sec * SR))


# Cloches discrètes : gamme pentatonique (do, ré, mi, sol, la, do), synthèse simple, volume bas sous la voix.
BELL_NOTES = [523.25, 587.33, 659.25, 783.99, 880.00, 1046.50, 1174.66, 1318.51]
BELL_GAIN = 0.22
_bell_cache = {}


def bell_samples(kind):
    """Renvoie une liste d'échantillons (float -1..1) pour un son de cloche."""
    if kind in _bell_cache:
        return _bell_cache[kind]
    if kind == "ok":
        freqs, gain = [BELL_NOTES[0] * 2, BELL_NOTES[2] * 2, BELL_NOTES[3] * 2], BELL_GAIN * 0.8
    else:
        k = max(0, min(int(kind), len(BELL_NOTES) - 1))
        freqs, gain = [BELL_NOTES[k]], BELL_GAIN * (0.75 + 0.06 * k)
    n = int(1.1 * SR)
    out = []
    for i in range(n):
        t = i / SR
        env = min(1.0, t / 0.004) * math.exp(-t * 4.5)
        v = 0.0
        for f in freqs:
            v += math.sin(2 * math.pi * f * t) + 0.35 * math.sin(2 * math.pi * f * 2.0 * t) * math.exp(-t * 6) \
                 + 0.12 * math.sin(2 * math.pi * f * 3.01 * t) * math.exp(-t * 9)
        out.append(gain * env * v / (len(freqs) * 1.47))
    _bell_cache[kind] = out
    return out


def mix_bells(audio, bells):
    """Ajoute les cloches (position en échantillons, type) au flux audio 16 bits."""
    import array
    pcm = array.array("h")
    pcm.frombytes(bytes(audio))
    for pos, kind in bells:
        for i, v in enumerate(bell_samples(kind)):
            j = pos + i
            if j >= len(pcm):
                break
            pcm[j] = max(-32768, min(32767, pcm[j] + int(v * 32767)))
    return bytearray(pcm.tobytes())


# =============================================================================
# CADRAGE AUTOMATIQUE (MODULE["autofit"] = True)
# =============================================================================
FIXED_IDS = ("title", "sub")          # le titre de l'écran reste à sa place, le reste est agrandi et centré
FIT_MAX = 1.45                        # agrandissement maximal
FIT_AREA = (80, 1840, 1015)           # gauche, droite, bas de la zone utile (le haut dépend du titre)


def _el_bbox(e):
    t = e["type"]
    if t == "text":
        return layout_text(e)["bbox"]
    if t in ("box", "image"):
        return (e["x"], e["y"], e["x"] + e["w"], e["y"] + e["h"])
    if t == "badge":
        w = mfont("bold", e["size"]).getlength(e["text"]) + 2 * e["pad"][0]
        h = e["size"] * 1.2 + 2 * e["pad"][1]
        x = e["x"] - (w / 2 if e["align"] == "center" else 0)
        return (x, e["y"], x + w, e["y"] + h)
    if t == "countdown":
        return (e["x"], e["y"], e["x"] + e["w"] + 90, e["y"] + (50 if e["label"] else 0) + 44)
    if t == "arrow":
        pts = [p for p in (e["frm"], e["to"]) if isinstance(p, (list, tuple))]
        if pts:
            return (min(p[0] for p in pts) - 20, min(p[1] for p in pts) - 20, max(p[0] for p in pts) + 20, max(p[1] for p in pts) + 20)
    return None


def _el_scale(e, s, ox, oy, tx, ty):
    """Copie de l'élément, agrandi d'un facteur s : le point (ox, oy) va en (tx, ty)."""
    e = dict(e)
    fx = lambda v: tx + (v - ox) * s
    fy = lambda v: ty + (v - oy) * s
    t = e["type"]
    if t == "arrow":
        for k in ("frm", "to"):
            if isinstance(e[k], (list, tuple)):
                e[k] = (fx(e[k][0]), fy(e[k][1]))
        e["width"] = max(2, round(e["width"] * s)); e["head"] = round(e["head"] * s); e["curve"] = e["curve"] * s
        return e
    e["x"], e["y"] = fx(e["x"]), fy(e["y"])
    if t == "text":
        old = e["size"]
        if e.get("max_w"):
            # mêmes retours à la ligne qu'avant l'agrandissement : largeur limite = ligne la plus large, mise à l'échelle
            lay = layout_text(dict(e, x=0, y=0))
            bb = lay["bbox"]
            e["size"] = max(8, round(old * s))
            e["max_w"] = (bb[2] - bb[0]) * e["size"] / old + 3
            # coupures de lignes figées : l'agrandissement ne peut plus faire passer une phrase sur deux lignes
            e["_lines"] = [(a, b) for a, b, _, _ in lay["lines"]]
        else:
            e["size"] = max(8, round(old * s))
    elif t in ("box", "image"):
        e["w"], e["h"] = round(e["w"] * s), round(e["h"] * s)
        e["radius"] = round(e["radius"] * s)
        if t == "image":
            e["x"], e["y"] = round(e["x"]), round(e["y"])
    elif t == "badge":
        e["size"] = max(8, round(e["size"] * s)); e["pad"] = (round(e["pad"][0] * s), round(e["pad"][1] * s))
    elif t == "countdown":
        e["w"] = round(e["w"] * s)
    return e


def autofit(scenes, card_img=None):
    """Agrandit et centre le contenu de chaque écran (un écran = les beats entre deux « clear »).
    Tant qu'un écran ne montre que son titre, le titre est affiché en grand au centre, avec l'illustration du module."""
    L, R, B = FIT_AREA
    for sc in scenes:
        if not sc.get("fit", True):
            continue
        screens, cur = [], []
        for i, b in enumerate(sc["beats"]):
            if (b["clear"] or i == 0) and cur:
                screens.append(cur); cur = []
            cur.append(b)
        if cur:
            screens.append(cur)
        for beats in screens:
            content = [e for b in beats for e in b["show"] if e["id"] not in FIXED_IDS]
            titled = any(e["id"] in FIXED_IDS for b in beats for e in b["show"])
            boxes = [bb for bb in (_el_bbox(e) for e in content) if bb]
            if boxes:
                x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
                x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
                # écran composé autour du milieu (un élément centré sur l'axe) : on garde cet axe au milieu,
                # sinon un petit badge à gauche suffit à décaler toute la composition vers la droite
                if any(e["type"] in ("text", "badge") and e.get("align") == "center" and abs(e["x"] - W / 2) < 2 for e in content):
                    half = max(W / 2 - x0, x1 - W / 2)
                    x0, x1 = W / 2 - half, W / 2 + half
                top = 290 if titled else 125
                aw, ah, bw, bh = R - L, B - top, max(1, x1 - x0), max(1, y1 - y0)
                s = min(aw / bw, ah / bh, FIT_MAX)
                if s < 1.04:
                    s = 1.0                                # pas la place d'agrandir : on centre seulement
                if bw * s <= aw + 1 and bh * s <= ah + 1:
                    tx = L + (aw - bw * s) / 2
                    ty = top + (ah - bh * s) * 0.42
                    for b in beats:
                        b["show"] = [e if e["id"] in FIXED_IDS else _el_scale(e, s, x0, y0, tx, ty) for e in b["show"]]
            # écran de titre : tant que seul le titre est visible
            if titled:
                seen, pending = {}, True
                for b in beats:
                    has_content = any(e["id"] not in FIXED_IDS for e in b["show"])
                    if pending and not has_content:
                        for e in b["show"]:
                            seen[e["id"]] = e
                        big = []
                        for e in b["show"]:
                            e2 = dict(e)
                            if e["id"] == "title":
                                e2.update(x=W / 2, y=520 if card_img else 400, size=round(e["size"] * 1.45), align="center", max_w=1600)
                            else:
                                e2.update(x=W / 2, y=(520 if card_img else 400) + 150, size=round(e["size"] * 1.25), align="center", max_w=1500)
                            big.append(e2)
                        if card_img:
                            big.insert(0, Img("_card", card_img, W // 2 - 240, 150, 480, 320, radius=32))
                        b["show"] = big
                    elif pending and has_content:
                        pending = False
                        if seen:
                            b["show"] = list(seen.values()) + b["show"]
                            b["hide"] = b["hide"] + ["_card"]


def build(module_file, draft=False, scenes_sel=None):
    spec = importlib.util.spec_from_file_location("module_script", module_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    MODULE, SCENES = mod.MODULE, mod.SCENES
    if MODULE.get("autofit"):
        autofit(SCENES, MODULE.get("card_img"))
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
    bells = []             # (position en échantillons, type de cloche)
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
            if b.get("bell") is not None:
                bells.append((len(audio) // 2 + int(TRANS * SR * 0.5), b["bell"]))
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
            if changed and b.get("anim") and prev_state and not b["clear"]:
                # transition animée : glissement des éléments déplacés, tracés dessinés ; seuls les vrais nouveaux éléments apparaissent en fondu
                ntr = max(2, int(round(min(b["anim"], dur - 0.1) * FPS)))
                fresh = {i for i in enter if i not in prev_state}
                for f in range(ntr):
                    p = (f + 1) / ntr
                    emit(rnd.render(state, sc["title"], fresh, min(1.0, p * ntr / max(1, TRANS * FPS)), 0.0, dur,
                                    move=(prev_state, p), draw_p=p), 1 / FPS)
            elif ntr:
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
    if bells:
        audio = mix_bells(audio, bells)
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
