# -*- coding: utf-8 -*-
"""
Scénario de la vidéo du module 1 : « Selamlaşma ve tanışma ».
Lancement : python video_engine.py modul_01_video.py

Pour un autre module, copier ce fichier, changer MODULE, VOC, OKUNUS et le texte des scènes.
Rappels de balisage du texte : [segment|style] avec style = hl, hl2, gold, mark, ok, no, mute, soft
FR("texte", "M1") retrouve automatiquement le fichier audio du site qui porte ce texte.
"""
from video_engine import T, Box, Img, Arrow, Badge, Countdown, TR, FR, beat, scene

MODULE = {"slug": "modul-1-selamlasma-tanisma", "label": "Modül 1", "url": "kolayfransizca.app"}
A = "a1/audio/m01/"
IMG = "a1/img/m01/"
CX = 960  # centre horizontal

# -----------------------------------------------------------------------------
# Données
# -----------------------------------------------------------------------------
DIALOGUE = [
    ("Elif", "Bonjour ! Je m'appelle Elif. Et toi, tu t'appelles comment ?", "Merhaba! Benim adım Elif. Ya sen, senin adın ne?"),
    ("Emre", "Salut ! Moi, je m'appelle Emre.", "Selam! Benim adım Emre."),
    ("Elif", "Pardon ? Tu peux répéter, s'il te plaît ?", "Pardon? Tekrar edebilir misin, lütfen?"),
    ("Emre", "Emre. E, M, R, E.", "Emre. E, M, R, E."),
    ("Elif", "Ah, Emre ! Enchantée.", "Ah, Emre! Memnun oldum."),
    ("Emre", "Enchanté. Ça va ?", "Memnun oldum. Nasılsın?"),
    ("Elif", "Ça va très bien, merci. Et toi ?", "Çok iyiyim, teşekkürler. Ya sen?"),
    ("Emre", "Très bien. Voilà notre professeur, madame Martin.", "Çok iyi. İşte öğretmenimiz, Bayan Martin."),
    ("Mme Martin", "Bonjour à tous ! Vous êtes Elif et Emre ?", "Herkese merhaba! Siz Elif ve Emre misiniz?"),
    ("Elif", "Oui, madame. Bonjour !", "Evet, hanımefendi. Merhaba!"),
]

# (n° de fichier sur le site, mot, turc, exemple M, exemple F, traduction)  — « Mutlaka öğren » uniquement
VOC = [
    (1, "bonjour", "merhaba / günaydın", "Bonjour, madame.", "", "Merhaba, hanımefendi."),
    (2, "bonsoir", "iyi akşamlar", "Bonsoir, monsieur.", "", "İyi akşamlar, beyefendi."),
    (3, "salut", "selam", "Salut, Marie !", "", "Selam, Marie!"),
    (4, "au revoir", "hoşça kal / güle güle", "Au revoir et merci.", "", "Hoşça kalın ve teşekkürler."),
    (9, "merci", "teşekkürler", "Merci beaucoup.", "", "Çok teşekkürler."),
    (10, "s'il vous plaît", "lütfen (resmi)", "Votre nom, s'il vous plaît ?", "", "Adınız, lütfen?"),
    (12, "pardon", "pardon / affedersiniz", "Pardon, je ne comprends pas.", "", "Pardon, anlamıyorum."),
    (13, "excusez-moi", "affedersiniz", "Excusez-moi, vous êtes madame Martin ?", "", "Affedersiniz, siz Bayan Martin misiniz?"),
    (15, "oui", "evet", "Oui, c'est moi.", "", "Evet, benim."),
    (16, "non", "hayır", "Non, merci.", "", "Hayır, teşekkürler."),
    (17, "monsieur", "bey / beyefendi", "Bonjour, monsieur Dupont.", "", "Merhaba, Bay Dupont."),
    (18, "madame", "hanım / hanımefendi", "Au revoir, madame.", "", "Hoşça kalın, hanımefendi."),
    (19, "le nom", "soyad", "Mon nom, c'est Yılmaz.", "", "Soyadım Yılmaz."),
    (20, "le prénom", "ad", "Mon prénom, c'est Emre.", "Mon prénom, c'est Elif.", "Adım Emre. / Adım Elif."),
    (21, "je m'appelle", "benim adım...", "Je m'appelle Emre.", "Je m'appelle Elif.", "Benim adım Emre. / Benim adım Elif."),
    (22, "comment", "nasıl", "Tu t'appelles comment ?", "", "Adın ne?"),
    (23, "et toi ?", "ya sen?", "Je m'appelle Emre, et toi ?", "Je m'appelle Elif, et toi ?", "Benim adım Emre, ya senin? / Benim adım Elif, ya senin?"),
    (24, "et vous ?", "ya siz?", "Ça va bien, merci. Et vous ?", "", "İyiyim, teşekkürler. Ya siz?"),
    (25, "enchanté / enchantée", "memnun oldum", "Enchanté, madame.", "Enchantée, madame.", "Memnun oldum, hanımefendi."),
    (26, "ça va ?", "nasılsın? / iyi misin?", "Salut, ça va ?", "", "Selam, nasılsın?"),
    (27, "très bien", "çok iyi", "Ça va très bien, merci.", "", "Çok iyiyim, teşekkürler."),
    (28, "être", "olmak", "Je suis turc.", "Je suis turque.", "Türküm."),
    (30, "répéter", "tekrar etmek", "Vous pouvez répéter, s'il vous plaît ?", "", "Tekrar edebilir misiniz, lütfen?"),
    (31, "épeler", "harf harf söylemek", "Vous pouvez épeler votre nom ?", "", "Adınızı harf harf söyleyebilir misiniz?"),
    (34, "moi", "ben", "Moi, je m'appelle Emre.", "Moi, je m'appelle Elif.", "Ben, benim adım Emre. / Ben, benim adım Elif."),
    (35, "toi", "sen", "Et toi, tu t'appelles comment ?", "", "Ya sen, senin adın ne?"),
]

