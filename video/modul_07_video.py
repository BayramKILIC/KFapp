# -*- coding: utf-8 -*-
"""
Scénario de la vidéo du module 7 : « Alışveriş » (Faire des achats).
Lancement :  py video_engine.py modul_07_video.py            (voix)
             py video_engine.py modul_07_video.py --draft    (sans voix, pour contrôler les écrans)

Même structure générale que le module 5, avec les choix du 27/11 :
  - accroche : deux questions, puis « Bu derste bu soruların cevabını beraber göreceğiz. », rappel du site, programme ;
  - le dialogue n'est écouté qu'une fois, ligne par ligne, avec le texte et la traduction ;
  - minuteur des questions : il affiche 5, 4, 3, 2, 1 mais ne dure que 3 secondes ;
  - terminaisons, accords et mots clés en couleur ;
  - quelques termes techniques français dits par Derya, une fois chacun (verbe, terminaison, déterminant, masculin,
    féminin, pluriel, pronom, adjectif, pronom personnel, liaison). Dans sa narration, un passage entre « » est lu
    avec l'accent français.
Règle Derya : jamais de petit mot français isolé (ce, ça, de...). Elle explique en turc ; le français est dit par les voix
françaises (fichiers du site a1/audio/m07/... ou FR("...") synthétisé).
"""
import os
import re
from video_engine import (layout_text, SITE_ROOT, T, Box, Img, Arrow, Badge, Bubble, Route, Dot, Countdown,
                          TR, FR, beat, scene)

MODULE = {"slug": "modul-7-alisveris", "label": "Modül 7", "url": "kolayfransizca.app"}
A = "a1/audio/m07/"
IMG = "a1/img/m07/"
CX = 960
WAIT = 3                                           # durée réelle du minuteur (il affiche 5 → 1)


def F(path):
    return {"file": A + path}


def G(n):
    return F(f"gram/m7-g{n:02d}.mp3")


def V(n, ex=False):
    return F(f"voc/m7-v{n:02d}{'-ex' if ex else ''}.mp3")


def D(n):
    return F(f"dialogue/m7-d{n:02d}.mp3")


def TT(n):
    return F(f"telaffuz/m7-t{n:02d}.mp3")


def fr(text):
    """Dans un texte turc, met le français entre « » en violet et en gras."""
    return re.sub(r"«\s*([^»]+?)\s*»", r"[« \1 »|fr]", text)


# =============================================================================
# Gabarits
# =============================================================================
CHAPTERS = ["Diyalog", "Fiyat sormak", "Je voudrais", "ce · cette · ces", "ça", "Renk ve beden", "Ödeme", "Kelimeler", "Telaffuz", "DELF ve test"]


def chapter(n, sub=None):
    """Carte de chapitre : où on en est dans la leçon (barre à segments), numéro et titre en grand."""
    els, w, gap = [], 152, 14
    x0 = CX - (len(CHAPTERS) * w + (len(CHAPTERS) - 1) * gap) / 2
    for k in range(len(CHAPTERS)):
        els.append(Box(f"cs{k}", x0 + k * (w + gap), 250, w, 16, fill="brand" if k + 1 == n else ("mute" if k + 1 < n else "line"), outline=None, radius=8))
    els += [Badge("cn", f"Bölüm {n} / {len(CHAPTERS)}", CX, 330, size=34, fill="tint", color="brand_dark", align="center"),
            T("ct", CHAPTERS[n - 1], CX, 430, size=110, font="display", align="center")]
    if sub:
        els.append(T("cu", sub, CX, 600, size=46, font="regular", color="soft", align="center", max_w=1500))
    return els


def title(text, sub=None):
    els = [T("title", text, 120, 125, size=66, font="display")]
    if sub:
        els.append(T("sub", sub, 120, 222, size=38, font="regular", color="soft", max_w=1680))
    return els


def note(text, kind="tavsiye", pid="note"):
    """Note du prof, seule à l'écran : grand cadre aéré, pastille, une idée par ligne, français en violet gras."""
    lab = "Öğretmenin tavsiyesi" if kind == "tavsiye" else "Öğretmenin notu"
    tint, line, ink = ("gold_tint", "gold", "gold_ink") if kind == "tavsiye" else ("tint", "brand", "brand_dark")
    txt = T(pid + "_txt", fr(text), 250, 0, size=48, font="regular", max_w=1420, line_h=1.6)
    th = layout_text(txt)["bbox"][3]
    h = 150 + th + 50
    y = 110 + (930 - h) / 2
    txt["y"] = y + 150
    return [Box(pid + "_box", 160, y, 1600, h, fill=tint, outline=line, radius=32, width=4),
            Box(pid + "_bar", 160, y + 40, 14, h - 80, fill=line, outline=None, radius=7),
            Dot(pid + "_ic", 270, y + 82, r=36, fill=line, outline="white", width=5, label="!", lcolor="white" if kind != "tavsiye" else "ink"),
            T(pid + "_lab", lab, 330, y + 52, size=44, font="display", color=ink), txt]


def hata(wrong, right, y=830, pid="ht"):
    """Carte « Sık yapılan hata » : la faute barrée en rouge, une flèche, la forme correcte en vert."""
    w = T(pid + "w", f"[{wrong}|frno]", 470, y + 34, size=46)
    wx = layout_text(w)["bbox"][2]
    return [Box(pid + "b", 120, y, 1680, 130, fill="card", outline="no", radius=24, width=3),
            Badge(pid + "l", "Sık yapılan hata", 150, y + 36, size=30, fill="no_tint", color="no"), w,
            T(pid + "a", "→", wx + 36, y + 28, size=52, color="soft"),
            T(pid + "r", f"[{right}|frok]", wx + 130, y + 34, size=46)]


def rule(text, y, pid="rule"):
    """Règle en une ligne, dans un bandeau."""
    return [Box(pid + "b", 120, y, 1680, 104, fill="tint", outline=None, radius=22),
            T(pid, fr(text), CX, y + 24, size=44, align="center", max_w=1620)]


def ex_line(eid, french, tr, x, y, size=54, trsize=36, max_w=1500):
    f = T(eid, french, x, y, size=size, max_w=max_w)
    fh = layout_text(f)["bbox"][3] - y
    return [f, T(eid + "t", tr, x, y + max(size + 18, fh + 4), size=trsize, font="regular", color="soft", max_w=max_w)]


def opt_text(oid, text, cx, y, max_w, color):
    """Texte d'une réponse, centré dans sa case ; réduit s'il ne tient pas sur une ligne."""
    for size in (46, 40, 34):
        el = T(oid, text, cx, y + 80 - size * 0.62, size=size, color=color, align="center", max_w=max_w)
        if len(layout_text(el)["lines"]) == 1:
            return el
    return T(oid, text, cx, y + 34, size=36, color=color, align="center", max_w=max_w, line_h=1.2)


def qcm(n, total, question, opts, ok, expl, says, wait=WAIT, label="Soru", qsize=60):
    """Question à choix : question, compte à rebours affiché de 5 à 1 mais qui dure 3 secondes, bonne réponse en vert."""
    w = 1640 // len(opts)
    show = [Badge("qn", f"{label} {n} / {total}" if total else label, CX, 150, size=34, fill="gold", color="ink", align="center"),
            T("qq", question, CX, 270, size=qsize, align="center", max_w=1640, line_h=1.25)]
    for k, o in enumerate(opts):
        x = 140 + k * w
        show += [Box(f"ob{k}", x, 520, w - 40, 160, fill="card", radius=26, width=3), opt_text(f"ot{k}", o, x + (w - 40) / 2, 520, w - 90, "ink")]
    x = 140 + ok * w
    return [beat(clear=True, show=show, say=says, pause=0.15),
            beat(show=Countdown("cd", 560, 780, 800, seconds=5), wait=wait),
            beat(hide=["cd"], show=[Box(f"ob{ok}", x, 520, w - 40, 160, fill="ok_tint", outline="ok", radius=26, width=6),
                                    opt_text(f"ot{ok}", opts[ok], x + (w - 40) / 2, 520, w - 90, "ok"),
                                    T("ex", fr(expl[0]), CX, 770, size=46, font="regular", color="soft", align="center", max_w=1640)],
                 say=TR(expl[1]), pause=0.5)]



def term(french, turkish, y=962):
    """Terme technique français, glissé en bas de l'écran : une fois par notion."""
    t = T("termt", f"Fransızca terim:   [{french}|gold]  =  {turkish}", CX, y + 17, size=36, color="white", align="center")
    x0, _, x1, _ = layout_text(t)["bbox"]
    w = (x1 - x0) + 110
    return [Box("termb", CX - w / 2, y, w, 82, fill="night", outline=None, radius=41), t]


# ----------------------------------------------------------------------------- la vitrine : huit vêtements avec leur prix
# clé : (mot, sens, prix, n° du vocabulaire)
SHOP = {"pantalon": ("le pantalon", "pantolon", 40, 15), "chemise": ("la chemise", "gömlek", 30, 16), "pull": ("le pull", "kazak", 45, 17),
        "robe": ("la robe", "elbise", 60, 18), "jupe": ("la jupe", "etek", 35, 19), "veste": ("la veste", "ceket", 59, 20),
        "manteau": ("le manteau", "palto", 90, 21), "chaussures": ("les chaussures", "ayakkabı", 55, 23)}
SX, SY, SW, SH = 60, 150, 272, 388                 # origine et taille d'une case