# Okunuş yaklaşık ; « ⁿ » = genizden söylenen ses (n tam okunmaz)
OKUNUS = {
    "bonjour": "bonjur", "bonsoir": "bonsuar", "salut": "salü", "au revoir": "o rövuar", "merci": "mersi",
    "s'il vous plaît": "sil vu ple", "pardon": "pardoⁿ", "excusez-moi": "eksküze mua", "oui": "vi", "non": "noⁿ",
    "monsieur": "mösyö", "madame": "madam", "le nom": "lö noⁿ", "le prénom": "lö prenoⁿ", "je m'appelle": "jö mapel",
    "comment": "komaⁿ", "et toi ?": "e tua", "et vous ?": "e vu", "enchanté / enchantée": "aⁿşaⁿte", "ça va ?": "sa va",
    "très bien": "tre biyeⁿ", "être": "etr", "répéter": "repete", "épeler": "eple", "moi": "mua", "toi": "tua",
}

ALPHABET = [("A", "a"), ("B", "be"), ("C", "se"), ("D", "de"), ("E", "ö"), ("F", "ef"), ("G", "je"), ("H", "aş"),
            ("I", "i"), ("J", "ji"), ("K", "ka"), ("L", "el"), ("M", "em"), ("N", "eⁿ"), ("O", "o"), ("P", "pe"),
            ("Q", "kü"), ("R", "er"), ("S", "es"), ("T", "te"), ("U", "ü"), ("V", "ve"), ("W", "dublö ve"),
            ("X", "iks"), ("Y", "igrek"), ("Z", "zed")]

# -----------------------------------------------------------------------------
# Petits gabarits réutilisables
# -----------------------------------------------------------------------------
def title(text, sub=None):
    els = [T("title", text, 120, 130, size=62, font="display")]
    if sub:
        els.append(T("sub", sub, 120, 222, size=32, font="regular", color="soft", max_w=1600))
    return els


def note(text, kind="tavsiye", y=820):
    lab = "Öğretmenin tavsiyesi" if kind == "tavsiye" else "Öğretmenin notu"
    fill = "gold_tint" if kind == "tavsiye" else "tint"
    return [Box("note_box", 120, y, 1680, 170, fill=fill, outline="gold" if kind == "tavsiye" else "brand", radius=22),
            T("note_lab", lab, 160, y + 26, size=28, color="gold_ink" if kind == "tavsiye" else "brand_dark"),
            T("note_txt", text, 160, y + 72, size=32, font="regular", max_w=1600)]


def hl_word(sentence, word):
    """Met le mot du vocabulaire en couleur dans la phrase d'exemple (si on le trouve)."""
    cands = [w.strip(" ?") for w in word.split("/")]
    low = sentence.lower()
    for c in sorted(cands, key=len, reverse=True):
        c = c.replace("le ", "") if c.startswith("le ") else c
        i = low.find(c.lower())
        if i >= 0 and c:
            return sentence[:i] + "[" + sentence[i:i + len(c)] + "|hl]" + sentence[i + len(c):]
    return sentence


def diff_mark(a, b, style="gold"):
    """Colore dans b ce qui diffère de a (ex. Enchanté -> Enchanté[e|gold])."""
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    j = 0
    while j < min(len(a), len(b)) - i and a[len(a) - 1 - j] == b[len(b) - 1 - j]:
        j += 1
    mid = b[i:len(b) - j]
    return b if not mid else b[:i] + f"[{mid}|{style}]" + b[len(b) - j:]


SCENES = []

# =============================================================================
# 1. Giriş
# =============================================================================
SCENES.append(scene("Giriş", [
    beat(show=[Badge("tag", "DELF A1 Hazırlık · Modül 1", 120, 250, size=30, fill="tint", color="brand_dark"),
               T("h1", "Fransızca selamlaşma\nve [tanışma|hl]", 120, 340, size=72, font="display", line_h=1.12),
               T("h1fr", "Saluer, se présenter", 120, 560, size=40, font="regular", color="soft"),
               Img("hero", IMG + "m01-hero.webp", 1100, 220, 700, 600, radius=32)],
         say=TR("Merhaba! Kolay Fransızca'nın DELF A1 hazırlık kursuna hoş geldin. Bu, birinci modül: selamlaşma ve tanışma.")),
    beat(clear=True, show=title("Bu derste neler öğreneceksin?"), say=TR("Bu derste neler öğreneceğiz?")),
    beat(show=T("o1", "•  Selam vermeyi ve vedalaşmayı", 140, 280, size=46), say=TR("Selam vermeyi ve vedalaşmayı,")),
    beat(show=T("o2", "•  Kendini tanıtmayı: « [tu|hl] » ve « [vous|hl] » farkı", 140, 380, size=46),
         say=TR("kendini tanıtmayı, tü ile vu arasındaki farkı,")),
    beat(show=T("o3", "•  Adını harf harf söylemeyi", 140, 480, size=46), say=TR("adını harf harf söylemeyi,")),
    beat(show=T("o4", "•  DELF sözlü sınavının [ilk bölümünü|hl]", 140, 580, size=46),
         say=TR("ve DELF sözlü sınavının ilk bölümüne hazırlanmayı öğreneceksin.")),
    beat(show=[Badge("url", "Alıştırmalar ve test:  kolayfransizca.app", 140, 720, size=36, fill="gold", color="ink")],
         say=TR("Bu dersin alıştırmaları, kelime testi ve modül testi ücretsiz olarak sitemizde seni bekliyor. Adresi ekranda görüyorsun."), pause=0.8),
]))

# =============================================================================
# 2. Diyalog
# =============================================================================
b = [beat(show=[Img("dimg", IMG + "m01-dialogue.webp", 480, 150, 960, 720, radius=32),
                Badge("pass", "1. dinleme · metin yok", CX, 900, size=32, fill="tint", color="brand_dark", align="center")],
          say=TR("Önce bir diyalog dinleyelim. Elif ve Emre, bir Fransızca kursunun ilk gününde tanışıyor. "
                 "İlk dinlemede metin yok. Sadece dinle ve ne anladığını düşün."), pause=0.8)]
for i, (who, fr, tr) in enumerate(DIALOGUE, 1):
    b.append(beat(show=Badge("pass", f"1. dinleme · {who} konuşuyor", CX, 900, size=32, fill="brand", color="white", align="center"),
                  say={"file": A + f"dialogue/m1-d{i:02d}.mp3"}, lead=0.1, pause=0.35))
b.append(beat(show=Badge("pass", "Ne anladın?", CX, 900, size=32, fill="gold", color="ink", align="center"),
              say=TR("Ne anladın? Şimdi metinle birlikte bir kez daha dinleyelim."), pause=0.6))
# 2e écoute : texte + traduction, 5 répliques par page
for page in (0, 1):
    for k in range(5):
        i = page * 5 + k
        show = [Img("dimg", IMG + "m01-dialogue.webp", 60, 170, 680, 510, radius=28),
                Badge("pass", "2. dinleme · metinle", 60, 720, size=30, fill="tint", color="brand_dark")]
        for kk in range(k + 1):
            j = page * 5 + kk
            who, fr, tr = DIALOGUE[j]
            y = 140 + kk * 172
            cur = kk == k
            show += [T(f"dw{kk}", who, 800, y + 4, size=26, color="brand" if cur else "mute"),
                     T(f"df{kk}", fr, 980, y, size=34, max_w=880, color="ink" if cur else "mute"),
                     T(f"dt{kk}", tr, 980, y + 92, size=27, font="regular", color="soft" if cur else "mute", max_w=880)]
        b.append(beat(clear=(k == 0), show=show, say={"file": A + f"dialogue/m1-d{i + 1:02d}.mp3"}, lead=0.15, pause=0.5))
# 3e passage : répéter
b.append(beat(clear=True, show=title("Sıra sende: dinle ve tekrar et"),
              say=TR("Şimdi sıra sende. Her cümleyi dinle, sonra yüksek sesle tekrar et."), pause=0.5))
for i, (who, fr, tr) in enumerate(DIALOGUE, 1):
    b.append(beat(clear=True, show=[Badge("who", who, CX, 200, size=32, fill="brand", color="white", align="center"),
                                    T("rf", fr, CX, 330, size=58, align="center", max_w=1600),
                                    T("rt", tr, CX, 560, size=36, font="regular", color="soft", align="center", max_w=1500)],
                  say={"file": A + f"dialogue/m1-d{i:02d}.mp3"}, pause=0.2))
    b.append(beat(show=[Badge("rep", "Tekrar et", CX, 700, size=34, fill="gold", color="ink", align="center"),
                        Countdown("cd", 560, 800, 800)], repeat=1.6))
SCENES.append(scene("Diyalog", b))

# =============================================================================
# 3. Dilbilgisi : tu / vous
# =============================================================================
SCENES.append(scene("Dilbilgisi: tu ve vous", [
    beat(show=title("« [Tu|hl] » mu, « [vous|hl] » mu?"),
         say=TR("Fransızcada, Türkçedeki sen ve siz ayrımının aynısı var.")),
    beat(show=[Img("itu", IMG + "m01-tu.webp", 120, 270, 380, 380, radius=28),
               T("tu1", "[Tu|hl] = sen", 540, 290, size=60, font="display"),
               T("tu2", "arkadaş, aile, çocuk, yaşıt", 540, 385, size=32, font="regular", color="soft")],
         say=TR("Tü, sen demektir. Arkadaşına, ailene, çocuklara ve yaşıtlarına tü dersin.")),
    beat(show=[T("tu3", "Salut ! [Tu|hl] t'appelles comment ?", 540, 480, size=40, max_w=1240),
               T("tu4", "Selam! Adın ne?", 540, 545, size=30, font="regular", color="soft")],
         say=FR("Salut ! Tu t'appelles comment ?")),
    beat(show=[Img("ivous", IMG + "m01-vous.webp", 120, 680, 380, 340, radius=28),
               T("vo1", "[Vous|hl] = siz", 540, 690, size=60, font="display"),
               T("vo2", "tanımadığın kişi, yaşça büyük, resmi durum", 540, 785, size=32, font="regular", color="soft")],
         say=TR("Vu ise siz demektir. Tanımadığın kişilere, yaşça büyüklere ve resmi durumlarda vu kullanırsın.")),
    beat(show=[T("vo3", "Bonjour ! [Vous|hl] vous appelez comment ?", 540, 870, size=40, max_w=1240),
               T("vo4", "Merhaba! Adınız ne?", 540, 935, size=30, font="regular", color="soft")],
         say=FR("Bonjour ! Vous vous appelez comment ?")),
    beat(clear=True, show=title("« [Tu|hl] » mu, « [vous|hl] » mu?") + note(
        "Emin değilsen her zaman « vous » kullan. Karşındaki kişi isterse sana « tu » demeni söyler.", y=360),
         say=TR("Benim tavsiyem şu: emin değilsen her zaman vu kullan. Karşındaki kişi isterse sana tü demeni söyler."), pause=0.8),
]))

# =============================================================================
# 4. Dilbilgisi : être
# =============================================================================
ETRE = [("je [suis|hl]", "je suis", "jö süi", "ben ...-im"), ("tu [es|hl]", "tu es", "tü e", "sen ...-sin"),
        ("il / elle [est|hl]", "il est, elle est", "il e / el e", "o ...-dir"), ("nous [sommes|hl]", "nous sommes", "nu som", "biz ...-iz"),
        ("vous [êtes|hl]", "vous êtes", "vu zet", "siz ...-siniz"), ("ils / elles [sont|hl]", "ils sont, elles sont", "il soⁿ / el soⁿ", "onlar ...-dirler")]
b = [beat(show=title("[être|hl] = olmak", "Türkçede « öğretmenim » derken -im ekini kullanırız. Fransızcada bunun yerine « être » fiili kullanılır."),
          say=TR("Şimdi en önemli fiillerden birini görelim: etr, yani olmak. Türkçede öğretmenim derken im ekini kullanırız. "
                 "Fransızcada ise bunun yerine etr fiili kullanılır."), pause=0.6)]
for i, (mk, txt, ok, tr) in enumerate(ETRE):
    y = 320 + i * 100
    b.append(beat(show=[T(f"e{i}", mk, 200, y, size=50),
                        Badge(f"eo{i}", ok, 760, y - 2, size=30, fill="tint", color="brand_dark"),
                        T(f"et{i}", tr, 1120, y + 4, size=36, font="regular", color="soft")],
                  say=FR(txt), lead=0.15, pause=0.5))
b.append(beat(show=[Badge("irr", "Düzensiz fiil: ezberle!", 1340, 250, size=30, fill="gold", color="ink"),
                    Arrow("ar1", {"id": "irr", "side": "left"}, {"id": "e0", "side": "right"}, curve=-40),
                    Arrow("ar2", {"id": "irr", "side": "bottom"}, {"id": "e5", "side": "right"}, curve=60)],
              say=TR("Dikkat: etr düzensiz bir fiildir. Her kişi için ayrı bir şekli var, bu yüzden bu tabloyu ezberlemen gerekiyor."), pause=0.6))