def shop(on=(), prices=True, names=True):
    """La vitrine, à gauche de l'écran. on : articles mis en valeur (jaune)."""
    els = []
    for i, (k, (w, tr, p, n)) in enumerate(SHOP.items()):
        x, y = SX + (i % 4) * (SW + 10), SY + (i // 4) * (SH + 12)
        o = k in on
        els += [Box("sb_" + k, x, y, SW, SH, fill="gold_tint" if o else "card", outline="gold" if o else "line", radius=24, width=6 if o else 2),
                Img("si_" + k, IMG + f"items/{k}.webp", x + 31, y + 62, 210, 210, radius=0)]
        if names:
            els.append(T("sn_" + k, w, x + SW / 2, y + 300, size=30, align="center", color="gold_ink" if o else "brand_dark"))
        if prices:
            els.append(Badge("sp_" + k, f"{p} €", x + SW / 2, y + 18, size=28, fill="gold" if o else "brand", color="ink" if o else "white", align="center", pad=(18, 5)))
    return els


PXR = 1230                                         # colonne de droite, à côté de la vitrine


def panel(word, tr, french=None, frtr=None, badge=None, wsize=100):
    """Colonne de droite : le mot en grand, son sens, puis la phrase d'exemple dans une carte."""
    w = T("word", word, PXR, 250, size=wsize, font="display", color="brand", max_w=640, line_h=1.05)
    wy = layout_text(w)["bbox"][3] + 14
    els = [w, T("wtr", tr, PXR, wy, size=50, font="regular", color="soft", max_w=640)]
    if badge:
        els.append(Badge("num", badge, PXR, 150, size=28, fill="tint", color="brand_dark"))
    if french:
        f = T("exf", french, PXR + 35, 660, size=44, max_w=560, line_h=1.25)
        fy = layout_text(f)["bbox"][3] + 20
        t = T("ext", frtr, PXR + 35, fy, size=32, font="regular", color="soft", max_w=560)
        els += [Box("exb", PXR, 628, 630, layout_text(t)["bbox"][3] + 30 - 628, fill="card", outline="line", radius=24), f, t]
    return els


PANEL_IDS = ["word", "wtr", "num", "exb", "exf", "ext"]


def cards3(items, y=300, h=520):
    """Trois cartes numérotées côte à côte : (numéro, titre, sous-texte)."""
    els = []
    for i, (num, head, sub) in enumerate(items):
        x = 120 + i * 570
        els.append([Box(f"p{i}", x, y, 540, h, fill="card", outline="brand", radius=32, width=3),
                    Dot(f"pn{i}", x + 80, y + 90, r=46, fill="brand", outline=None, width=0, label=num, lcolor="white"),
                    T(f"ph{i}", head, x + 40, y + 180, size=50, font="display", max_w=460, line_h=1.15),
                    T(f"ps{i}", sub, x + 40, y + 340, size=36, color="brand", max_w=470, line_h=1.35)])
    return els


SCENES = []

# =============================================================================
# 1. Giriş : deux questions, la promesse, le rappel du site, le programme
# =============================================================================
b = [beat(clear=True, show=[Badge("q1n", "Soru 1", CX, 170, size=36, fill="gold", color="ink", align="center"),
                            T("q1", "Almak istediğin şeyin [Fransızca adını bilmiyorsan]\nonu nasıl satın alırsın?".replace("[Fransızca adını bilmiyorsan]", "[Fransızca adını bilmiyorsan|hl]"),
                              CX, 250, size=66, font="display", align="center", line_h=1.25, max_w=1700)],
          say=TR("Almak istediğin şeyin Fransızca adını bilmiyorsan onu nasıl satın alırsın?"), pause=0.5),
     beat(show=[Badge("q2n", "Soru 2", CX, 520, size=36, fill="gold", color="ink", align="center"),
                T("q2", "« Bu ne kadar? » sorusunu Fransızcada\n[kaç farklı şekilde|hl] sorabilirsin?", CX, 600, size=66, font="display", align="center", line_h=1.25, max_w=1700)],
          say=TR("Bu ne kadar sorusunu Fransızcada kaç farklı şekilde sorabilirsin?"), pause=0.5),
     beat(show=[Box("prb", 260, 850, 1400, 110, fill="brand", outline=None, radius=55),
                T("pr", "Bu derste bu soruların cevabını beraber göreceğiz.", CX, 876, size=48, color="white", align="center")],
          say=TR("Bu derste bu soruların cevabını beraber göreceğiz."), pause=0.6),
     beat(clear=True, show=[Img("hero", IMG + "m07-hero.webp", 120, 150, 1680, 630, radius=36),
                            Box("hb", 120, 640, 1680, 140, fill="night", outline=None, radius=0, alpha=0.78),
                            T("h1", "Modül 7 · [Alışveriş|gold]", 170, 668, size=76, font="display", color="white"),
                            Badge("url", "Alıştırmalar · Modül testi · PDF özet fişi:  kolayfransizca.app", CX, 850, size=38, fill="gold", color="ink", align="center")],
          say=TR("Merhaba! Kolay Fransızca'nın DELF A1 hazırlık kursunun yedinci modülüne hoş geldin. Bu videoyu YouTube'da açtıysan bilmeni isterim: "
                 "alıştırmalar, modül testi ve PDF özet fişi kolayfransizca.app sitemizde seni bekliyor."), pause=0.4),
     beat(clear=True, show=title("Bu derste neler öğreneceksin?"), say=TR("Peki bu derste neler öğreneceksin?"), pause=0.1)]
for c, say in zip(cards3([("1", "Fiyat sormak\nve ödemek", "Ça coûte combien ?\nJe paie par carte."),
                          ("2", "Kibarca istemek\nve göstermek", "Je voudrais ce pull.\nJe voudrais ça."),
                          ("3", "Giysi, renk\nve beden", "une robe noire\nQuelle taille ?")]),
                  ["Bir: fiyat sormayı, fiyatı anlamayı ve ödeme yapmayı.", "İki: bir ürünü kibarca istemeyi ve parmağınla göstermeyi.",
                   "Üç: giysilerin adlarını, renkleri ve bedeni. Başlayalım!"]):
    b.append(beat(show=c, say=TR(say), pause=0.25))
SCENES.append(scene("Giriş", b, fit=False))

# =============================================================================
# 2. Diyalog : une seule écoute, bulles ligne par ligne avec la traduction
# =============================================================================
DIALOGUE = [
    ("La vendeuse", "Bonjour monsieur ! Je peux vous aider ?", "Merhaba beyefendi! Yardımcı olabilir miyim?"),
    ("Emre", "Bonjour. [Je voudrais|hl] un pull, s'il vous plaît. C'est pour ma mère.", "Merhaba. Bir kazak istiyorum, lütfen. Annem için."),
    ("La vendeuse", "Bien sûr. Quelle [taille|hl] ?", "Tabii. Kaç beden?"),
    ("Emre", "M, je pense. [Ce|hl] pull bleu, il coûte [combien|hl] ?", "M, sanırım. Bu mavi kazak ne kadar?"),
    ("La vendeuse", "[Ce|hl] pull coûte quarante-cinq euros.", "Bu kazak kırk beş euro."),
    ("Emre", "Oh, c'est un peu cher. Vous avez [moins cher|hl] ?", "Ah, biraz pahalı. Daha ucuzu var mı?"),
    ("La vendeuse", "Oui, [ces|hl] pulls sont à vingt-cinq euros.", "Evet, bu kazaklar yirmi beş euro."),
    ("Emre", "Très bien. Vous avez d'autres [couleurs|hl] ?", "Çok iyi. Başka renkler var mı?"),
    ("La vendeuse", "Oui : rouge, vert ou noir.", "Evet: kırmızı, yeşil veya siyah."),
    ("Emre", "Je prends le rouge. Et [ça|gold], [qu'est-ce que c'est|gold] ?", "Kırmızısını alıyorum. Peki şu nedir?"),
    ("La vendeuse", "[Ça|gold] ? C'est une écharpe. Elle coûte douze euros.", "Şu mu? Bu bir atkı. On iki euro."),
    ("Emre", "D'accord, je prends [ça|gold] aussi. Ça fait [combien|hl] ?", "Tamam, onu da alıyorum. Toplam ne kadar?"),
    ("La vendeuse", "Ça fait trente-sept euros. Vous payez comment ?", "Otuz yedi euro tutuyor. Nasıl ödüyorsunuz?"),
    ("Emre", "Par carte, s'il vous plaît.", "Kartla, lütfen."),
    ("La vendeuse", "Voilà. Merci et bonne journée !", "Buyurun. Teşekkürler, iyi günler!"),
    ("Emre", "Merci, au revoir !", "Teşekkürler, hoşça kalın!"),
]
WHO = {"Emre": ("a1/img/kisiler/emre.webp", "gold", "gold_tint", "E"), "La vendeuse": ("a1/img/kisiler/vendeuse.webp", "brand", "tint", "V")}
PER = 4


def portrait(pid, who, x, y, size):
    path, colr, _, letter = WHO[who]
    if os.path.exists(SITE_ROOT / path):
        return [Dot(pid + "r", x + size / 2, y + size / 2, r=size // 2 + 5, fill="white", outline=colr, width=5),
                Img(pid, path, x, y, size, size, radius=size // 2, top=True)]
    return [Dot(pid, x + size / 2, y + size / 2, r=size // 2, fill=colr, label=letter)]


def dialogue_page(page, k):
    """Répliques de la page jusqu'à la k-ième, en bulles avec la traduction : Emre à gauche, la vendeuse à droite."""
    show, y = [], 118
    for kk in range(k + 1):
        who, french, tr = DIALOGUE[page * PER + kk]
        cur, left = kk == k, who == "Emre"
        bx = 230 if left else 390
        plain = re.sub(r"\[([^|\]]+)\|[^\]]+\]", r"\1", french)
        f = T(f"df{kk}", french if cur else plain, bx + 44, y + 22, size=48 if len(plain) < 48 else 41, max_w=1210, color="ink" if cur else "mute", line_h=1.2)
        bottom = layout_text(f)["bbox"][3]
        t = T(f"dt{kk}", tr, bx + 44, bottom + 10, size=33, font="regular", color="soft" if cur else "mute", max_w=1210, line_h=1.2)
        bottom = layout_text(t)["bbox"][3]
        h = max(124, bottom + 26 - y)
        show += portrait(f"da{kk}", who, 70 if left else 1740, y + (h - 110) / 2, 110)
        show += [Bubble(f"db{kk}", bx, y, 1300, h, "left" if left else "right", fill=WHO[who][2], outline=WHO[who][1], dim=not cur), f, t]
        y += h + 26
    return show


b = [beat(clear=True, show=chapter(1, "Emre annesine bir hediye alıyor."),
          say=TR("Önce diyaloğu dinleyelim. Emre annesine bir hediye almak için bir giyim mağazasına giriyor."), pause=0.2),
     beat(clear=True, show=[Img("dimg", IMG + "m07-dialogue.webp", 400, 130, 1120, 760, radius=36),
                            Badge("pass", "Dinlerken iki şeyi bul: Emre ne alıyor? Toplam ne kadar ödüyor?", CX, 925, size=36, fill="gold", color="ink", align="center")],
          say=TR("Dinlerken iki şeyi bulmaya çalış. Emre ne alıyor? Ve toplam ne kadar ödüyor?"), pause=0.5)]
for i in range(len(DIALOGUE)):
    b.append(beat(clear=(i % PER == 0), show=dialogue_page(i // PER, i % PER), say=D(i + 1), lead=0.12, pause=0.5))
b.append(beat(clear=True, show=title("Emre ne aldı?") + [
        Box("r1", 220, 300, 1480, 130, fill="card", outline="line", radius=26), T("r1a", "le pull [rouge|no]", 270, 332, size=58), T("r1p", "25 €", 1650, 326, size=64, font="display", align="right"),
        Box("r2", 220, 450, 1480, 130, fill="card", outline="line", radius=26), T("r2a", "l'écharpe", 270, 482, size=58), T("r2p", "12 €", 1650, 476, size=64, font="display", align="right")],
              say=TR("Emre ne aldı? Yirmi beş euroya kırmızı bir kazak ve on iki euroya bir atkı."), pause=0.3))
b.append(beat(show=[Box("r3", 220, 620, 1480, 150, fill="brand", outline=None, radius=26), T("r3a", "Ça fait...", 270, 660, size=58, color="white"),
                    T("r3p", "37 €", 1650, 650, size=80, font="display", color="white", align="right"),
                    Badge("r4", "par carte · kartla", CX, 830, size=40, fill="gold", color="ink", align="center")],
              say=TR("Toplam otuz yedi euro. Ve kartla ödedi. Atkının adını bilmiyordu ama yine de onu aldı. Nasıl yaptığını birazdan göreceğiz."), pause=0.5))
b.append(beat(clear=True, show=[
        T("rp0", "Diyaloğu tekrar et", CX, 250, size=96, font="display", align="center"),
        T("rp1", "Bu videodan sonra diyaloğu birkaç kez yeniden oku\nve cümleleri [yüksek sesle|hl] tekrar et.", CX, 430, size=54, align="center", line_h=1.4),
        Badge("rpu", "Diyaloğun metni ve sesleri:  kolayfransizca.app", CX, 680, size=40, fill="gold", color="ink", align="center")],
              say=TR("Bu videodan sonra diyaloğu birkaç kez yeniden okumanı ve cümleleri yüksek sesle tekrar etmeni tavsiye ederim. "
                     "Metni ve sesleri sitemizde bulabilirsin."), pause=0.5))
SCENES.append(scene("Diyalog", b, fit=False))

# =============================================================================
# 3. Dilbilgisi : fiyat sormak (réponse à la deuxième question)
# =============================================================================
WAYS = [("Ça coûte [combien|hl] ?", "Bu ne kadar?", 1), ("C'est [combien|hl] ?", "Ne kadar? (en kısa yol)", 2),
        ("[Combien|hl] coûte ce pull ?", "Bu kazak ne kadar?", 3), ("Quel est [le prix|gold] de ce sac ?", "Bu çantanın fiyatı nedir? (daha resmî)", 4)]
b = [beat(clear=True, show=chapter(2, "« Bu ne kadar? » sorusunun dört yolu."), say=TR("İkinci bölüm: fiyat sormak. Dersin başındaki ikinci soruyu hatırla. Cevabı: en az dört farklı şekilde."), pause=0.2),
     beat(clear=True, show=title("Bu ne kadar?", "Dört yol, hepsi doğru. İlk ikisi en sık duyacakların."), say=TR("Dördü de doğrudur. Günlük hayatta en çok ilk ikisini duyarsın."), pause=0.1)]
for i, (french, tr, g) in enumerate(WAYS):
    y = 300 + i * 165
    b.append(beat(show=[Box(f"wb{i}", 120, y, 1680, 145, fill="card", outline="brand" if i < 2 else "line", radius=26, width=3 if i < 2 else 2),
                        Dot(f"wn{i}", 195, y + 72, r=40, fill="brand" if i < 2 else "mute", outline=None, width=0, label=str(i + 1), lcolor="white"),
                        T(f"wf{i}", french, 270, y + 26, size=58), T(f"wt{i}", tr, 1750, y + 46, size=36, font="regular", color="soft", align="right")],
                  say=[G(g), TR(tr.split(" (")[0])], lead=0.05, pause=0.25))
b.append(beat(clear=True, show=title("Cevabı anlamak") + [
        Img("i1", IMG + "items/pull.webp", 150, 270, 250, 250, radius=0), Badge("i1p", "25 €", 275, 540, size=40, fill="brand", color="white", align="center"),
        T("a1", "Ça coût[e|no] vingt-cinq euros.", 480, 320, size=64), T("a1t", "Yirmi beş euro. (tek ürün)", 480, 420, size=38, font="regular", color="soft")],
              say=[G(5), TR("Yirmi beş euro.")], pause=0.2))
b.append(beat(show=[Img("i2", IMG + "items/chaussures.webp", 150, 610, 250, 250, radius=0), Badge("i2p", "55 €", 275, 880, size=40, fill="brand", color="white", align="center"),
                    T("a2", "Ces chaussures coût[ent|no] cinquante-cinq euros.", 480, 660, size=58, max_w=1320), T("a2t", "Bu ayakkabılar elli beş euro. (çoğul)", 480, 760, size=38, font="regular", color="soft")],
              say=[G(7), TR("Bu ayakkabılar elli beş euro.")], pause=0.2))
b.append(beat(show=term("un verbe", "fiil"), say=TR("Fiyatı söyleyen kelime bir fiildir. Fransızcada fiile « un verbe » denir. Tekilde ve çoğulda yazılışı farklıdır ama okunuşu aynıdır."), pause=0.3))
b.append(beat(show=term("la terminaison", "fiilin son eki"), say=TR("Kırmızı kısma bak: fiilin son eki. Fransızcası « la terminaison ». Çoğuldaki son üç harf okunmaz."), pause=0.5))
b.append(beat(clear=True, show=title("Kasada: toplam", "Tek ürün için « Ça coûte », hepsi için « Ça fait »." ) + [
        T("b1", "le pull", 300, 330, size=54), T("b1p", "25 €", 1100, 324, size=60, font="display", align="right"),
        T("b2", "l'écharpe", 300, 430, size=54), T("b2p", "12 €", 1100, 424, size=60, font="display", align="right"),
        Box("bl", 300, 530, 800, 5, fill="ink", outline=None, radius=0),
        T("b3", "Ça [fait|hl] combien ?", 300, 580, size=64), T("b3t", "Toplam ne kadar?", 300, 680, size=38, font="regular", color="soft")],
              say=[G(8), TR("Toplam ne kadar?")], pause=0.2))
b.append(beat(show=[Box("b4b", 1180, 300, 620, 420, fill="brand", outline=None, radius=32), T("b4", "37 €", 1490, 340, size=150, font="display", color="white", align="center"),
                    T("b4t", "Ça [fait|gold] trente-sept euros.", 1490, 580, size=40, color="white", align="center", max_w=560)],
              say=[G(9), TR("Otuz yedi euro tutuyor. Tek bir ürünün fiyatını sorarken birinci fiili, kasada toplamı sorarken ikinci fiili kullan.")], pause=0.5))
# lire un prix
b.append(beat(clear=True, show=title("Fiyatı okumak", "« euro » kelimesi iki sayının ortasında söylenir.") + [
        Box("p1", 120, 300, 520, 200, fill="card", outline="brand", radius=28, width=3), T("p1a", "12 €", 380, 340, size=110, font="display", align="center"),
        T("p1b", "douze [euros|hl]", 720, 360, size=64)],
              say=[G(10), TR("On iki euro.")], pause=0.2))
b.append(beat(show=[Box("p2", 120, 530, 520, 200, fill="card", outline="brand", radius=28, width=3), T("p2a", "2[,|no]50 €", 380, 570, size=110, font="display", align="center"),
                    T("p2b", "deux [euros|hl] cinquante", 720, 590, size=64)],
              say=[G(11), TR("İki euro elli. Yazıda virgül var ama konuşurken virgül denmez: onun yerine para birimi söylenir.")], pause=0.2))
b.append(beat(show=hata("deux cinquante euros", "deux euros cinquante", y=790), say=TR("Türkçedeki gibi sayıları yan yana söyleme. Para birimi ortaya gelir."), pause=0.5))
b += qcm(1, 0, "Dinle: elbise ne kadar?", ["39,80 €", "39,90 €", "49,90 €"], 1, ("« trente-neuf euros quatre-vingt-dix » = 39,90 €", "Doğru cevap ikinci şık: otuz dokuz euro doksan."),
         [TR("Sıra sende. Dinle: elbise ne kadar?"), F("quiz/m7-q01.mp3"), F("quiz/m7-q01.mp3")], label="Sıra sende", qsize=72)
SCENES.append(scene("Dilbilgisi: fiyat sormak", b, fit=False))

# =============================================================================
# 4. Dilbilgisi : je voudrais
# =============================================================================
b = [beat(clear=True, show=chapter(3, "« İstiyorum » demenin kibar yolu."), say=TR("Üçüncü bölüm: bir şeyi kibarca istemek. Türkçe konuşanların en sık yaptığı hata burada."), pause=0.2),
     beat(clear=True, show=title("« İstiyorum » nasıl denir?") + [
         Box("v1", 120, 280, 820, 400, fill="no_tint", outline="no", radius=32, width=4), Badge("v1l", "Emir gibi · kaba kaçar", 530, 310, size=34, fill="no", color="white", align="center"),
         T("v1t", "Je [veux|no] un pull.", 530, 430, size=76, font="display", align="center"), T("v1s", "Bir kazak istiyorum.", 530, 560, size=40, font="regular", color="soft", align="center")],
          say=[FR("Je veux un pull.", "M1"), TR("Türkçedeki istiyorum kelimesini böyle çevirirsen dükkânda emir verir gibi konuşmuş olursun. Satıcının yüzü asılır.")], pause=0.3),
     beat(show=[Box("v2", 980, 280, 820, 400, fill="ok_tint", outline="ok", radius=32, width=4), Badge("v2l", "Kibar · her zaman bunu kullan", 1390, 310, size=34, fill="ok", color="white", align="center"),
                T("v2t", "Je [voudrais|ok] un pull,\ns'il vous plaît.", 1390, 410, size=64, font="display", align="center", line_h=1.2),
                T("v2s", "Bir kazak rica ediyorum, lütfen.", 1390, 590, size=40, font="regular", color="soft", align="center")],
          say=[G(14), TR("Fransızlar böyle der. Anlamı aynıdır ama çok daha kibardır.")], pause=0.3),
     beat(show=rule("Dükkânda, kafede, gişede: her zaman « je voudrais ».", 760), say=TR("Dükkânda, kafede, gişede: bir şey isterken her zaman bu kalıbı kullan."), pause=0.5),
     beat(clear=True, show=title("Arkasından ne gelir?") + ex_line("j1", "Je voudrais [un pull|hl].", "Bir kazak istiyorum.  →  arkasından bir isim", 140, 280, size=64, trsize=40),
          say=[FR("Je voudrais un pull.", "F1"), TR("Arkasından bir isim gelebilir.")], pause=0.2),
     beat(show=ex_line("j2", "Je voudrais [essayer|gold] cette robe.", "Bu elbiseyi denemek istiyorum.  →  arkasından bir fiil, mastar hâlinde", 140, 480, size=64, trsize=40),
          say=[G(15), TR("Ya da bir fiil gelebilir. O zaman ikinci fiil çekilmez, mastar hâlinde kalır.")], pause=0.2),
     beat(show=ex_line("j3", "Je [prends|hl] le rouge.", "Kırmızısını alıyorum.  →  karar verince", 140, 680, size=64, trsize=40),
          say=[G(18), TR("Karar verdiğinde ise almak fiilini kullanırsın. Onu altıncı modülde öğrendin.")], pause=0.5),
     beat(clear=True, show=note("Mağazaya girerken: « Bonjour ! »\nBir şey isterken: « Je voudrais... s'il vous plaît. »\nÇıkarken: « Merci, au revoir ! »"),
          say=TR("Benim tavsiyem: üç şeyi hiç unutma. Girerken selam ver. İsterken kibar kalıbı kullan ve lütfen de. Çıkarken teşekkür et ve vedalaş."), pause=0.6)]
b += qcm(2, 0, "Satıcıya hangisini söylersin?", ["Je veux ça.", "Je voudrais ça, s'il vous plaît.", "Donne-moi ça."], 1,
         ("« Je voudrais... s'il vous plaît. »", "Doğru cevap ikinci şık. Diğer ikisi kaba kaçar."), TR("Sıra sende. Satıcıya hangisini söylersin?"), label="Sıra sende", qsize=72)
SCENES.append(scene("Dilbilgisi: je voudrais", b, fit=False))

# =============================================================================
# 5. Dilbilgisi : ce, cet, cette, ces
# =============================================================================
COLS = [("pull", "ce", "pull", "eril · masculin", "tint", "brand", 21, "ce pull · ce sac"),
        ("robe", "cette", "robe", "dişil · féminin", "no_tint", "no", 23, "cette robe · cette écharpe"),
        ("chaussures", "ces", "chaussures", "çoğul · pluriel", "ok_tint", "ok", 24, "ces pulls · ces chaussures")]
b = [beat(clear=True, show=chapter(4, "Türkçede tek kelime: « bu ». Fransızcada dört biçim."), say=TR("Dördüncü bölüm. Türkçede bu kelimesi hiç değişmez. Fransızcada ise dört biçimi vardır."), pause=0.2),
     beat(clear=True, show=title("Türkçede: hep « bu »") + [
         T("t0", "[bu|hl] kazak", 395, 330, size=70, font="display", align="center"), T("t1", "[bu|hl] elbise", 960, 330, size=70, font="display", align="center"),
         T("t2", "[bu|hl] ayakkabılar", 1525, 330, size=70, font="display", align="center")],
          say=TR("Bu kazak, bu elbise, bu ayakkabılar. Türkçede hep aynı kelime."), pause=0.3)]
STY = {"brand": "hl", "no": "no", "ok": "ok"}
for i, (img, det, noun, lab, tint, line, g, both) in enumerate(COLS):
    x = 120 + i * 565
    b.append(beat(show=[Box(f"c{i}", x, 470, 550, 470, fill=tint, outline=line, radius=32, width=4),
                        Img(f"ci{i}", IMG + f"items/{img}.webp", x + 165, 490, 220, 220, radius=0),
                        T(f"ct{i}", f"[{det}|{STY[line]}] {noun}", x + 275, 720, size=64, font="display", align="center"),
                        Badge(f"cl{i}", lab, x + 275, 850, size=34, fill=line, color="white", align="center")],
                  say=[G(g), TR({0: "İsim erilse.", 1: "İsim dişilse.", 2: "İsim çoğulsa: eril de olsa, dişil de olsa."}[i])], lead=0.05, pause=0.3))
b.append(beat(hide=["title", "t0", "t1", "t2"], show=term("masculin · féminin · pluriel", "eril · dişil · çoğul", y=330) + [
        T("dq", "İsmin önüne gelen bu küçük kelimeler: [déterminant|fr]", CX, 180, size=52, align="center")],
              say=TR("İsmin önüne gelen bu küçük kelimelere Fransızcada « un déterminant » denir. Hangisini seçeceğin isme bağlıdır: "
                     "eril, yani « masculin ». Dişil, yani « féminin ». Ya da çoğul, yani « pluriel »."), pause=0.6))
# cet : devant une voyelle ou un h muet
b.append(beat(clear=True, show=title("Dördüncü biçim: sesli harften önce") + [
        Box("f1", 420, 320, 240, 160, fill="card", outline="brand", radius=24, width=4), T("f1t", "ce", 540, 350, size=90, font="display", align="center"),
        Box("f2", 700, 320, 800, 160, fill="card", outline="line", radius=24, width=3), T("f2t", "[o|no]rdinateur", 1100, 350, size=90, font="display", align="center"),
        T("fn", "İki sesli harf yan yana: söylemesi zor.", CX, 540, size=44, font="regular", color="soft", align="center")],
              say=TR("Peki eril bir isim sesli harfle başlıyorsa? İki sesli harf yan yana gelir ve söylemesi zorlaşır."), pause=0.3))
b.append(beat(show=[Box("f1", 420, 320, 290, 160, fill="brand", outline="brand", radius=24, width=4), T("f1t", "ce[t|gold]", 565, 350, size=90, font="display", align="center", color="white"),
                    Box("f2", 740, 320, 800, 160, fill="card", outline="line", radius=24, width=3), T("f2t", "ordinateur", 1140, 350, size=90, font="display", align="center"),
                    T("fn", "Araya bir « t » girer: [cet|hl] ordinateur, [cet|hl] hôtel", CX, 540, size=48, align="center")],
              say=[TR("Bu yüzden araya bir harf girer."), G(22), TR("Okunmayan h harfiyle başlayan isimlerde de aynısı olur.")], anim=0.8, pause=0.3))
b.append(beat(show=hata("ce ordinateur", "cet ordinateur", y=650) + rule("Bu biçim, dişil biçimle aynı okunur.", 820, pid="r2"),
              say=TR("Bir ipucu: bu dördüncü biçim, dişil biçimle tıpatıp aynı okunur. Sadece yazılışı farklıdır."), pause=0.5))
b.append(beat(clear=True, show=note("Her yeni ismi tanımlığıyla ezberle: « le sac », « la robe ».\nCinsiyeti bilirsen hangi biçimi kullanacağını da bilirsin.\n"
                                    "Fransızcada « bu » ile « şu » ayrımı yoktur."),
              say=TR("Benim tavsiyem: her yeni ismi tanımlığıyla birlikte ezberle. Cinsiyeti bilirsen hangi biçimi kullanacağını da bilirsin. "
                     "Bir de şunu bil: Fransızcada bu ile şu arasında fark yoktur, ikisi için de aynı kelime kullanılır."), pause=0.6))
b += qcm(3, 0, "___ chemise est belle.", ["Ce", "Cet", "Cette"], 2, ("la chemise: dişil → « cette chemise »", "Doğru cevap üçüncü şık. İsim dişil."),
         TR("Sıra sende. Boşluğa hangisi gelir?"), label="Sıra sende", qsize=80)
b += qcm(4, 0, "___ hôtel est près de la gare.", ["Ce", "Cet", "Ces"], 1, ("eril + okunmayan h → « cet hôtel »", "Doğru cevap ikinci şık. İsim eril ve okunmayan h ile başlıyor."),
         TR("Bir tane daha."), label="Sıra sende", qsize=72)
SCENES.append(scene("Dilbilgisi: ce, cet, cette, ces", b, fit=False))

# =============================================================================
# 6. Dilbilgisi : ça · Qu'est-ce que c'est ? (réponse à la première question)
# =============================================================================
b = [beat(clear=True, show=chapter(5, "Adını bilmediğin şeyi satın almak."), say=TR("Beşinci bölüm. Şimdi dersin başındaki ilk sorunun cevabına geldik."), pause=0.2),
     beat(clear=True, show=[Img("di", IMG + "m07-dialogue.webp", 80, 190, 1000, 750, radius=36),
                            T("w0", "Emre bu kelimeyi\nbilmiyor:", PXR - 60, 230, size=54, font="regular", color="soft", max_w=700, line_h=1.25),
                            T("w1", "atkı = [?|no]", PXR - 60, 410, size=110, font="display")],
          say=TR("Emre atkı kelimesinin Fransızcasını bilmiyor. Ama onu almak istiyor. Ne yapıyor?"), pause=0.3),
     beat(show=[T("w2", "Et [ça|gold],\n[qu'est-ce que c'est|hl] ?", PXR - 60, 600, size=62, font="display", max_w=720, line_h=1.2),
                T("w3", "Peki şu nedir?", PXR - 60, 790, size=42, font="regular", color="soft")],
          say=[D(10), TR("Parmağıyla gösteriyor ve tek bir küçük kelime söylüyor.")], pause=0.3),
     beat(clear=True, show=title("İsim söylüyorsan · isim söylemiyorsan") + [
         Box("m1", 140, 320, 420, 150, fill="tint", outline="brand", radius=24, width=3), T("m1t", "[ce|hl] pull", 350, 352, size=70, font="display", align="center"),
         Box("m2", 600, 320, 480, 150, fill="no_tint", outline="no", radius=24, width=3), T("m2t", "[cette|no] robe", 840, 352, size=70, font="display", align="center"),
         Box("m3", 1120, 320, 660, 150, fill="ok_tint", outline="ok", radius=24, width=3), T("m3t", "[ces|ok] chaussures", 1450, 352, size=70, font="display", align="center"),
         T("mn", "İsmi söylüyorsan: dört biçimden biri + isim", CX, 520, size=44, font="regular", color="soft", align="center")],
          say=TR("İsmi biliyorsan ve söylüyorsan, az önce öğrendiğin dört biçimden birini kullanırsın."), pause=0.3),
     beat(show=[Box("m1", 760, 600, 400, 210, fill="gold", outline="gold", radius=32, width=3), T("m1t", "ça", 960, 630, size=130, font="display", align="center"),
                Box("m2", 760, 600, 400, 210, fill="gold", outline="gold", radius=32, width=3), T("m2t", "ça", 960, 630, size=130, font="display", align="center"),
                Box("m3", 760, 600, 400, 210, fill="gold", outline="gold", radius=32, width=3), T("m3t", "ça", 960, 630, size=130, font="display", align="center"),
                T("mo", "[ce pull   ·   cette robe   ·   ces chaussures|mute]", CX, 360, size=56, align="center"),
                T("mn", "İsmi söylemiyorsan: tek kelime yeter", CX, 850, size=44, font="regular", color="soft", align="center")],
          say=[TR("Ama ismi bilmiyorsan ya da söylemek istemiyorsan, hepsinin yerine tek bir kelime geçer."), FR("ça", "F1"), FR("ça", "F1")], anim=1.1, pause=0.3),
     beat(show=term("un pronom", "zamir"), say=TR("Bu kelime ismin yerine geçer, yani bir zamirdir. Fransızcada zamire « un pronom » denir. Arkasından isim gelmez."), pause=0.5)]
CA = [("Je voudrais [ça|gold], s'il vous plaît.", "Şunu istiyorum, lütfen.", 25), ("[Ça|gold] coûte combien ?", "Bu ne kadar?", 26), ("Je prends [ça|gold] aussi.", "Bunu da alıyorum.", 28)]
b.append(beat(clear=True, show=title("Bu küçük kelimeyle her şeyi alabilirsin", "Göster ve söyle: adını bilmen gerekmez."), say=TR("Bu küçük kelimeyle Fransa'da her şeyi satın alabilirsin. Göster ve söyle."), pause=0.1))
for i, (french, tr, g) in enumerate(CA):
    b.append(beat(show=ex_line(f"ca{i}", french, tr, 140, 300 + i * 190, size=64, trsize=40), say=[G(g), TR(tr)], lead=0.05, pause=0.25))
b.append(beat(show=hata("Je voudrais ça pull.", "Je voudrais ce pull.", y=870), say=TR("Dikkat: bu kelimenin arkasına isim koyma. İsim varsa dört biçimden birini kullan."), pause=0.5))
b.append(beat(clear=True, show=title("Bu nedir?") + [
        T("k1", "[Qu'est-ce que c'est|hl] ?", 140, 280, size=84, font="display"), T("k1t", "Bu nedir?   ·   okunuşu: kes-kö-se", 140, 400, size=40, font="regular", color="soft")],
              say=[G(29), TR("Uzun yazılır ama tek bir kelime gibi, üç heceyle okunur."), G(29)], pause=0.3))
b.append(beat(show=ex_line("k2", "[C'est|hl] une écharpe.", "Bu bir atkı.  (tekil)", 140, 540, size=64, trsize=40) + ex_line("k3", "[Ce sont|gold] des clés.", "Bunlar anahtar.  (çoğul)", 1000, 540, size=64, trsize=40, max_w=800),
              say=[G(30), TR("Bu bir atkı."), G(31), TR("Bunlar anahtar. Çoğulda cevap değişir.")], pause=0.5))
b += qcm(5, 0, "Adını bilmiyorsun: Je voudrais ___, s'il vous plaît.", ["ce", "ça", "cette"], 1, ("İsim yoksa: « ça »", "Doğru cevap ikinci şık. Diğer ikisi tek başına kullanılmaz."),
         TR("Sıra sende. Ürünün adını bilmiyorsun. Boşluğa hangisi gelir?"), label="Sıra sende", qsize=60)
SCENES.append(scene("Dilbilgisi: ça ve Qu'est-ce que c'est ?", b, fit=False))

# =============================================================================
# 7. Dilbilgisi : la couleur après le nom, l'accord, la taille
# =============================================================================
b = [beat(clear=True, show=chapter(6, "Renk ismin arkasına gelir ve isme uyar."), say=TR("Altıncı bölüm: giysiyi tarif etmek. Önce renk, sonra beden."), pause=0.2),
     beat(clear=True, show=title("Renk nereye gelir?") + [
         Badge("l1", "Türkçe", 300, 300, size=34, fill="tint", color="brand_dark"),
         Box("x1", 300, 370, 360, 150, fill="gold_tint", outline="gold", radius=24, width=4), T("x1t", "mavi", 480, 400, size=80, font="display", align="center", color="gold_ink"),
         Box("x2", 700, 370, 360, 150, fill="card", outline="brand", radius=24, width=4), T("x2t", "kazak", 880, 400, size=80, font="display", align="center"),
         Img("xi", IMG + "items/pull.webp", 1350, 300, 380, 380, radius=0)],
          say=TR("Türkçede renk ismin önündedir: mavi kazak."), pause=0.3),
     beat(show=[Badge("l1", "Fransızca", 300, 300, size=34, fill="brand", color="white"),
                Box("x2", 300, 370, 400, 150, fill="card", outline="brand", radius=24, width=4), T("x2t", "un pull", 500, 400, size=80, font="display", align="center"),
                Box("x1", 740, 370, 360, 150, fill="gold_tint", outline="gold", radius=24, width=4), T("x1t", "bleu", 920, 400, size=80, font="display", align="center", color="gold_ink"),
                T("xn", "Fransızcada renk ismin [arkasına|hl] gelir.", 300, 600, size=50, max_w=1000)],
          say=[TR("Fransızcada ise tam tersi: renk ismin arkasına gelir."), FR("un pull bleu", "F1")], anim=1.0, pause=0.3),
     beat(show=hata("un bleu pull", "un pull bleu", y=730) + term("un adjectif", "sıfat"),
          say=TR("Renkler birer sıfattır. Fransızcada sıfata « un adjectif » denir. Ve sıfat, ismin cinsiyetine ve sayısına uyar."), pause=0.5)]
# le tableau des accords
ROWS = [("noir", "siyah", "un pull noir", "une robe noir[e|no]", "des pulls noir[s|ok]", FR("un pull noir, une robe noire", "F1")),
        ("bleu", "mavi", "un sac bleu", "une veste bleu[e|no]", "des sacs bleu[s|ok]", FR("un sac bleu, une veste bleue", "F1")),
        ("vert", "yeşil", "un pull vert", "une jupe ver[te|no]", "des pulls vert[s|ok]", G(32)),
        ("blanc", "beyaz", "un pantalon blanc", "une chemise blanc[he|no]", "des pantalons blanc[s|ok]", G(33)),
        ("rouge", "kırmızı", "un sac rouge", "une robe rouge", "des sacs rouge[s|ok]", FR("un sac rouge, une robe rouge", "F1"))]
RSAY = ["Dişilde sona bir harf eklenir. Okunuşu değişmez.", "Aynı şekilde. Okunuşu yine aynı.", "Burada dikkat: dişilde sondaki sessiz harf artık okunur.",
        "Bu renk düzensizdir: dişilde sonu tamamen değişir.", "Bu renk zaten o harfle bitiyor: dişilde değişmez."]
b.append(beat(clear=True, show=[T("title", "Sıfatın sonu değişir", 120, 110, size=60, font="display"),
                                Badge("h1", "masculin · eril", 440, 215, size=30, fill="brand", color="white"), Badge("h2", "féminin · dişil: + e", 880, 215, size=30, fill="no", color="white"),
                                Badge("h3", "pluriel · çoğul: + s", 1350, 215, size=30, fill="ok", color="white")] + term("la terminaison", "kelimenin sonu", y=968),
              say=TR("Sıfatın sonu değişir. Bu son kısmın Fransızcası « la terminaison ». Dişilde genellikle bir harf, çoğulda bir harf daha eklenir."), pause=0.2))
for r, (w, tr, m, f, p, audio) in enumerate(ROWS):
    y = 285 + r * 132
    b.append(beat(show=[Box(f"rb{r}", 120, y, 1680, 118, fill="card", outline="line", radius=22),
                        T(f"rw{r}", w, 150, y + 16, size=48, font="display", color="brand"), T(f"rt{r}", tr, 150, y + 74, size=28, font="regular", color="soft"),
                        T(f"rm{r}", m, 440, y + 34, size=40), T(f"rf{r}", f, 880, y + 34, size=40), T(f"rp{r}", p, 1350, y + 34, size=40)],
                  say=[audio, TR(RSAY[r])], lead=0.05, pause=0.25))
b.append(beat(clear=True, show=title("Üç şeyi hatırla") + [
        Dot("u0", 190, 330, r=44, fill="gold", outline=None, width=0, label="1"), T("uq0", "Dişilde sona [-e|no] eklenir: noir → noir[e|no]", 270, 298, size=52),
        Dot("u1", 190, 500, r=44, fill="gold", outline=None, width=0, label="2"), T("uq1", "Çoğulda sona [-s|ok] eklenir ve okunmaz: des pulls bleu[s|ok]", 270, 468, size=52, max_w=1500),
        Dot("u2", 190, 670, r=44, fill="gold", outline=None, width=0, label="3"), T("uq2", "Dişil ve çoğul birlikte: des chaussures noir[e|no][s|ok]", 270, 638, size=52, max_w=1500)],
              say=[TR("Üç şeyi hatırla. Bir: dişilde sona bir harf eklenir. İki: çoğulda bir harf daha eklenir ve okunmaz. Üç: isim hem dişil hem çoğulsa ikisi birden gelir."), G(34)], pause=0.5))
# la taille
SIZE = [("Quelle est votre [taille|hl] ?", "Bedeniniz nedir?", 35), ("Je fais du [M|gold].", "Bedenim M.", 36), ("Je peux [essayer|hl] ?", "Deneyebilir miyim?", 37),
        ("C'est [trop|no] petit.", "Fazla küçük.", 38), ("C'est [trop|no] grand.", "Fazla büyük.", 39)]
b.append(beat(clear=True, show=title("Beden ve deneme") + [Box(f"z{i}", 1300 + i * 170, 130, 140, 100, fill="gold" if s == "M" else "card", outline="brand", radius=20, width=3) for i, s in enumerate("SML")]
              + [T(f"zt{i}", s, 1370 + i * 170, 146, size=58, font="display", align="center") for i, s in enumerate("SML")],
              say=TR("Şimdi beden. Satıcı sana bedenini sorar, sen de cevap verirsin."), pause=0.1))
for i, (french, tr, g) in enumerate(SIZE):
    x, y = (140, 290 + i * 200) if i < 3 else (1000, 290 + (i - 3) * 200)
    b.append(beat(show=ex_line(f"sz{i}", french, tr, x, y, size=58, trsize=38, max_w=800), say=[G(g), TR(tr)], lead=0.05, pause=0.2))
b += qcm(6, 0, "Une robe ___.", ["noir", "noire", "noirs"], 1, ("la robe: dişil → « noire »", "Doğru cevap ikinci şık. İsim dişil, sıfatın sonuna bir harf eklenir."),
         TR("Sıra sende. Boşluğa hangisi gelir?"), label="Sıra sende", qsize=90)
SCENES.append(scene("Dilbilgisi: renk ve beden", b, fit=False))

# =============================================================================
# 8. Dilbilgisi : comparer, quantités, payer
# =============================================================================
b = [beat(clear=True, show=chapter(7, "Pahalı mı, ucuz mu? Ve kasada."), say=TR("Yedinci bölüm: karşılaştırmak ve ödemek."), pause=0.2),
     beat(clear=True, show=title("Hangisi daha pahalı?") + [
         Img("c1", IMG + "items/pull.webp", 250, 260, 330, 330, radius=0), Badge("c1p", "45 €", 415, 610, size=54, fill="brand", color="white", align="center"),
         Img("c2", IMG + "items/chemise.webp", 1340, 260, 330, 330, radius=0), Badge("c2p", "30 €", 1505, 610, size=54, fill="brand", color="white", align="center"),
         T("cv", ">", CX, 340, size=160, font="display", color="soft", align="center")],
          say=TR("Kazak kırk beş euro, gömlek otuz euro. Hangisi daha pahalı?"), pause=0.3),
     beat(show=ex_line("cp1", "Ce pull est [plus cher que|hl] cette chemise.", "Bu kazak bu gömlekten daha pahalı.", CX - 700, 730, size=58, trsize=38, max_w=1400),
          say=[G(41), TR("Sıfatın önüne daha anlamında bir kelime, karşılaştırdığın şeyin önüne de ikinci bir kelime gelir: Türkçedeki ekin karşılığıdır.")], pause=0.3),
     beat(hide=["cp1", "cp1t"], show=[Badge("c2p", "30 €", 1505, 610, size=54, fill="gold", color="ink", align="center"), Badge("c1p", "45 €", 415, 610, size=54, fill="mute", color="white", align="center")]
          + ex_line("cp2", "Cette chemise est [moins ch|hl][ère|no] [que|hl] ce pull.", "Bu gömlek bu kazaktan daha ucuz.", CX - 700, 730, size=58, trsize=38, max_w=1400),
          say=[G(42), TR("Tersini söylemek için daha az anlamındaki kelimeyi kullan. İsim dişil olduğu için sıfatın sonu da değişti.")], pause=0.3),
     beat(clear=True, show=title("Mağazada işine yarar") + ex_line("mc1", "C'est [trop cher|no].", "Bu fazla pahalı.", 140, 300, size=64, trsize=40)
          + ex_line("mc2", "Vous avez [moins cher|hl] ?", "Daha ucuzu var mı?", 140, 500, size=64, trsize=40)
          + [T("mc3", "ucuz = [pas cher|ok]  ·  daha ucuz = [moins cher|ok]", 140, 720, size=50)],
          say=[G(45), TR("Bu fazla pahalı."), G(44), TR("Daha ucuzu var mı? Fransızcada ucuz için ayrı bir kelime aramana gerek yok: pahalı değil demen yeterli.")], pause=0.5),
     # quantités
     beat(clear=True, show=title("Miktar söylemek", "Miktar kelimesinden sonra her zaman aynı küçük kelime gelir.")
          + ex_line("qt1", "un kilo [de|hl] tomates", "bir kilo domates", 140, 300, size=64, trsize=40),
          say=[G(46), TR("Bir kilo domates.")], pause=0.2),
     beat(show=ex_line("qt2", "une bouteille [d'|hl]eau", "bir şişe su  ·  sesli harften önce kısalır", 140, 490, size=64, trsize=40), say=[G(48), TR("Bir şişe su.")], pause=0.2),
     beat(show=hata("un kilo des tomates", "un kilo de tomates", y=720), say=TR("Miktardan sonra tanımlık gelmez. Bu kural hiç değişmez."), pause=0.5)]
# à la caisse
PAY = [("Vous payez [comment|hl] ?", "Nasıl ödüyorsunuz?", 50), ("Je paie [par carte|hl].", "Kartla ödüyorum.", 51), ("Je paie [en espèces|gold].", "Nakit ödüyorum.", 52),
       ("Voilà votre [monnaie|gold].", "Buyurun, para üstünüz.", 54)]
b.append(beat(clear=True, show=title("Kasada") + [Img("ci", IMG + "m07-caisse.webp", 1040, 250, 760, 570, radius=32)], say=TR("Ve kasadayız. Dört cümle yeter."), pause=0.1))
for i, (french, tr, g) in enumerate(PAY):
    b.append(beat(show=ex_line(f"py{i}", french, tr, 120, 270 + i * 175, size=54, trsize=36, max_w=880), say=[G(g), TR(tr)], lead=0.05, pause=0.2))
# acheter et payer
PRON = ["je", "tu", "il / elle", "nous", "vous", "ils / elles"]
CONJ = [("acheter", "satın almak", ["ach[è|no]te", "ach[è|no]tes", "ach[è|no]te", "[achet|ok]ons", "[achet|ok]ez", "ach[è|no]tent"], 55),
        ("payer", "ödemek", ["pa[i|no]e", "pa[i|no]es", "pa[i|no]e", "[pay|ok]ons", "[pay|ok]ez", "pa[i|no]ent"], 61)]
b.append(beat(clear=True, show=[T("title", "İki fiil: acheter ve payer", 120, 110, size=60, font="display")]
              + [T(f"pr{r}", p, 200, 388 + r * 84, size=42, font="regular", color="soft") for r, p in enumerate(PRON)] + term("un pronom personnel", "şahıs zamiri", y=930),
              say=TR("Son olarak iki fiil. Soldaki küçük kelimeler şahıs zamirleridir, Fransızcası « un pronom personnel »."), pause=0.2))
for c, (verb, tr, forms, g0) in enumerate(CONJ):
    x = 560 + c * 620
    b.append(beat(show=[Box(f"vb{c}", x - 40, 210, 560, 690, fill="card", outline="line", radius=26),
                        T(f"vh{c}", verb, x, 226, size=60, font="display", color="brand"), T(f"vt{c}", tr, x, 306, size=32, font="regular", color="soft")],
                  say=TR({"acheter": "Satın almak.", "payer": "Ödemek."}[verb]), pause=0.1))
    for r, form in enumerate(forms):
        b.append(beat(show=T(f"v{c}{r}", form, x, 374 + r * 84, size=58, font="display"), say=G(g0 + r), lead=0.05, pause=0.1))
b.append(beat(hide=["termb", "termt"], show=rule("Kırmızı harf dört biçimde değişir. « nous » ve « vous » mastar gibi kalır.", 918, pid="vr"),
              say=TR("Dikkat: kırmızı harf dört biçimde değişir. Biz ve siz biçimleri ise mastardaki gibi kalır: yeşil kısma bak."), pause=0.5))
b += qcm(7, 0, "Un kilo ___ pommes, s'il vous plaît.", ["des", "de", "les"], 1, ("Miktar + « de »: un kilo de pommes", "Doğru cevap ikinci şık. Miktardan sonra tanımlık gelmez."),
         TR("Sıra sende. Boşluğa hangisi gelir?"), label="Sıra sende", qsize=66)
SCENES.append(scene("Dilbilgisi: karşılaştırma ve ödeme", b, fit=False))

# =============================================================================
# 9. Mağazada : une scène d'achat à suivre dans la vitrine, puis le total à trouver
# =============================================================================
b = [beat(clear=True, show=[T("f1", "Şimdi hepsini bir arada görelim.", CX, 300, size=60, font="regular", color="soft", align="center"),
                            T("f2", "Mağazada: [dinle ve takip et|hl]", CX, 400, size=100, font="display", align="center"),
                            T("f3", "Bir müşteri alışveriş yapıyor. Sonunda toplamı sen bulacaksın.", CX, 600, size=46, font="regular", color="soft", align="center")],
          say=TR("Şimdi öğrendiklerimizi bir arada görelim. Bir müşteri alışveriş yapıyor. Dinle ve vitrinde takip et. Sonunda toplamı sen bulacaksın."), pause=0.3),
     beat(clear=True, show=shop() + panel("La vitrine", "Sekiz ürün, sekiz fiyat.", wsize=84), say=TR("İşte vitrin: sekiz ürün ve fiyatları."), pause=0.4),
     beat(hide=PANEL_IDS, show=shop(["chemise"]) + panel("cette\nchemise", "bu gömlek · dişil", "Je voudrais [cette|no] chemise blanc[he|no], s'il vous plaît.", "Bu beyaz gömleği istiyorum, lütfen.", "Müşteri · 1 / 3", wsize=84),
          say=[FR("Bonjour. Je voudrais cette chemise blanche, s'il vous plaît.", "M1"), TR("Bu beyaz gömleği istiyor. İsim dişil: iki kelimenin de sonu değişti.")], pause=0.3),
     beat(hide=PANEL_IDS, show=shop(["chemise", "chaussures"]) + panel("ces\nchaussures", "bu ayakkabılar · çoğul", "Et [ces|ok] chaussures, elles coût[ent|ok] combien ?", "Peki bu ayakkabılar ne kadar?", "Müşteri · 2 / 3", wsize=76),
          say=[FR("Et ces chaussures, elles coûtent combien ?", "M1"), FR("Elles coûtent cinquante-cinq euros.", "F1"), TR("Ayakkabıların fiyatını soruyor: elli beş euro.")], pause=0.3),
     beat(hide=PANEL_IDS, show=shop(["chemise", "jupe"]) + panel("trop cher", "fazla pahalı", "C'est [trop cher|no]. Je prends la chemise et [ça|gold].", "Fazla pahalı. Gömleği ve şunu alıyorum.", "Müşteri · 3 / 3", wsize=84),
          say=[FR("C'est trop cher. Je prends la chemise et ça.", "M1"), TR("Ayakkabılar fazla pahalı. Gömleği alıyor ve yeşil eteği parmağıyla gösteriyor: adını bilmiyor.")], pause=0.3),
     beat(hide=PANEL_IDS, show=shop(["chemise", "jupe"]) + [
         Badge("q", "Sıra sende", PXR, 150, size=30, fill="gold", color="ink"), T("qq", "Ça fait\ncombien ?", PXR, 220, size=76, font="display", line_h=1.1),
         Box("o1", PXR, 420, 630, 104, fill="card", radius=22, width=3), T("o1t", "[A|hl]   55 €", PXR + 35, 444, size=46),
         Box("o2", PXR, 544, 630, 104, fill="card", radius=22, width=3), T("o2t", "[B|hl]   65 €", PXR + 35, 568, size=46),
         Box("o3", PXR, 668, 630, 104, fill="card", radius=22, width=3), T("o3t", "[C|hl]   75 €", PXR + 35, 692, size=46)],
          say=[FR("Ça fait combien ?", "M1"), TR("Toplam ne kadar? Vitrine bak ve hesapla.")], pause=0.2),
     beat(show=Countdown("cd", PXR, 830, 520, seconds=5), wait=WAIT + 1),
     beat(hide=["cd"], show=[Box("o2", PXR, 544, 630, 104, fill="ok_tint", outline="ok", radius=22, width=6), T("o2t", "[B   65 €|ok]", PXR + 35, 568, size=46),
                             T("o1t", "[A   55 €|soft]", PXR + 35, 444, size=46), T("o3t", "[C   75 €|soft]", PXR + 35, 692, size=46),
                             T("ex", "30 € + 35 € = [65 €|ok]", PXR, 820, size=50)],
          say=[FR("Ça fait soixante-cinq euros.", "F1"), TR("Doğru cevap B. Gömlek otuz, etek otuz beş: toplam altmış beş euro. Bravo!")], pause=0.6)]
SCENES.append(scene("Mağazada", b, fit=False))

# =============================================================================
# 10. Kelimeler : les vêtements dans la vitrine, six mots clés, puis les autres sur un écran
# =============================================================================
CLOTHES = [("pantalon", "Je voudrais un [pantalon|hl] noir.", "Siyah bir pantolon istiyorum."), ("chemise", "Cette [chemise|hl] est belle.", "Bu gömlek güzel."),
           ("pull", "Ce [pull|hl] est trop petit.", "Bu kazak fazla küçük."), ("robe", "Je voudrais essayer cette [robe|hl].", "Bu elbiseyi denemek istiyorum."),
           ("jupe", "Cette [jupe|hl] est jolie.", "Bu etek güzel."), ("veste", "Je porte une [veste|hl] bleue.", "Mavi bir ceket giyiyorum."),
           ("manteau", "Mon [manteau|hl] est trop petit.", "Paltom fazla küçük."), ("chaussures", "Ces [chaussures|hl] sont chères.", "Bu ayakkabılar pahalı.")]
b = [beat(clear=True, show=chapter(8, "Giysiler vitrinde, sonra altı anahtar kelime."), say=TR("Sekizinci bölüm: kelimeler. Önce giysiler. Her kelimeyi dinle ve tekrar et."), pause=0.2)]
for i, (k, ex, extr) in enumerate(CLOTHES):
    w, tr, p, n = SHOP[k]
    b.append(beat(clear=(i == 0), hide=[] if i == 0 else PANEL_IDS, show=shop([k], prices=False) + panel(w, tr, ex, extr, f"Giysiler · {i + 1} / {len(CLOTHES)}", wsize=84 if len(w) < 12 else 66),
                  say=[V(n), TR(tr), V(n, ex=True), TR(extr)], lead=0.05, pause=0.3))
KEYS = [("le prix", "fiyat", 6, "Quel est [le prix|hl] de ce sac ?", "Bu çantanın fiyatı nedir?"), ("cher · chère", "pahalı", 7, "Cette robe est [chère|hl].", "Bu elbise pahalı."),
        ("la taille", "beden", 25, "Quelle est votre [taille|hl] ?", "Bedeniniz nedir?"), ("la couleur", "renk", 28, "Vous avez une autre [couleur|hl] ?", "Başka bir renk var mı?"),
        ("le sac", "çanta", 24, "Je cherche un [sac|hl].", "Bir çanta arıyorum."), ("la carte bancaire", "banka kartı", 11, "Je peux payer par [carte bancaire|hl] ?", "Banka kartıyla ödeyebilir miyim?")]
for i, (w, tr, n, ex, extr) in enumerate(KEYS):
    x, y = 120 + (i % 3) * 570, 270 + (i // 3) * 360
    b.append(beat(clear=(i == 0), show=([T("title", "Altı anahtar kelime", 120, 125, size=66, font="display")] if i == 0 else []) + [
        Box(f"kb{i}", x, y, 540, 330, fill="card", outline="brand", radius=28, width=3),
        T(f"kw{i}", w, x + 36, y + 28, size=58 if len(w) < 13 else 46, font="display", color="brand"), T(f"kt{i}", tr, x + 36, y + 106, size=38, font="regular", color="soft"),
        T(f"ke{i}", ex, x + 36, y + 180, size=34, max_w=470, line_h=1.25), T(f"kr{i}", extr, x + 36, y + 276, size=26, font="regular", color="soft", max_w=470)],
                  say=[V(n), TR(tr), V(n, ex=True), TR(extr)], lead=0.05, pause=0.25))
REST = [("moins cher", "daha ucuz"), ("en espèces", "nakit"), ("la monnaie", "para üstü"), ("l'écharpe", "atkı"), ("essayer", "denemek"), ("porter", "giymek"),
        ("vert · verte", "yeşil"), ("le mètre", "metre"), ("le cadeau", "hediye"), ("l'ordinateur", "bilgisayar"), ("le stylo", "kalem"), ("le cahier", "defter"), ("les clés", "anahtarlar")]
els = title(f"Öğrenmen tavsiye edilir: {len(REST)} kelime daha", "Bütün kelimeler, örnek cümleleri ve sesleriyle sitemizde:  kolayfransizca.app")
for i, (w, tr) in enumerate(REST):
    c, r = i % 4, i // 4
    x, y = 120 + c * 425, 300 + r * 150
    els += [Box(f"rb{i}", x, y, 405, 128, fill="card", outline="line", radius=20), T(f"rw{i}", w, x + 24, y + 16, size=40, color="brand_dark"),
            T(f"rt{i}", tr, x + 24, y + 72, size=32, font="regular", color="soft")]
b.append(beat(clear=True, show=els, say=TR("Bu modülün diğer kelimeleri de ekranda. Bütün kelimeleri örnek cümleleri ve sesleriyle birlikte sitemizde bulabilirsin."), pause=2.0))
b.append(beat(clear=True, show=note("Giysileri üzerindekilerle ezberle.\nHer sabah giyinirken ne giydiğini söyle:\n« Je porte un pantalon noir et une chemise blanche. »\n"
                                    "Rengi ismin arkasına koymayı böylece unutmazsın."),
              say=TR("Benim tavsiyem: giysileri üzerindekilerle ezberle. Her sabah giyinirken ne giydiğini Fransızca söyle. Rengi ismin arkasına koymayı böylece hiç unutmazsın."), pause=0.6))
SCENES.append(scene("Kelimeler", b, fit=False))

# =============================================================================
# 11. Telaffuz : la nasale [ɛ̃] et la liaison dans les prix
# =============================================================================
IN = [("v[in|hl]gt", "yirmi", 1), ("le p[ain|hl]", "ekmek", 4), ("comb[ien|hl]", "ne kadar", 5), ("le magas[in|hl]", "mağaza", 3)]
b = [beat(clear=True, show=chapter(9, "Fiyat sorarken hep duyacağın bir ses."), say=TR("Dokuzuncu bölüm: telaffuz. Fiyat sorarken hep duyacağın bir genizden ses var."), pause=0.2),
     beat(clear=True, show=title("Üçüncü genizden ses") + [
         Box("o1", 120, 260, 820, 300, fill="tint", outline="brand", radius=28, width=3), T("o1a", "[in|hl] · [ain|hl] · [ien|hl]", 530, 290, size=84, font="display", align="center"),
         T("o1b", "Dudaklar gergin, gülümser gibi", 530, 450, size=40, font="regular", color="soft", align="center"),
         Box("o2", 980, 260, 820, 300, fill="gold_tint", outline="gold", radius=28, width=3), T("o2a", "[an|gold] · [en|gold]", 1390, 290, size=96, font="display", align="center"),
         T("o2b", "Ağız açık (5. modülde gördün)", 1390, 450, size=40, font="regular", color="soft", align="center")],
          say=TR("Bu harf gruplarında n harfi okunmaz, ses genizden çıkar. Dudaklarını gülümser gibi ger. Beşinci modüldeki sesten farkı budur: onda ağız açıktı."), pause=0.3)]
for i, (w, tr, n) in enumerate(IN):
    x, y = (330 if i % 2 == 0 else 730), 620 + (i // 2) * 150
    b.append(beat(show=[T(f"in{i}", w, x, y, size=60, align="center"), T(f"it{i}", tr, x, y + 78, size=30, font="regular", color="soft", align="center")], say=TT(n), lead=0.05, pause=0.25))
b.append(beat(show=[T("p1", "v[in|hl]gt", 1210, 620, size=84, font="display", align="center"), T("p1t", "yirmi", 1210, 730, size=36, font="regular", color="soft", align="center"),
                    T("pv", "≠", 1390, 630, size=80, font="display", color="soft", align="center"),
                    T("p2", "v[en|gold]t", 1570, 620, size=84, font="display", align="center"), T("p2t", "rüzgâr", 1570, 730, size=36, font="regular", color="soft", align="center")],
              say=[TR("Bu iki kelimede tek fark genizden sestir. Dinle."), TT(14), TT(15), TT(14), TT(15)], pause=0.4))
LI = [("deu[x|no]", "euros", "z", 8), ("di[x|no]", "euros", "z", 11), ("ving[t|no]", "euros", "t", 12)]
b.append(beat(clear=True, show=title("Fiyatlarda bağlama", "« euros » sesli harfle başlar: sayının son harfi okunur ve ona bağlanır.") + term("la liaison", "bağlama"),
              say=TR("Bir şey daha. Para birimi sesli harfle başlar. Bu yüzden sayının normalde okunmayan son harfi okunur ve sonraki kelimeye bağlanır. Buna bağlama denir, Fransızcası « la liaison »."), pause=0.2))
for i, (a, e, snd, n) in enumerate(LI):
    y = 330 + i * 190
    b.append(beat(show=[T(f"la{i}", a, 620, y, size=96, font="display", align="right"), T(f"lb{i}", e, 700, y, size=96, font="display"),
                        Arrow(f"lr{i}", (600, y + 130), (720, y + 130), color="no", width=6, curve=-0.5, head=18),
                        Badge(f"ls{i}", f"[{snd}] sesi", 1200, y + 30, size=40, fill="no_tint", color="no")], say=[TT(n), TT(n)], lead=0.05, pause=0.3))
b += qcm(8, 0, "Dinle: hangi kelime?", ["vingt", "vent"], 1, ("« vent »: ağız açık söylenir", "Doğru cevap ikinci şık. Ağız açık söylendi."),
         [TR("Sıra sende. Hangi kelimeyi duyuyorsun?"), TT(15), TT(15)], label="Sıra sende", qsize=72)
SCENES.append(scene("Telaffuz", b, fit=False))

# =============================================================================
# 12. DELF köşesi : le jeu de rôle d'achat de l'épreuve orale
# =============================================================================
STEPS = [("1", "Selam ver", "Bonjour madame !", FR("Bonjour madame !", "M1")), ("2", "Ürünü iste", "[Je voudrais|hl] un kilo de pommes, s'il vous plaît.", FR("Je voudrais un kilo de pommes, s'il vous plaît.", "M1")),
         ("3", "Fiyatı sor", "Ça fait [combien|hl] ?", G(8)), ("4", "Öde", "[Voilà|hl].", FR("Voilà.", "M1")), ("5", "Teşekkür et", "[Merci, au revoir|hl] !", FR("Merci, au revoir !", "M1"))]
b = [beat(clear=True, show=chapter(10, "Sözlü sınavın üçüncü bölümü: alışveriş canlandırması."),
          say=TR("Son bölüm: DELF köşesi. Sözlü sınavın üçüncü bölümünde bir alışveriş canlandırırsın. Sınav görevlisi satıcıdır, sen müşterisin."), pause=0.2),
     beat(clear=True, show=title("Sınavda ne olur?", "Önüne ürün resimleri ve oyun parası konur. Yaklaşık iki dakika sürer.")
          + [Img(f"dx{i}", IMG + f"items/{k}.webp", 1240 + (i % 2) * 280, 300 + (i // 2) * 290, 250, 250, radius=0) for i, k in enumerate(["pull", "chaussures", "robe", "pantalon"])],
          say=TR("Önüne ürün resimleri ve oyun parası konur. Bir ya da iki ürün alırsın. Beş adımı sırayla yaparsan tam puan alırsın."), pause=0.2)]
for i, (num, head, french, audio) in enumerate(STEPS):
    y = 300 + i * 132
    b.append(beat(show=[Dot(f"sn{i}", 170, y + 46, r=40, fill="gold", outline=None, width=0, label=num), T(f"sh{i}", head, 240, y + 14, size=46, font="display"),
                        T(f"sf{i}", french, 560, y + 18, size=40, max_w=640)], say=[TR(head + "."), audio], lead=0.05, pause=0.2))
b.append(beat(clear=True, show=note("Satıcıya her zaman « vous » ile konuş.\nBir kelimeyi bilmiyorsan resmi göster ve küçük kelimeyi kullan:\n« Je voudrais ça, s'il vous plaît. »"),
              say=TR("Benim tavsiyem: satıcıya her zaman siz diye hitap et. Ve bir kelimeyi bilmiyorsan panik yapma: resmi göster ve bugün öğrendiğin küçük kelimeyi kullan."), pause=0.6))
# mini simulation : l'examinatrice parle, l'élève répond, puis la réponse modèle
SIMS = [("Bonjour ! Je peux vous aider ?", "Selam ver ve bir şişe su iste.", "Bonjour. [Je voudrais|hl] une bouteille d'eau, s'il vous plaît.", "Bonjour. Je voudrais une bouteille d'eau, s'il vous plaît."),
        ("Voilà. Ça fait un euro cinquante.", "Parayı ver, teşekkür et ve vedalaş.", "[Voilà|hl]. [Merci, au revoir|hl] !", "Voilà. Merci, au revoir !")]
b.append(beat(clear=True, show=[T("s0", "Şimdi sen müşterisin", CX, 330, size=100, font="display", align="center"),
                                T("s1", "Satıcıyı dinle, yüksek sesle cevap ver, sonra örnek cevabı dinle.", CX, 520, size=46, font="regular", color="soft", align="center")],
              say=TR("Şimdi sen müşterisin. Satıcıyı dinle, yüksek sesle cevap ver, sonra örnek cevabı dinle."), pause=0.3))
for i, (seller, task, model, msay) in enumerate(SIMS):
    b.append(beat(clear=True, show=portrait("sv", "La vendeuse", 1700, 180, 130) + [
        Badge("sl", f"Canlandırma · {i + 1} / {len(SIMS)}", 120, 130, size=34, fill="gold", color="ink"),
        Bubble("sb", 420, 180, 1240, 150, "right", fill="tint", outline="brand"), T("st", seller, 470, 220, size=54),
        T("sk", task, CX, 430, size=50, align="center", color="soft", font="regular")], say=[FR(seller, "F1")], pause=0.2))
    b.append(beat(show=Countdown("cd", 560, 540, 800, label="Şimdi sen söyle", seconds=5), wait=WAIT + 1))
    b.append(beat(hide=["cd"], show=portrait("se", "Emre", 90, 640, 130) + [Bubble("eb", 260, 640, 1400, 190, "left", fill="gold_tint", outline="gold"),
                                                                       T("et", model, 310, 680, size=50, max_w=1300), Badge("el", "Örnek cevap", 260, 856, size=32, fill="ok_tint", color="ok")],
                  say=[FR(msay, "M1")], pause=0.6))
SCENES.append(scene("DELF köşesi", b, fit=False))

# =============================================================================
# 13. Mini test : d'abord les réponses aux deux questions du début, puis cinq questions
# =============================================================================
b = [beat(clear=True, show=title("Baştaki iki soru: cevapları artık biliyorsun") + [
        Box("a1", 120, 270, 1680, 300, fill="card", outline="brand", radius=32, width=3), Badge("a1n", "Soru 1", 160, 300, size=32, fill="gold", color="ink"),
        T("a1q", "Adını bilmediğin şeyi nasıl satın alırsın?", 160, 370, size=46, font="regular", color="soft"),
        T("a1a", "Göster ve söyle:  Je voudrais [ça|gold], s'il vous plaît.", 160, 450, size=60, font="display")],
          say=[TR("Dersin başında iki soru sormuştum. Birincisi: adını bilmediğin şeyi nasıl satın alırsın? Cevap: gösterirsin ve şunu söylersin."), G(25)], pause=0.3),
     beat(show=[Box("a2", 120, 600, 1680, 330, fill="card", outline="brand", radius=32, width=3), Badge("a2n", "Soru 2", 160, 630, size=32, fill="gold", color="ink"),
                T("a2q", "« Bu ne kadar? » kaç farklı şekilde sorulur?", 160, 700, size=46, font="regular", color="soft"),
                T("a2a", "Ça coûte [combien|hl] ?  ·  C'est [combien|hl] ?\n[Combien|hl] coûte... ?  ·  Quel est [le prix|gold] de... ?", 160, 770, size=48, font="display", line_h=1.35)],
          say=TR("İkincisi: bu ne kadar sorusu kaç farklı şekilde sorulur? Cevap: en az dört şekilde. Hepsini bugün öğrendin."), pause=0.6)]
QUIZ = [("___ robe est jolie.", ["Ce", "Cette", "Ces"], 1, ("la robe: dişil → « cette robe »", "Doğru cevap ikinci şık. İsim dişil."), "Boşluğa ne gelir?"),
        ("Une chemise ___.", ["blanc", "blanche", "blancs"], 1, ("blanc düzensizdir: dişili « blanche »", "Doğru cevap ikinci şık. Bu renk düzensizdir."), "Boşluğa ne gelir?"),
        ("Dinle: toplam ne kadar?", ["62,15 €", "72,50 €", "62,50 €"], 2, ("« soixante-deux euros cinquante » = 62,50 €", "Doğru cevap üçüncü şık: altmış iki euro elli."), "Dinle. Toplam ne kadar?"),
        ("Tanımadığın bir satıcıya:", ["Je veux ce sac.", "Je voudrais ce sac, s'il vous plaît.", "Tu as ce sac ?"], 1, ("« Je voudrais... s'il vous plaît. »", "Doğru cevap ikinci şık: kibar kalıp."), "Hangisi doğru?"),
        ("Kasada toplamı soruyorsun:", ["Ça fait combien ?", "Qu'est-ce que c'est ?", "Quelle taille ?"], 0, ("Toplam: « Ça fait combien ? »", "Doğru cevap birinci şık."), "Hangisi doğru?")]
b.append(beat(clear=True, show=[T("mt1", "Mini test", CX, 330, size=120, font="display", align="center"), T("mt2", "5 soru · hızlı cevap ver", CX, 520, size=48, font="regular", color="soft", align="center")],
              say=TR("Son olarak beş hızlı soru. Çabuk cevap ver."), pause=0.3))
for i, (qq, opts, ok, expl, qs) in enumerate(QUIZ, 1):
    b += qcm(i, len(QUIZ), qq, opts, ok, expl, [TR(qs)] + ([F("quiz/m7-q03.mp3"), F("quiz/m7-q03.mp3")] if qq.startswith("Dinle") else []), qsize=64)
SCENES.append(scene("Mini test", b, fit=False))

# =============================================================================
# 14. Kapanış : trois choses à retenir
# =============================================================================
els = title("Üç şey hatırla")
for c in cards3([("1", "Fiyat sor", "Ça coûte [combien|hl] ?\nÇa fait [combien|hl] ?"), ("2", "Kibarca iste", "[Je voudrais|hl] ce pull.\n[Je voudrais|hl] ça."),
                 ("3", "Tarif et", "une robe noir[e|no]\n[cette|no] robe · [ces|ok] pulls")], y=260, h=480):
    els += c
SCENES.append(scene("Kapanış", [
    beat(clear=True, show=els, say=TR("Bugünden üç şey hatırla. Bir: fiyat sormak ve toplamı sormak. İki: kibarca istemek ve adını bilmediğin şeyi göstermek. "
                                      "Üç: rengi ismin arkasına koymak ve isme uydurmak."), pause=0.4),
    beat(show=Badge("url", "Alıştırmalar, mağaza oyunu, modül testi ve PDF özet fişi:  kolayfransizca.app", CX, 820, size=36, fill="gold", color="ink", align="center"),
         say=TR("Şimdi sıra alıştırmalarda. Sitemizde bu modülün alıştırmalarını, mağaza oyununu, DELF tarzı testi ve PDF özet fişini ücretsiz olarak bulabilirsin."), pause=0.5),
    beat(clear=True, show=[T("t1", "Bu kurs tamamen [ücretsiz|hl].", CX, 300, size=72, font="display", align="center"),
                           T("t2", "Teşekkür etmenin en güzel yolu: kanala abone olmak.", CX, 430, size=46, align="center"),
                           Badge("nx", "Sonraki ders: Modül 8 · Restoranda", CX, 620, size=38, fill="tint", color="brand_dark", align="center")],
         say=TR("Bu kurs tamamen ücretsiz. Bana teşekkür etmenin en güzel yolu kanala abone olmak. Sekizinci modülde restoranda sipariş vermeyi öğreneceğiz. Görüşmek üzere!"), pause=1.5),
], fit=False))