b.append(beat(hide=["irr", "ar1", "ar2"],
              show=[T("e4", "vous [ê|gold]tes", 200, 720, size=50),
                    Arrow("ar3", (1000, 980), {"id": "eo4", "side": "bottom"}, curve=-60),
                    T("lia", "vou[s|gold] + [ê|gold]tes → « vu [z|gold]et »", 1000, 960, size=34)],
              say=TR("Bir ayrıntı: vu zet derken, vu kelimesinin sonundaki okunmayan s harfi, sonraki sesli harfle birleşir ve z gibi okunur. "
                     "Buna liyezon denir."), pause=0.8))
SCENES.append(scene("Dilbilgisi: être", b))

# =============================================================================
# 5. Dilbilgisi : s'appeler
# =============================================================================
APP = [("je [m'|gold]appelle", "je m'appelle", "jö mapel", "benim adım"), ("tu [t'|gold]appelles", "tu t'appelles", "tü tapel", "senin adın"),
       ("il / elle [s'|gold]appelle", "il s'appelle, elle s'appelle", "il sapel", "onun adı"),
       ("nous [nous|gold] appelons", "nous nous appelons", "nu nuzaploⁿ", "bizim adımız"),
       ("vous [vous|gold] appelez", "vous vous appelez", "vu vuzaple", "sizin adınız"),
       ("ils / elles [s'|gold]appellent", "ils s'appellent, elles s'appellent", "il sapel", "onların adı")]
b = [beat(show=title("[s'appeler|hl] = adı ... olmak", "Kendini tanıtmak için bu fiili kullanırız."),
          say=TR("Kendini tanıtmak için saple fiilini kullanırız. Kelime anlamı, kendini çağırmak gibidir."), pause=0.5)]
for i, (mk, txt, ok, tr) in enumerate(APP):
    y = 320 + i * 100
    b.append(beat(show=[T(f"a{i}", mk.replace("[", "").replace("|gold]", ""), 200, y, size=50),
                        Badge(f"ao{i}", ok, 860, y - 2, size=30, fill="tint", color="brand_dark"),
                        T(f"at{i}", tr, 1260, y + 4, size=36, font="regular", color="soft")],
                  say=FR(txt), lead=0.15, pause=0.5))
b.append(beat(show=[T(f"a{i}", mk, 200, 320 + i * 100, size=50) for i, (mk, _, _, _) in enumerate(APP)],
              say=TR("Fiilin önündeki küçük kelime kişiye göre değişir: jö ile mö, tü ile tö, il ile sö. "
                     "Sesli harften önce bunlar kısalır ve kesme işaretiyle yazılır."), pause=0.6))
b.append(beat(show=[T("a5", "ils / elles [s'|gold]appel[lent|mute]", 200, 820, size=50),
                    Badge("okm", "okunmaz", 1500, 960, size=30, fill="no", color="white"),
                    Arrow("ar4", {"id": "okm", "side": "top"}, {"id": "a5", "char": -2, "side": "bottom"}, color="no", curve=40)],
              say=TR("Bir de şuna dikkat et: çoğul hâlin sonundaki e, n ve t harfleri okunmaz. "
                     "Bu yüzden tekil ve çoğul hâl aynı okunur: il sapel."), pause=0.6))
b.append(beat(clear=True, show=title("[s'appeler|hl] = adı ... olmak") + note(
    "« Je m'appelle » kalıbını şimdilik olduğu gibi ezberle. Bu fiilin kuralını 5. modülde ayrıntılı olarak göreceğiz.", kind="not", y=360),
              say=TR("Şimdilik jö mapel kalıbını olduğu gibi ezberle. Bu fiilin kuralını beşinci modülde ayrıntılı olarak göreceğiz."), pause=0.8))
SCENES.append(scene("Dilbilgisi: s'appeler", b))

# =============================================================================
# 6. Accord de l'adjectif
# =============================================================================
SCENES.append(scene("Sıfatın dişil hali", [
    beat(show=title("Sıfat, anlattığı kişiye uyar"),
         say=TR("Fransızcada sıfat, anlattığı kişinin cinsiyetine göre değişir. Türkçede böyle bir şey yok, o yüzden dikkatli dinle."), pause=0.5),
    beat(show=[Badge("lm", "Erkek", 200, 330, size=30, fill="tint", color="brand_dark"),
               T("c1", "Je suis conten[t|mute]", 420, 320, size=64)],
         say=[TR("Bir erkek, jö süi konton der. Sondaki t okunmaz."), FR("Je suis content.", "M1")]),
    beat(show=[Badge("lf", "Kadın", 200, 490, size=30, fill="gold", color="ink"),
               T("c2", "Je suis conten[t|hl][e|gold]", 420, 480, size=64),
               Badge("pe", "+ e", 1300, 400, size=34, fill="gold", color="ink"),
               Arrow("ar5", {"id": "pe", "side": "bottom"}, {"id": "c2", "char": -1, "side": "top"}, curve=-30)],
         say=[TR("Bir kadın ise sona bir e ekler. Bu e sayesinde t harfi artık okunur: jö süi kontont."), FR("Je suis contente.", "F1")]),
    beat(clear=True, show=title("Sıfat, anlattığı kişiye uyar") + [
        Badge("lm", "Erkek", 200, 330, size=30, fill="tint", color="brand_dark"), T("c1", "Enchant[é|hl] !", 420, 320, size=64),
        Badge("lf", "Kadın", 200, 490, size=30, fill="gold", color="ink"), T("c2", "Enchant[é|hl][e|gold] !", 420, 480, size=64),
        Badge("pe", "okunuş değişmez", 1100, 400, size=30, fill="tint", color="brand_dark"),
        Arrow("ar5", {"id": "pe", "side": "bottom"}, {"id": "c2", "char": -3, "side": "top"}, curve=-30)],
         say=[TR("Anşante kelimesinde de kadınlar sona e ekler. Ama burada okunuş değişmez, fark sadece yazıdadır."),
              FR("Enchanté !", "M1"), FR("Enchantée !", "F1")]),
    beat(clear=True, show=title("Sıfat, anlattığı kişiye uyar") + [
        Badge("lm", "Erkek", 200, 330, size=30, fill="tint", color="brand_dark"), T("c1", "Je suis tur[c|hl]", 420, 320, size=64),
        Badge("lf", "Kadın", 200, 490, size=30, fill="gold", color="ink"), T("c2", "Je suis tur[que|gold]", 420, 480, size=64),
        Badge("pe", "düzensiz", 1200, 400, size=30, fill="gold", color="ink"),
        Arrow("ar5", {"id": "pe", "side": "bottom"}, {"id": "c2", "char": -2, "side": "top"}, curve=-30)],
         say=[TR("Bazı sıfatların dişil hâli düzensizdir: erkek için c ile, kadın için q, u, e ile yazılır. Ama ikisi de aynı okunur: türk."),
              FR("Je suis turc.", "M1"), FR("Je suis turque.", "F1")]),
    beat(clear=True, show=title("Sıfat, anlattığı kişiye uyar") + note(
        "Sıfatların eril ve dişil hallerini 3. modülde ayrıntılı olarak göreceğiz.", kind="not", y=360),
         say=TR("Sıfatların eril ve dişil hallerini üçüncü modülde ayrıntılı olarak göreceğiz."), pause=0.8),
]))

# =============================================================================
# 7. Pronoms toniques
# =============================================================================
TON = [("[Moi|hl], je m'appelle Emre.", "Moi, je m'appelle Emre.", "Ben, benim adım Emre.", "mua"),
       ("Et [toi|hl], tu t'appelles comment ?", "Et toi, tu t'appelles comment ?", "Ya sen, senin adın ne?", "tua"),
       ("Et [vous|hl], vous êtes madame Martin ?", "Et vous, vous êtes madame Martin ?", "Ya siz, siz Bayan Martin misiniz?", "vu")]
b = [beat(show=title("[moi|hl], [toi|hl], [vous|hl]: vurgulu zamirler"),
          say=TR("Birini vurgulamak ya da ya sen diye sormak için vurgulu zamirleri kullanırız. Mua ben, tua sen, vu siz demektir."), pause=0.5)]
for i, (mk, txt, tr, ok) in enumerate(TON):
    y = 320 + i * 220
    b.append(beat(show=[T(f"p{i}", mk, 200, y, size=52, max_w=1300),
                        T(f"pt{i}", tr, 200, y + 80, size=32, font="regular", color="soft"),
                        Badge(f"po{i}", "okunuşu: " + ok, 1500, y + 4, size=28, fill="tint", color="brand_dark")],
                  say=FR(txt), pause=0.6))
b.append(beat(clear=True, show=title("[moi|hl], [toi|hl], [vous|hl]: vurgulu zamirler") + note(
    "Diğer vurgulu zamirleri (lui, elle) ve « c'est » ile birini tanıtmayı 3. modülde göreceğiz.", kind="not", y=360),
              say=TR("Diğer vurgulu zamirleri, yani lüi ve el zamirlerini, üçüncü modülde göreceğiz."), pause=0.8))
SCENES.append(scene("Vurgulu zamirler", b))

# =============================================================================
# 8. Alphabet
# =============================================================================
def alpha_grid(active=None, special=()):
    els = []
    for k, (L, ok) in enumerate(ALPHABET):
        r, c = divmod(k, 9)
        x, y = 190 + c * 190, 300 + r * 230
        colr = "brand" if k == active else ("gold_ink" if L in special else "ink")
        els.append(T(f"L{k}", L, x, y, size=84, font="display", color=colr, align="center"))
        els.append(T(f"Lo{k}", ok, x, y + 105, size=30, font="regular", color="brand" if k == active else "soft", align="center"))
    return els


b = [beat(show=title("Adını harf harf söyle: Fransız alfabesi"),
          say=TR("Fransa'da adını sık sık harf harf söylemen istenir. Bunun için Fransız alfabesini bilmen gerekiyor. "
                 "Her harfin altında Türkçe okunuşu var."), pause=0.4),
     beat(show=alpha_grid(), say=TR("Dinle ve tekrar et."), pause=0.3)]
for k, (L, ok) in enumerate(ALPHABET):
    b.append(beat(show=alpha_grid(active=k), say={"file": A + f"alphabet/{L.lower()}.mp3"}, lead=0.05, pause=0.35))
b.append(beat(show=alpha_grid(special=("E", "G", "J", "U")) + [
    Badge("att", "Dikkat!", 1700, 140, size=30, fill="gold", color="ink")],
              say=TR("Dikkat: E harfi ö, U harfi ü, G harfi je, J harfi ji diye okunur. Türkçeyle karıştırma."), pause=0.6))
b.append(beat(clear=True, show=title("Adını harf harf söyle") + [
    T("sp1", "Emre", CX, 330, size=110, font="display", align="center"),
    T("sp2", "[E|hl] · [M|hl] · [R|hl] · [E|hl]", CX, 520, size=80, font="display", align="center"),
    T("sp3", "ö · em · er · ö", CX, 650, size=40, font="regular", color="soft", align="center")],
              say=[TR("Mesela Emre adını şöyle söyleriz:"), {"file": A + "dialogue/m1-d04.mp3"}], pause=0.6))
b.append(beat(show=[Badge("you", "Sıra sende: kendi adını harf harf söyle", CX, 780, size=34, fill="gold", color="ink", align="center"),
                    Countdown("cd", 560, 880, 800)], say=TR("Sıra sende: kendi adını Fransızca harf harf söyle."), wait=9))
SCENES.append(scene("Fransız alfabesi", b))

# =============================================================================
# 9. Kelimeler (Mutlaka öğren)
# =============================================================================
b = [beat(show=title("Mutlaka öğren: 26 kelime", "Diğer 10 kelime « Öğrenmen tavsiye edilir » listesinde, sitede."),
          say=TR("Şimdi bu modülde mutlaka öğrenmen gereken yirmi altı kelimeye geçiyoruz. Her kelimeyi dinle, okunuşuna bak "
                 "ve örnek cümleyle birlikte tekrar et. Tavsiye edilen diğer kelimeler sitede."), pause=0.4),
     beat(show=[T("ok1", "Okunuşta küçük [ⁿ|hl] gördüğünde,", CX, 480, size=48, align="center"),
                T("ok2", "o sesi genizden söyle: « n » harfini tam okuma.", CX, 560, size=48, align="center"),
                T("ok3", "Okunuşlar yaklaşıktır. Asıl doğrusu sestir.", CX, 680, size=32, font="regular", color="soft", align="center")],
          say=TR("Okunuşta küçük bir n harfi gördüğünde, o sesi genizden söyle, n harfini tam okuma. "
                 "Okunuşlar yaklaşıktır, asıl doğrusu sestir."), pause=0.6)]
for k, (num, word, tr, exm, exf, extr) in enumerate(VOC, 1):
    base = A + f"voc/m1-v{num:02d}"
    trm, _, trf = extr.partition(" / ")
    trf = trf or trm
    head = [Badge("cnt", f"Kelime {k} / {len(VOC)}", 120, 120, size=28, fill="tint", color="brand_dark"),
            T("w", word, CX, 200, size=104, font="display", align="center")]
    b.append(beat(clear=True, show=head, say={"file": base + ".mp3"}, lead=0.2, pause=0.4))
    b.append(beat(show=[Badge("wo", "okunuşu:  " + OKUNUS[word], CX, 350, size=34, fill="tint", color="brand_dark", align="center"),
                        T("wm", tr, CX, 450, size=44, font="regular", color="soft", align="center")],
                  say=TR(tr.replace(" / ", ", ").replace("(", "").replace(")", "")), pause=0.4))
    ex_show = [Box("exb", 200, 580, 1520, 330, fill="card")]
    if exf:
        ex_show += [Badge("exg", "Erkek", 240, 610, size=26, fill="tint", color="brand_dark")]
    ex_show += [T("exf", hl_word(exm, word), CX, 660, size=50, align="center", max_w=1400)]
    b.append(beat(show=ex_show, say={"file": base + ("-ex-m.mp3" if exf else "-ex.mp3")}, pause=0.4))
    b.append(beat(show=T("ext", trm, CX, 800, size=36, font="regular", color="soft", align="center", max_w=1400),
                  say=TR(trm), pause=0.3))
    b.append(beat(show=Badge("rep", "Tekrar et", 1500, 610, size=26, fill="gold", color="ink"),
                  say={"file": base + ("-ex-m.mp3" if exf else "-ex.mp3")}, pause=1.2))
    if exf:
        b.append(beat(hide=["rep"], show=[Badge("exg", "Kadın", 240, 610, size=26, fill="gold", color="ink"),
                                          T("exf", diff_mark(exm, exf), CX, 660, size=50, align="center", max_w=1400),
                                          T("ext", trf, CX, 800, size=36, font="regular", color="soft", align="center", max_w=1400)],
                      say={"file": base + "-ex-f.mp3"}, pause=1.2))
SCENES.append(scene("Kelimeler", b))

# =============================================================================
# 10. Telaffuz
# =============================================================================
SIL = [("vou[s|mute]", "vous", "vu"), ("françai[s|mute]", "français", "fransé"), ("commen[t|mute]", "comment", "komaⁿ"),
       ("deu[x|mute]", "deux", "dö"), ("peti[t|mute]", "petit", "pöti")]
SPO = [("ave[c|hl2]", "avec", "avek"), ("bonjou[r|hl2]", "bonjour", "bonjur"), ("neu[f|hl2]", "neuf", "nöf"), ("i[l|hl2]", "il", "il")]
b = [beat(show=title("Sondaki harfler çoğu zaman okunmaz"),
          say=TR("Şimdi Türkçe konuşanların en çok zorlandığı konulardan birine bakalım. Türkçede her harf okunur. "
                 "Fransızcada ise kelimenin sonundaki sessiz harf çoğu zaman okunmaz."), pause=0.4),
     beat(show=[T("big", "salu[t|mute]", CX, 340, size=150, font="display", align="center"),
                Badge("okm", "okunmaz", 1420, 330, size=32, fill="no", color="white"),
                Arrow("art", {"id": "okm", "side": "left"}, {"id": "big", "char": -1, "side": "top"}, color="no", curve=-50),
                Badge("oks", "okunuşu:  salü", CX, 600, size=40, fill="tint", color="brand_dark", align="center")],
          say=[TR("Mesela bu kelime. Sondaki t okunmaz, bu yüzden salü deriz."), FR("salut")], pause=0.6),
     beat(clear=True, show=title("Okunmayanlar: -s, -t, -x, -d, -z, -p"), say=TR("Aynı kural bu kelimelerde de geçerli. Dinle:"), pause=0.2)]
for i, (mk, w, ok) in enumerate(SIL):
    x = 220 + i * 370
    b.append(beat(show=[T(f"s{i}", mk, x, 380, size=64, font="display", align="center"),
                        T(f"so{i}", ok, x, 490, size=34, font="regular", color="brand", align="center")],
                  say=FR(w), lead=0.1, pause=0.6))
b.append(beat(clear=True, show=title("Ama: [-c|hl], [-r|hl], [-f|hl], [-l|hl] genelde okunur") + [
    T("care", "[C|gold]a[R|gold]e[F|gold]u[L|gold]", CX, 260, size=110, font="display", align="center")],
              say=TR("Ama dört harf genelde okunur: ce, re, fe ve le. Bunları hatırlamak için İngilizce kerful kelimesini düşün."), pause=0.4))
for i, (mk, w, ok) in enumerate(SPO):
    x = 300 + i * 440
    b.append(beat(show=[T(f"c{i}", mk, x, 520, size=64, font="display", align="center"),
                        T(f"co{i}", ok, x, 630, size=34, font="regular", color="brand", align="center")],
                  say=FR(w), lead=0.1, pause=0.6))
b.append(beat(show=[T("ex1", "İstisna: -er ile biten fiillerde « r » okunmaz.", CX, 780, size=36, align="center"),
                    T("ex2", "répéte[r|mute]   →  repete        épele[r|mute]   →  eple", CX, 870, size=44, align="center")],
              say=[TR("Bir istisna var: e ve r ile biten fiillerde r okunmaz."), FR("répéter"), FR("épeler")], pause=0.6))
b.append(beat(clear=True, show=title("Dişil hali okunuşu değiştirebilir") + [
    T("pm", "Il est françai[s|mute].", 200, 360, size=64), Badge("pmo", "fransé", 1200, 366, size=32, fill="tint", color="brand_dark"),
    T("pf", "Elle est françai[s|hl][e|gold].", 200, 560, size=64), Badge("pfo", "fransez", 1200, 566, size=32, fill="gold", color="ink"),
    Arrow("are", {"id": "pfo", "side": "bottom"}, {"id": "pf", "char": -2, "side": "bottom"}, curve=-60)],
              say=[TR("Hatırlarsan, dişil hâlde sona bir e eklenir. Bu e, önceki harfin okunmasını sağlar: fransé, fransez."),
                   FR("Il est français.", "M1"), FR("Elle est française.", "F1")], pause=0.6))
for w, said, yes, ok in [("très", "très", False, "tre"), ("bonsoir", "bonsoir", True, "bonsuar"), ("trois", "trois", False, "trua")]:
    mk_q = w
    mk_a = (w[:-1] + f"[{w[-1]}|" + ("hl2" if yes else "mute") + "]")
    b.append(beat(clear=True, show=title("Dinle: son harf okunuyor mu?") + [
        T("qw", mk_q, CX, 380, size=130, font="display", align="center")], say=FR(said), pause=0.2))
    b.append(beat(show=Countdown("cd", 560, 640, 800), wait=4))
    b.append(beat(hide=["cd"], show=[T("qw", mk_a, CX, 380, size=130, font="display", align="center"),
                                     Badge("qa", ("Okunuyor" if yes else "Okunmuyor") + "  ·  " + ok, CX, 640, size=38,
                                           fill="ok", color="white", align="center")],
                  say=TR(("Okunuyor: " if yes else "Okunmuyor: ") + ok + "."), pause=0.6))
b.append(beat(clear=True, show=title("Sondaki harfler çoğu zaman okunmaz") + note(
    "Bazen okunmayan son harf, sesli harfle başlayan bir sonraki kelimeyle birleşip okunur: buna « liaison » denir. Bunu 2. modülde sayılarla göreceğiz.",
    kind="not", y=360),
              say=TR("Bazen okunmayan son harf, bir sonraki kelimeyle birleşip okunur. Buna liyezon denir. Bunu ikinci modülde sayılarla göreceğiz."), pause=0.8))
SCENES.append(scene("Telaffuz", b))

# =============================================================================
# 11. DELF köşesi
# =============================================================================
SIM = [("Bonjour !", None, "Bonjour madame !", "Bonjour madame !"),
       ("Vous vous appelez comment ?", None, "Je m'appelle Emre Yılmaz.", "Je m'appelle Elif Yılmaz."),
       ("Vous pouvez épeler votre prénom, s'il vous plaît ?", None, "Oui. E, M, R, E.", "Oui. E, L, I, F."),
       ("Vous êtes français ?", "Vous êtes française ?", "Non, je suis turc.", "Non, je suis turque."),
       ("Vous êtes en France depuis combien de temps ?", None,
        "Pardon, je ne comprends pas. Vous pouvez répéter, s'il vous plaît ?", "Pardon, je ne comprends pas. Vous pouvez répéter, s'il vous plaît ?"),
       ("Ça va ?", None, "Ça va très bien, merci. Et vous ?", "Ça va très bien, merci. Et vous ?"),
       ("Merci, c'est terminé. Au revoir !", None, "Merci, au revoir madame !", "Merci, au revoir madame !")]
parts = [Box("p1", 120, 300, 540, 200, fill="tint", outline="brand"), T("p1t", "1. Yönlendirilmiş görüşme", 150, 340, size=34, max_w=480),
         Box("p2", 690, 300, 540, 200, fill="card"), T("p2t", "2. Bilgi alışverişi", 720, 340, size=34, color="soft", max_w=480),
         Box("p3", 1260, 300, 540, 200, fill="card"), T("p3t", "3. Canlandırma", 1290, 340, size=34, color="soft", max_w=480)]
b = [beat(show=title("DELF köşesi: sözlü sınav, 1. bölüm") + parts,
          say=TR("Şimdi DELF sınavına geçelim. Sözlü sınav üç bölümden oluşur: yönlendirilmiş görüşme, bilgi alışverişi ve canlandırma. "
                 "Bugün birinci bölüme hazırlanıyoruz."), pause=0.4),
     beat(show=T("p1d", "Görevli sana kendinle ilgili basit sorular sorar. Hazırlık süresi yok.", 150, 420, size=26, font="regular", max_w=480),
          say=TR("Birinci bölümde sınav görevlisi sana kendinle ilgili basit sorular sorar. Bu bölüm için hazırlık süresi verilmez."), pause=0.4)]
TIPS = [("Görevliyi selamla ve « [vous|hl] » ile hitap et.", "Görevliyi selamla ve ona vu ile hitap et."),
        ("Sadece « Oui » deme: tam ve kısa bir cümle kur.", "Sadece vi deme. Kısa ama tam bir cümle kur."),
        ("Anlamadığında sessiz kalma: « [Vous pouvez répéter ?|hl] »", "Anlamadığında sessiz kalma, tekrar etmesini iste."),
        ("Sonunda vedalaşmayı unutma.", "Görüşmenin sonunda vedalaşmayı unutma.")]
for i, (txt, say) in enumerate(TIPS):
    b.append(beat(show=T(f"tip{i}", f"{i + 1}.  {txt}", 150, 560 + i * 90, size=38, max_w=1650), say=TR(say), pause=0.3))
b.append(beat(clear=True, show=title("Simülasyon"),
              say=TR("Şimdi bir simülasyon yapalım. Görevli soruyu soracak, sen de on saniye içinde yüksek sesle cevap vereceksin. "
                     "Sonra örnek cevabı dinleyeceğiz."), pause=0.5))
for i, (qm, qf, am, af) in enumerate(SIM, 1):
    qtext = qm if not qf else f"{qm}  /  {qf.split()[-2]} ?"
    q_audio = A + f"delf/m1-sim-q{i:02d}" + ("-m" if qf else "") + ".mp3"
    b.append(beat(clear=True, show=[Badge("qn", f"Soru {i} / {len(SIM)}", 120, 120, size=28, fill="tint", color="brand_dark"),
                                    T("ql", "Sınav görevlisi", CX, 220, size=30, color="soft", align="center"),
                                    T("qq", qtext, CX, 280, size=60, align="center", max_w=1600)],
                  say={"file": q_audio}, pause=0.2))
    b.append(beat(show=[Badge("yt", "Şimdi sen cevap ver", CX, 480, size=34, fill="gold", color="ink", align="center"),
                        Countdown("cd", 560, 580, 800)], wait=10))
    ans = [T("al", "Örnek cevap", CX, 480, size=30, color="soft", align="center")]
    says = [{"file": A + f"delf/m1-sim-a{i:02d}-m.mp3"}]
    if am == af:
        ans.append(T("am", am, CX, 540, size=48, color="brand_dark", align="center", max_w=1600))
    else:
        ans += [Badge("gm", "Erkek", 200, 560, size=26, fill="tint", color="brand_dark"),
                T("am", am, 380, 550, size=48, color="brand_dark", max_w=1400),
                Badge("gf", "Kadın", 200, 690, size=26, fill="gold", color="ink"),
                T("af", diff_mark(am, af), 380, 680, size=48, color="brand_dark", max_w=1400)]
        says.append({"file": A + f"delf/m1-sim-a{i:02d}-f.mp3"})
    b.append(beat(hide=["yt", "cd"], show=ans, say=says, pause=0.8))
    if i == 5:
        b.append(beat(show=T("n5", "Bu soru bilerek A1 seviyesinin üstündeydi.", CX, 820, size=34, font="regular", color="soft", align="center"),
                      say=TR("Bu soru bilerek A1 seviyesinin üstündeydi. Gördüğün gibi, anlamadığında tekrar etmesini istemek en doğru cevap."), pause=0.6))
b.append(beat(clear=True, show=title("DELF köşesi") + note(
    "Gerçek sınavda ailen, işin ve zevklerin hakkında da soru gelebilir. Bu konuları 2, 3 ve 4. modüllerde göreceğiz.", kind="not", y=360),
              say=TR("Gerçek sınavda ailen, işin ve zevklerin hakkında da soru gelebilir. Bu konuları ikinci, üçüncü ve dördüncü modüllerde göreceğiz."), pause=0.8))
SCENES.append(scene("DELF köşesi", b))

# =============================================================================
# 12. Mini test
# =============================================================================
QUIZ_SAY = ["Sabah bir dükkâna giriyorsun. Ne dersin?", "Öğretmenine adını nasıl sorarsın?", "Boşluğa hangi kelime gelir?",
            "Bir kadın hangisini yazar?", "Ekrandaki kelime nasıl okunur?"]
QUIZ = [("Sabah bir dükkâna giriyorsun. Ne dersin?", ["Bonjour !", "Bonsoir !", "Bonne soirée !"], 0,
         "Doğru cevap: bonjur. Gün içinde karşılaşınca bonjur denir."),
        ("Öğretmenine adını nasıl sorarsın?", ["Vous vous appelez comment ?", "Tu t'appelles comment ?", "Salut, ça va ?"], 0,
         "Doğru cevap: vu vuzaple koman. Öğretmene vu ile hitap ederiz."),
        ("Je ___ turque.", ["suis", "es", "est"], 0, "Doğru cevap: süi. Jö ile etr fiili süi olur."),
        ("Bir kadın hangisini yazar?", ["Enchanté", "Enchantée", "Enchantés"], 1, "Doğru cevap: ikinci seçenek. Kadınlar sona bir e ekler."),
        ("« salut » nasıl okunur?", ["salüt", "salü", "salut"], 1, "Doğru cevap: salü. Sondaki t okunmaz.")]
b = [beat(show=title("Mini test: 5 soru"), say=TR("Şimdi kendini test etme zamanı. Beş soru var. Her soru için beş saniyen olacak."), pause=0.4)]
for i, (q, opts, ok, expl) in enumerate(QUIZ, 1):
    show = [Badge("qn", f"Soru {i} / {len(QUIZ)}", 120, 120, size=28, fill="tint", color="brand_dark"),
            T("qq", q, CX, 260, size=56, align="center", max_w=1600)]
    for k, o in enumerate(opts):
        x = 140 + k * 560
        show += [Box(f"ob{k}", x, 450, 520, 150, fill="card"), T(f"ot{k}", o, x + 260, 495, size=38, align="center", max_w=480)]
    b.append(beat(clear=True, show=show, say=TR(QUIZ_SAY[i - 1]), pause=0.2))
    b.append(beat(show=Countdown("cd", 560, 700, 800), wait=5))
    b.append(beat(hide=["cd"], show=[Box(f"ob{ok}", 140 + ok * 560, 450, 520, 150, fill="ok_tint", outline="ok", width=4),
                                     T(f"ot{ok}", opts[ok], 140 + ok * 560 + 260, 495, size=38, color="ok", align="center", max_w=480),
                                     T("ex", expl, CX, 700, size=34, font="regular", color="soft", align="center", max_w=1600)],
                  say=TR(expl), pause=0.6))
SCENES.append(scene("Mini test", b))

# =============================================================================
# 13. Kapanış
# =============================================================================
SCENES.append(scene("Kapanış", [
    beat(show=title("Bugün neler öğrendik?") + [
        T("r1", "•  Selam vermek ve vedalaşmak", 140, 280, size=44),
        T("r2", "•  « [tu|hl] » ve « [vous|hl] » farkı", 140, 370, size=44),
        T("r3", "•  [être|hl] ve [s'appeler|hl] fiilleri", 140, 460, size=44),
        T("r4", "•  Fransız alfabesi ve sondaki okunmayan harfler", 140, 550, size=44),
        T("r5", "•  DELF sözlü sınavının ilk bölümü", 140, 640, size=44)],
         say=TR("Bugün selam vermeyi ve vedalaşmayı, tü ve vu farkını, etr ve saple fiillerini, Fransız alfabesini "
                "ve DELF sözlü sınavının ilk bölümünü öğrendik."), pause=0.5),
    beat(show=Badge("url", "Alıştırmalar, kelime testi ve modül testi:  kolayfransizca.app", 140, 760, size=34, fill="gold", color="ink"),
         say=TR("Şimdi sıra alıştırmalarda. Sitemizde bu modülün alıştırmalarını, kelime testini, yazma ödevini ve DELF tarzı testi ücretsiz olarak bulabilirsin."),
         pause=0.5),
    beat(clear=True, show=[T("t1", "Bu kurs tamamen [ücretsiz|hl].", CX, 300, size=64, font="display", align="center"),
                           T("t2", "Teşekkür etmenin en güzel yolu: kanala abone olmak.", CX, 420, size=44, align="center"),
                           Badge("nx", "Sonraki ders: Modül 2 · Kişisel bilgilerim", CX, 600, size=34, fill="tint", color="brand_dark", align="center")],
         say=[TR("Bu kurs tamamen ücretsiz. Bana teşekkür etmenin en güzel yolu kanala abone olmak. Bir sonraki modülde görüşmek üzere."),
              FR("à bientôt")], pause=1.5),
]))
