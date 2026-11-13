# -*- coding: utf-8 -*-
"""
Scénario de la vidéo du module 2 : « Kişisel bilgilerim ».
Lancement : python video_engine.py modul_02_video.py
Même gabarit que modul_01_video.py. Balisage : [segment|style] avec style = hl, hl2, gold, mark, ok, no, mute, soft.
Les audios français viennent des fichiers du site (a1/audio/m02/...). Le texte turc est lu par Derya.
Dans le texte turc, les mots français sont écrits comme ils se prononcent, pour que Derya les lise correctement.
"""
from video_engine import T, Box, Img, Arrow, Badge, Countdown, TR as _TR, FR, beat, scene


def TR(text):
    """Narration turque : le « ⁿ » des okunuş est réservé à l'écran, Derya lit un « n » normal."""
    return _TR(text.replace("ⁿ", "n"))

MODULE = {"slug": "modul-2-kisisel-bilgiler", "label": "Modül 2", "url": "kolayfransizca.app"}
A = "a1/audio/m02/"
IMG = "a1/img/m02/"
CX = 960


def F(path):
    return {"file": A + path}


# -----------------------------------------------------------------------------
# Données
# -----------------------------------------------------------------------------
DIALOGUE = [
    ("Mme Roux", "Bonjour monsieur ! C'est pour une inscription ?", "Merhaba beyefendi! Kayıt için mi geldiniz?"),
    ("Emre", "Oui, pour le cours de français. Je m'appelle Emre Yılmaz.", "Evet, Fransızca kursu için. Benim adım Emre Yılmaz."),
    ("Mme Roux", "Vous pouvez épeler votre nom, s'il vous plaît ?", "Soyadınızı harf harf söyleyebilir misiniz, lütfen?"),
    ("Emre", "Yılmaz. Y, I, L, M, A, Z.", "Yılmaz. Y, I, L, M, A, Z."),
    ("Mme Roux", "Merci. Vous avez quel âge ?", "Teşekkürler. Kaç yaşındasınız?"),
    ("Emre", "J'ai vingt-huit ans.", "Yirmi sekiz yaşındayım."),
    ("Mme Roux", "Quelle est votre nationalité ?", "Uyruğunuz nedir?"),
    ("Emre", "Je suis turc. Je suis né à Istanbul.", "Türküm. İstanbul'da doğdum."),
    ("Mme Roux", "Et vous habitez où ?", "Peki nerede oturuyorsunuz?"),
    ("Emre", "J'habite à Lyon, au 15, rue Victor-Hugo.", "Lyon'da, Victor-Hugo Sokağı 15 numarada oturuyorum."),
    ("Mme Roux", "Quelle est votre profession ?", "Mesleğiniz nedir?"),
    ("Emre", "Je suis ingénieur.", "Mühendisim."),
    ("Mme Roux", "Votre numéro de téléphone, s'il vous plaît ?", "Telefon numaranız, lütfen?"),
    ("Emre", "C'est le 06 45 18 72 30.", "06 45 18 72 30."),
    ("Mme Roux", "Et votre courriel ?", "Peki e-postanız?"),
    ("Emre", "emre.yilmaz@gmail.com", "emre.yilmaz@gmail.com"),
]

# (n° de fichier sur le site, mot, turc, exemple M, exemple F, traduction) — « Mutlaka öğren » uniquement
VOC = [
    (1, "avoir", "sahip olmak", "J'ai deux enfants.", "", "İki çocuğum var."),
    (2, "l'âge", "yaş", "Tu as quel âge ?", "", "Kaç yaşındasın?"),
    (3, "un an", "yıl / yaş", "J'ai trente ans.", "", "Otuz yaşındayım."),
    (4, "habiter", "oturmak / yaşamak", "J'habite à Lyon.", "", "Lyon'da yaşıyorum."),
    (5, "l'adresse", "adres", "Quelle est votre adresse ?", "", "Adresiniz nedir?"),
    (7, "la ville", "şehir", "Istanbul est une grande ville.", "", "İstanbul büyük bir şehirdir."),
    (8, "le pays", "ülke", "La Turquie est un beau pays.", "", "Türkiye güzel bir ülkedir."),
    (9, "la nationalité", "uyruk", "Quelle est votre nationalité ?", "", "Uyruğunuz nedir?"),
    (10, "turc / turque", "Türk", "Je suis turc.", "Je suis turque.", "Türküm."),
    (11, "français / française", "Fransız", "Je suis français.", "Je suis française.", "Fransızım."),
    (12, "la Turquie", "Türkiye", "Je viens de Turquie.", "", "Türkiye'den geliyorum."),
    (13, "la France", "Fransa", "J'habite en France.", "", "Fransa'da yaşıyorum."),
    (14, "venir de", "-den gelmek", "Je viens d'Ankara.", "", "Ankara'dan geliyorum."),
    (15, "né / née", "doğmuş", "Je suis né à Kayseri.", "Je suis née à Kayseri.", "Kayseri'de doğdum."),
    (16, "la date de naissance", "doğum tarihi", "Ma date de naissance est le 5 mai 1995.", "", "Doğum tarihim 5 Mayıs 1995."),
    (17, "la profession", "meslek", "Quelle est votre profession ?", "", "Mesleğiniz nedir?"),
    (18, "travailler", "çalışmak", "Je travaille dans un bureau.", "", "Bir ofiste çalışıyorum."),
    (19, "étudiant / étudiante", "öğrenci", "Je suis étudiant.", "Je suis étudiante.", "Öğrenciyim."),
    (25, "marié / mariée", "evli", "Je suis marié.", "Je suis mariée.", "Evliyim."),
    (26, "célibataire", "bekâr", "Je suis célibataire.", "", "Bekârım."),
    (27, "le numéro de téléphone", "telefon numarası", "Quel est ton numéro de téléphone ?", "", "Telefon numaran nedir?"),
    (28, "le courriel", "e-posta", "Quel est votre courriel ?", "", "E-postanız nedir?"),
    (29, "parler", "konuşmak", "Je parle turc et un peu français.", "", "Türkçe ve biraz Fransızca konuşuyorum."),
    (31, "un, deux, trois", "bir, iki, üç", "J'ai trois enfants.", "", "Üç çocuğum var."),
    (32, "dix", "on", "J'habite au numéro dix.", "", "On numarada oturuyorum."),
    (33, "vingt", "yirmi", "J'ai vingt ans.", "", "Yirmi yaşındayım."),
    (34, "cent", "yüz", "Le billet coûte cent euros.", "", "Bilet yüz euro tutuyor."),
    (35, "mille", "bin", "Paris est à mille kilomètres.", "", "Paris bin kilometre uzaklıkta."),
    (36, "quel / quelle", "hangi / ne", "Quel est votre nom ?", "", "Soyadınız nedir?"),
    (37, "où", "nerede", "Tu habites où ?", "", "Nerede oturuyorsun?"),
    (38, "combien", "kaç / ne kadar", "Tu as combien d'enfants ?", "", "Kaç çocuğun var?"),
]

# Okunuş yaklaşık ; « ⁿ » = genizden söylenen ses (n tam okunmaz)
OKUNUS = {
    "avoir": "avuar", "l'âge": "laj", "un an": "öⁿ naⁿ", "habiter": "abite", "l'adresse": "ladres", "la ville": "la vil",
    "le pays": "lö pei", "la nationalité": "la nasyonalite", "turc / turque": "türk", "français / française": "fransé / fransez",
    "la Turquie": "la türki", "la France": "la fraⁿs", "venir de": "vönir dö", "né / née": "ne",
    "la date de naissance": "la dat dö nesaⁿs", "la profession": "la profesyoⁿ", "travailler": "travaye",
    "étudiant / étudiante": "etüdyaⁿ / etüdyaⁿt", "marié / mariée": "marye", "célibataire": "selibater",
    "le numéro de téléphone": "lö nümero dö telefon", "le courriel": "lö kuryel", "parler": "parle",
    "un, deux, trois": "öⁿ, dö, trua", "dix": "dis", "vingt": "veⁿ", "cent": "saⁿ", "mille": "mil",
    "quel / quelle": "kel", "où": "u", "combien": "koⁿbiyeⁿ",
}

NUM = {0: "zéro", 1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit", 9: "neuf", 10: "dix",
       11: "onze", 12: "douze", 13: "treize", 14: "quatorze", 15: "quinze", 16: "seize", 17: "dix-sept", 18: "dix-huit",
       19: "dix-neuf", 20: "vingt", 21: "vingt et un", 22: "vingt-deux", 30: "trente", 40: "quarante", 50: "cinquante",
       60: "soixante", 70: "soixante-dix", 80: "quatre-vingts", 90: "quatre-vingt-dix", 100: "cent", 200: "deux cents", 1000: "mille"}


# -----------------------------------------------------------------------------
# Petits gabarits réutilisables (identiques au module 1)
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
    """Met le mot du vocabulaire en couleur dans la phrase d'exemple (articles retirés)."""
    cands = [w.strip(" ?") for w in word.split("/")]
    low = sentence.lower()
    for c in sorted(cands, key=len, reverse=True):
        for art in ("le ", "la ", "l'", "un "):
            if c.startswith(art) and len(c) > len(art) + 1:
                c = c[len(art):]
        i = low.find(c.lower())
        if i >= 0 and c:
            return sentence[:i] + "[" + sentence[i:i + len(c)] + "|hl]" + sentence[i + len(c):]
    return sentence


def diff_mark(a, b, style="gold"):
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
    beat(show=[Badge("tag", "DELF A1 Hazırlık · Modül 2", 120, 250, size=30, fill="tint", color="brand_dark"),
               T("h1", "Fransızca kişisel\n[bilgiler|hl]", 120, 340, size=72, font="display", line_h=1.12),
               T("h1fr", "Mes informations", 120, 560, size=40, font="regular", color="soft"),
               Img("hero", IMG + "m02-hero.webp", 1100, 220, 700, 600, radius=32)],
         say=TR("Merhaba! Kolay Fransızca'nın DELF A1 hazırlık kursunun ikinci modülüne hoş geldin. Bugünün konusu: kişisel bilgiler.")),
    beat(clear=True, show=title("Bu derste neler öğreneceksin?"), say=TR("Bu derste neler öğreneceğiz?")),
    beat(show=T("o1", "•  Yaşını söylemek: « [avoir|hl] » fiili", 140, 280, size=46), say=TR("Yaşını söylemeyi ve avuar fiilini,")),
    beat(show=T("o2", "•  Soru sormak: [quel|hl], [où|hl], [comment|hl], [combien|hl]", 140, 380, size=46),
         say=TR("kel, u, koman ve koⁿbiyen ile soru sormayı,")),
    beat(show=T("o3", "•  Nerede yaşadığını söylemek: [à|hl], [en|hl], [au|hl]", 140, 480, size=46),
         say=TR("nerede yaşadığını ve nereli olduğunu doğru edatla söylemeyi,")),
    beat(show=T("o4", "•  0'dan 1000'e [sayılar|hl] ve telefon numarası", 140, 580, size=46),
         say=TR("sıfırdan bine kadar sayıları ve telefon numarası söylemeyi,")),
    beat(show=T("o5", "•  DELF yazılı sınavı: [form doldurma|hl]", 140, 680, size=46),
         say=TR("ve DELF yazılı sınavının ilk alıştırması olan form doldurmayı öğreneceksin.")),
    beat(show=[Badge("url", "Alıştırmalar ve test:  kolayfransizca.app", 140, 810, size=36, fill="gold", color="ink")],
         say=TR("Bu dersin alıştırmaları, kelime testi ve modül testi ücretsiz olarak sitemizde seni bekliyor. Adresi ekranda görüyorsun."), pause=0.8),
]))

# =============================================================================
# 2. Diyalog
# =============================================================================
b = [beat(show=[Img("dimg", IMG + "m02-dialogue.webp", 480, 150, 960, 720, radius=32),
                Badge("pass", "1. dinleme · metin yok", CX, 900, size=32, fill="tint", color="brand_dark", align="center")],
          say=TR("Önce bir diyalog dinleyelim. Emre, Lyon'daki bir dil okulunda Fransızca kursuna kaydoluyor. "
                 "Sekreter Madam Ru ona sorular soruyor. İlk dinlemede metin yok. Sadece dinle ve hangi bilgileri anladığını düşün."), pause=0.8)]
for i, (who, fr, tr) in enumerate(DIALOGUE, 1):
    b.append(beat(show=Badge("pass", f"1. dinleme · {who} konuşuyor", CX, 900, size=32, fill="brand", color="white", align="center"),
                  say=F(f"dialogue/m2-d{i:02d}.mp3"), lead=0.1, pause=0.35))
b.append(beat(show=Badge("pass", "Ne anladın?", CX, 900, size=32, fill="gold", color="ink", align="center"),
              say=TR("Emre kaç yaşında? Mesleği ne? Şimdi metinle birlikte bir kez daha dinleyelim."), pause=0.6))
PER = 4
for page in range(len(DIALOGUE) // PER):
    for k in range(PER):
        i = page * PER + k
        show = [Img("dimg", IMG + "m02-dialogue.webp", 60, 170, 680, 510, radius=28),
                Badge("pass", "2. dinleme · metinle", 60, 720, size=30, fill="tint", color="brand_dark")]
        for kk in range(k + 1):
            j = page * PER + kk
            who, fr, tr = DIALOGUE[j]
            y = 150 + kk * 205
            cur = kk == k
            show += [T(f"dw{kk}", who, 800, y + 4, size=26, color="brand" if cur else "mute"),
                     T(f"df{kk}", fr, 980, y, size=36, max_w=880, color="ink" if cur else "mute"),
                     T(f"dt{kk}", tr, 980, y + 100, size=27, font="regular", color="soft" if cur else "mute", max_w=880)]
        b.append(beat(clear=(k == 0), show=show, say=F(f"dialogue/m2-d{i + 1:02d}.mp3"), lead=0.15, pause=0.5))
b.append(beat(clear=True, show=title("Sıra sende: Emre'nin cevaplarını tekrar et"),
              say=TR("Şimdi sıra sende. Emre'nin her cevabını dinle, sonra yüksek sesle tekrar et."), pause=0.5))
for i, (who, fr, tr) in enumerate(DIALOGUE, 1):
    if who != "Emre":
        continue
    q = DIALOGUE[i - 2]
    b.append(beat(clear=True, show=[T("rq", q[1], CX, 170, size=36, font="regular", color="soft", align="center", max_w=1600),
                                    Badge("who", who, CX, 270, size=32, fill="brand", color="white", align="center"),
                                    T("rf", fr, CX, 370, size=58, align="center", max_w=1600),
                                    T("rt", tr, CX, 580, size=36, font="regular", color="soft", align="center", max_w=1500)],
                  say=F(f"dialogue/m2-d{i:02d}.mp3"), pause=0.2))
    b.append(beat(show=[Badge("rep", "Tekrar et", CX, 710, size=34, fill="gold", color="ink", align="center"),
                        Countdown("cd", 560, 810, 800)], repeat=1.6))
b.append(beat(clear=True, show=title("Fransızca kursuna kayıt") + note(
    "Bir resmi kuruma, okula veya kütüphaneye kaydolurken hep aynı soruları duyarsın: adın, yaşın, adresin, telefonun. "
    "Bu soruları ezberlersen birçok durumda işine yarar.", y=360),
              say=TR("Benim tavsiyem şu: Fransa'da bir resmi kuruma, okula ya da kütüphaneye kaydolurken hep aynı soruları duyarsın. "
                     "Adın, yaşın, adresin, telefonun. Bu diyalogdaki soruları ezberlersen birçok durumda işine yarar."), pause=0.8))
SCENES.append(scene("Diyalog", b))

# =============================================================================
# 3. Dilbilgisi : avoir
# =============================================================================
AVOIR = [("j'[ai|hl]", "gram/m2-g01.mp3", "je", "benim ... var"), ("tu [as|hl]", "gram/m2-g02.mp3", "tü a", "senin ... var"),
         ("il / elle [a|hl]", "gram/m2-g03.mp3", "il a / el a", "onun ... var"), ("nous [avons|hl]", "gram/m2-g04.mp3", "nu zavoⁿ", "bizim ... var"),
         ("vous [avez|hl]", "gram/m2-g05.mp3", "vu zave", "sizin ... var"), ("ils / elles [ont|hl]", "gram/m2-g06.mp3", "il zoⁿ / el zoⁿ", "onların ... var")]
b = [beat(show=title("[avoir|hl] = sahip olmak", "« être » fiilinden sonra en çok kullanılan ikinci fiil."),
          say=TR("Birinci modülde etr fiilini gördük. Bugün en çok kullanılan ikinci fiile geçiyoruz: avuar, yani sahip olmak."), pause=0.6)]
for i, (mk, f, ok, tr) in enumerate(AVOIR):
    y = 320 + i * 100
    b.append(beat(show=[T(f"v{i}", mk, 200, y, size=50),
                        Badge(f"vo{i}", ok, 760, y - 2, size=30, fill="tint", color="brand_dark"),
                        T(f"vt{i}", tr, 1180, y + 4, size=36, font="regular", color="soft")],
                  say=F(f), lead=0.15, pause=0.5))
b.append(beat(show=[Badge("irr", "Düzensiz fiil: ezberle!", 1400, 250, size=30, fill="gold", color="ink"),
                    Arrow("ar1", {"id": "irr", "side": "left"}, {"id": "v0", "side": "right"}, curve=-40),
                    Arrow("ar2", {"id": "irr", "side": "bottom"}, {"id": "v5", "side": "right"}, curve=60)],
              say=TR("Avuar da etr gibi düzensiz bir fiildir. Bu tabloyu ezberlemen gerekiyor."), pause=0.6))
b.append(beat(hide=["irr", "ar1", "ar2"],
              show=[T("v0", "j'[ai|hl]", 200, 320, size=50),
                    T("je", "j[e|mute] + [a|gold]i → [j'|gold]ai", 1000, 960, size=36),
                    Arrow("ar3", (1000, 975), {"id": "v0", "side": "bottom"}, curve=-60)],
              say=TR("Dikkat: jö kelimesi sesli harfle başlayan e'nin önünde kısalır ve kesme işaretiyle yazılır: je."), pause=0.6))
b.append(beat(hide=["je", "ar3"],
              show=[T("v3", "nou[s|gold] [a|gold]vons", 200, 620, size=50), T("v4", "vou[s|gold] [a|gold]vez", 200, 720, size=50),
                    T("v5", "il[s|gold] / elle[s|gold] [o|gold]nt", 200, 820, size=50),
                    Badge("z", "[z] sesi", 1000, 960, size=32, fill="gold", color="ink"),
                    Arrow("ar4", {"id": "z", "side": "left"}, {"id": "vo4", "side": "bottom"}, curve=40)],
              say=TR("Bir ayrıntı daha: nu, vu ve il kelimelerinin sonundaki s, sonraki sesli harfe bağlanır ve z gibi okunur: "
                     "nu zavoⁿ, vu zave, il zoⁿ."), pause=0.8))
b.append(beat(clear=True, show=title("Yaş [avoir|hl] ile söylenir") + [
    T("ag1", "Türkçe:   28 yaşındayım.", 200, 300, size=44, color="soft"),
    T("ag2", "J'[ai|hl] vingt-huit [ans|hl].", 200, 420, size=72)],
              say=[TR("Türkçede yirmi sekiz yaşındayım deriz. Fransızcada ise yirmi sekiz yıla sahibim denir."), F("gram/m2-g07.mp3")], pause=0.5))
b.append(beat(show=[T("ag3", "Je suis vingt-huit ans.", 200, 580, size=60, color="no"),
                    Badge("wr", "YANLIŞ", 1300, 590, size=34, fill="no", color="white"),
                    Arrow("ar5", {"id": "wr", "side": "left"}, {"id": "ag3", "side": "right"}, color="no", curve=-30)],
              say=TR("Yani jö süi ile yaş söylenmez. Bu, Türklerin en sık yaptığı hatalardan biridir."), pause=0.6))
b.append(beat(show=[T("ag4", "J'ai vingt-huit ___.", 200, 720, size=48, color="soft"),
                    Badge("ans", "« ans » kelimesini unutma!", 1000, 730, size=30, fill="gold", color="ink")],
              say=TR("Bir de an kelimesini unutma. Sadece je vent üit demek eksik bir cümledir."), pause=0.6))
b.append(beat(clear=True, show=title("Yaş [avoir|hl] ile söylenir") + [
    T("aq1", "Vous [avez|hl] quel âge ?", 200, 330, size=56), T("aq1t", "Kaç yaşındasınız?", 200, 410, size=32, font="regular", color="soft")],
              say=F("gram/m2-g08.mp3"), pause=0.5))
b.append(beat(show=[T("aq2", "Elle [a|hl] deux enfants.", 200, 520, size=56), T("aq2t", "Onun iki çocuğu var.", 200, 600, size=32, font="regular", color="soft")],
              say=F("gram/m2-g09.mp3"), pause=0.6))
b.append(beat(clear=True, show=title("[avoir|hl] = sahip olmak") + note(
    "« ils ont » (onların ... var) ile « ils sont » (onlar ...dir) arasındaki farkı 9. modülde ayrıntılı olarak göreceğiz.", kind="not", y=360),
              say=TR("İl zoⁿ ile il soⁿ arasındaki farkı dokuzuncu modülde ayrıntılı olarak göreceğiz."), pause=0.8))
SCENES.append(scene("Dilbilgisi: avoir", b))

# =============================================================================
# 4. Soru sormak
# =============================================================================
QW = [("[quel|hl] / [quelle|hl]", "kel", "hangi, ne"), ("[où|hl]", "u", "nerede"), ("[comment|hl]", "komaⁿ", "nasıl"), ("[combien|hl]", "koⁿbiyeⁿ", "kaç, ne kadar")]
b = [beat(show=title("Soru sormak", "Günlük konuşmada soru kelimesi genelde cümlenin sonuna gelir."),
          say=TR("Kişisel bilgileri sormak için dört soru kelimesine ihtiyacın var."), pause=0.4)]
for i, (mk, ok, tr) in enumerate(QW):
    y = 320 + i * 110
    b.append(beat(show=[T(f"w{i}", mk, 200, y, size=56, font="display"),
                        Badge(f"wo{i}", ok, 760, y + 4, size=30, fill="tint", color="brand_dark"),
                        T(f"wt{i}", tr, 1080, y + 8, size=36, font="regular", color="soft")],
                  say=TR(f"{ok}: {tr}."), lead=0.1, pause=0.3))
EXQ = [("Vous habitez [où|hl] ?", "gram/m2-g12.mp3", "Nerede oturuyorsunuz?"), ("Vous vous appelez [comment|hl] ?", "gram/m2-g13.mp3", "Adınız ne?"),
       ("Vous avez [combien|hl] d'enfants ?", "gram/m2-g14.mp3", "Kaç çocuğunuz var?")]
b.append(beat(clear=True, show=title("Soru kelimesi sona gelir"), say=TR("Dinle: soru kelimesi cümlenin sonunda ve ses sonda yükseliyor."), pause=0.3))
for i, (mk, f, tr) in enumerate(EXQ):
    y = 320 + i * 200
    b.append(beat(show=[T(f"e{i}", mk, 200, y, size=54), T(f"et{i}", tr, 200, y + 82, size=32, font="regular", color="soft")],
                  say=F(f), pause=0.5))
b.append(beat(show=[Badge("up", "ses sonda yükselir ↗", 1350, 240, size=30, fill="gold", color="ink"),
                    Arrow("ar6", {"id": "up", "side": "bottom"}, {"id": "e0", "char": -3, "side": "top"}, curve=40)],
              say=TR("Soru kelimesini söylerken sesini yükselt."), pause=0.6))
b.append(beat(clear=True, show=title("[quel|hl] mi, [quelle|hl] mi?") + [
    Badge("em", "eril isim", 200, 300, size=30, fill="tint", color="brand_dark"),
    T("q1", "[Quel|hl] est votre nom ?", 200, 370, size=56), T("q1b", "quel âge · quel numéro", 200, 450, size=34, font="regular", color="soft")],
              say=[TR("Kel kelimesi, ardından gelen ismin cinsiyetine uyar. Eril isimlerle q, u, e, l yazılır."), F("gram/m2-g10.mp3")], pause=0.5))
b.append(beat(show=[Badge("df", "dişil isim", 200, 560, size=30, fill="gold", color="ink"),
                    T("q2", "Quel[le|gold] est votre adresse ?", 200, 630, size=56),
                    T("q2b", "quelle nationalité · quelle profession", 200, 710, size=34, font="regular", color="soft"),
                    Badge("same", "okunuş aynı: kel", 1350, 520, size=30, fill="tint", color="brand_dark"),
                    Arrow("ar7", {"id": "same", "side": "bottom"}, {"id": "q2", "char": 5, "side": "top"}, curve=-40)],
              say=[TR("Dişil isimlerle sona l, e eklenir. Ama okunuş değişmez, ikisi de kel okunur."), F("gram/m2-g11.mp3")], pause=0.6))
b.append(beat(clear=True, show=title("Soru sormak") + note(
    "Aynı soru resmi yazıda « Où habitez-vous ? » şeklinde de sorulabilir. Soru sormanın üç yolunu 4. modülde göreceğiz.", kind="not", y=360),
              say=TR("Aynı soru resmi yazıda farklı bir sırayla da sorulabilir. Soru sormanın üç yolunu dördüncü modülde göreceğiz. "
                     "Şimdilik soru kelimesini cümlenin sonuna koyman yeterli."), pause=0.8))
SCENES.append(scene("Dilbilgisi: soru sormak", b))

# =============================================================================
# 5. Şehirler ve ülkeler
# =============================================================================
COLS = [("à", "+ şehir", "J'habite [à|hl] Lyon.", "gram/m2-g15.mp3", "à Paris · à Istanbul", "brand"),
        ("en", "+ dişil ülke", "J'habite [en|hl] France.", "gram/m2-g16.mp3", "en Turquie · en Allemagne", "no"),
        ("au", "+ eril ülke", "J'habite [au|hl] Canada.", "gram/m2-g17.mp3", "au Maroc · au Japon", "ok"),
        ("aux", "+ çoğul ülke", "J'habite [aux|hl] États-Unis.", "gram/m2-g18.mp3", "aux Pays-Bas", "gold_ink")]
SAYC = ["Şehirlerden önce a kullanılır.", "Dişil ülkelerden önce aⁿ kullanılır. Fransa ve Türkiye dişildir.",
        "Eril ülkelerden önce o kullanılır.", "Çoğul ülkelerden önce yine o kullanılır, ama x ile yazılır."]
b = [beat(show=title("Nerede yaşıyorsun? [à|hl], [en|hl], [au|hl]", "Türkçede hepsi « -de / -da » ile söylenir. Fransızcada edat yere göre değişir."),
          say=TR("Nerede yaşadığını söylerken, Türkçede hep de, da ekini kullanırız. Fransızcada ise edat, yerin türüne göre değişir."), pause=0.4)]
for i, (p, kind, ex, f, more, colr) in enumerate(COLS):
    x = 120 + i * 430
    b.append(beat(show=[Box(f"cb{i}", x, 330, 400, 520, fill="card", outline=colr, width=4),
                        T(f"cp{i}", p, x + 30, 360, size=96, font="display", color=colr),
                        T(f"ck{i}", kind, x + 30, 500, size=32, font="regular", color="soft"),
                        T(f"ce{i}", ex, x + 30, 590, size=34, max_w=350),
                        T(f"cm{i}", more, x + 30, 740, size=26, font="regular", color="soft", max_w=350)],
                  say=[TR(SAYC[i]), F(f)], pause=0.5))
b.append(beat(clear=True, show=title("Ülke dişil mi, eril mi?") + [
    T("fe", "la Franc[e|gold] · la Turqui[e|gold] · l'Allemagn[e|gold]", 200, 330, size=48),
    Badge("fe2", "-e ile bitiyor → dişil → en", 200, 420, size=30, fill="gold", color="ink"),
    T("ma", "le Canada · le Japon · le Maroc", 200, 560, size=48),
    Badge("ma2", "diğerleri → eril → au", 200, 650, size=30, fill="tint", color="brand_dark")],
              say=TR("Bir ülkenin dişil mi eril mi olduğunu nasıl anlarsın? Sonuna bak: e ile bitenler genelde dişildir. Diğerleri genelde erildir."), pause=0.5))
b.append(beat(show=[T("exc", "İstisna: le Mexiqu[e|no] → au Mexique", 200, 780, size=40, color="no")],
              say=TR("Bilinen bir istisna var: Meksika, e ile bittiği hâlde erildir: o meksik."), pause=0.6))
VEN = [("Je viens [d'|hl]Ankara.", "gram/m2-g19.mp3", "şehir: de, sesli harften önce d'"),
       ("Je viens [de|hl] Turquie.", "gram/m2-g20.mp3", "dişil ülke: de"),
       ("Il vient [du|hl] Maroc.", "gram/m2-g21.mp3", "eril ülke: du = de + le"),
       ("Elle vient [des|hl] États-Unis.", "gram/m2-g22.mp3", "çoğul ülke: des = de + les")]
b.append(beat(clear=True, show=title("Nereli olduğunu söylemek: [venir de|hl]"),
              say=TR("Nereli olduğunu söylemek için vönir dö kullanırız, yani den gelmek."), pause=0.3))
for i, (mk, f, tr) in enumerate(VEN):
    y = 300 + i * 150
    b.append(beat(show=[T(f"n{i}", mk, 200, y, size=52), T(f"nt{i}", tr, 1150, y + 8, size=32, font="regular", color="soft")],
                  say=F(f), pause=0.5))
b.append(beat(show=[Badge("du", "de + le = du", 1350, 940, size=32, fill="gold", color="ink"),
                    Arrow("ar8", {"id": "du", "side": "top"}, {"id": "n2", "char": 10, "side": "bottom"}, curve=50)],
              say=TR("Dö kelimesi lö ile birleşince dü olur. Dö ile le birleşince de dey olur."), pause=0.6))
b.append(beat(clear=True, show=title("Şehirler ve ülkeler") + note(
    "Ülke adlarını öğrenirken artikeliyle birlikte öğren: la France, le Canada. Böylece hangi edatı kullanacağını hemen bilirsin.", y=360),
              say=TR("Benim tavsiyem: ülke adlarını artikeliyle birlikte öğren, la frans, lö kanada gibi. Böylece hangi edatı kullanacağını hemen bilirsin."), pause=0.8))
SCENES.append(scene("Şehirler ve ülkeler", b))

# =============================================================================
# 6. Uyruk ve meslek
# =============================================================================
GEN = [("Je suis turc.", "Je suis turque.", 1, -4, "düzensiz", "Türk kelimesi düzensizdir. Erkek için c ile, kadın için q, u, e ile yazılır. İkisi de türk okunur."),
       ("Je suis français.", "Je suis française.", 2, -3, "s okunur: [z]", "Kadın için sona e eklenir ve s harfi z gibi okunur: fransé, fransez."),
       ("Je suis allemand.", "Je suis allemande.", 3, -3, "d okunur", "Alman kelimesinde de aynı kural var: sona eklenen e, d harfini okutur."),
       ("Je suis algérien.", "Je suis algérienne.", 4, -4, "-ien → -ienne", "İyeⁿ ile biten kelimeler kadın için i, e, n, n, e olur: aljeriyeⁿ, aljeriyen."),
       ("Je suis vendeur.", "Je suis vendeuse.", 7, -3, "-eur → -euse", "Ör ile biten meslekler kadın için öz olur: vaⁿdör, vaⁿdöz."),
       ("Je suis belge.", "Je suis belge.", 5, -2, "değişmez", "Zaten e ile biten kelimeler değişmez: belj."),
       ("Je suis né à Kayseri.", "Je suis née à Kayseri.", 8, 10, "okunuş aynı", "Ne kelimesi de konuşan kişiye uyar. Kadın sona e ekler ama okunuş değişmez.")]
b = [beat(show=title("Uyruk ve meslek: [eril|hl] ve [dişil|gold]"),
          say=TR("Birinci modülde türk ve türk örneğini gördük. Uyrukların ve mesleklerin çoğu aynı kurala uyar. Şimdi bir erkeği ve bir kadını dinleyelim."), pause=0.5)]
for m, f, n, ch, lab, say in GEN:
    b.append(beat(clear=True, show=title("Uyruk ve meslek: [eril|hl] ve [dişil|gold]") + [
        Badge("lm", "Erkek", 200, 340, size=30, fill="tint", color="brand_dark"), T("gm", m, 420, 330, size=64),
        Badge("lf", "Kadın", 200, 520, size=30, fill="gold", color="ink"), T("gf", diff_mark(m, f), 420, 510, size=64)],
                  say=[F(f"gram/m2-gx{n:02d}-m.mp3"), F(f"gram/m2-gx{n:02d}-f.mp3")], pause=0.3))
    b.append(beat(show=[Badge("pe", lab, 1350, 700, size=32, fill="gold", color="ink"),
                        Arrow("ar9", {"id": "pe", "side": "top"}, {"id": "gf", "char": ch, "side": "bottom"}, curve=-40)],
                  say=TR(say), pause=0.6))
b.append(beat(clear=True, show=title("Uyruk ve meslek") + note(
    "Uyruk adları Fransızcada küçük harfle yazılır: « Je suis turc ». Ülke adları ise büyük harfle başlar: « la Turquie ».", kind="not", y=360),
              say=TR("Bir yazım notu: uyruk adları Fransızcada küçük harfle yazılır, ülke adları ise büyük harfle başlar. "
                     "Sıfatların tüm eril ve dişil hâllerini üçüncü modülde göreceğiz."), pause=0.8))
SCENES.append(scene("Uyruk ve meslek", b))

# =============================================================================
# 7. Sayılar
# =============================================================================
def num_grid(nums, active=None, cols=7, y0=300, dy=230, x0=230, dx=245):
    els = []
    for k, n in enumerate(nums):
        r, c = divmod(k, cols)
        x, y = x0 + c * dx, y0 + r * dy
        on = n == active
        els.append(T(f"N{k}", str(n), x, y, size=80, font="display", color="brand" if on else "ink", align="center"))
        els.append(T(f"Nw{k}", NUM[n], x, y + 100, size=28, font="regular", color="brand" if on else "soft", align="center"))
    return els


b = [beat(show=title("0'dan 1000'e sayılar"),
          say=TR("Yaş, adres, telefon numarası: kişisel bilgilerin çoğu sayıdır. Şimdi sayıları dinle ve her birini tekrar et."), pause=0.4)]
LOW = list(range(0, 21))
for part in (LOW[:14], LOW[14:]):
    b.append(beat(clear=True, show=title("0 – 20") + num_grid(part), pause=0.2))
    for n in part:
        b.append(beat(show=num_grid(part, active=n), say=F(f"nombres/n-{n}.mp3"), lead=0.05, pause=0.45))
HIGH = [21, 22, 30, 40, 50, 60, 100, 200, 1000]
b.append(beat(clear=True, show=title("Onlar ve fazlası") + num_grid(HIGH, cols=5, dx=330, x0=290), pause=0.2))
for n in HIGH:
    b.append(beat(show=num_grid(HIGH, active=n, cols=5, dx=330, x0=290), say=F(f"nombres/n-{n}.mp3"), lead=0.05, pause=0.45))
b.append(beat(show=[Badge("et", "21: vingt [et|hl] un", 290, 820, size=32, fill="gold", color="ink")],
              say=TR("Dikkat: yirmi bir, otuz bir gibi sayılarda e kelimesi araya girer: veⁿ te öⁿ."), pause=0.6))
CALC = [(70, "[soixante|hl]-[dix|no]", "[60|hl] + [10|no]", "Yetmiş için altmış artı on denir: suasaⁿt dis."),
        (71, "[soixante|hl] et [onze|no]", "[60|hl] + [11|no]", "Yetmiş bir: altmış artı on bir."),
        (80, "[quatre|ok]-[vingts|hl]", "[4|ok] × [20|hl]", "Seksen için dört kere yirmi denir: katr veⁿ."),
        (90, "[quatre|ok]-[vingt|hl]-[dix|no]", "[4|ok] × [20|hl] + [10|no]", "Doksan ise dört kere yirmi artı on: katr veⁿ dis.")]
b.append(beat(clear=True, show=title("70, 80, 90: hesapla kurulur", "60'a kadar sayılar düzenlidir. Sonra Fransızca hesap yapar."),
              say=TR("Altmışa kadar sayılar düzenlidir. Yetmiş, seksen ve doksanda ise Fransızca hesap yapar. Renkleri takip et."), pause=0.4))
for i, (n, w, eq, say) in enumerate(CALC):
    y = 330 + i * 150
    b.append(beat(show=[T(f"cn{i}", str(n), 200, y, size=72, font="display"),
                        T(f"cw{i}", w, 420, y + 10, size=54),
                        T(f"ce{i}", eq, 1350, y + 10, size=54, font="display")],
                  say=[TR(say), F(f"nombres/n-{n}.mp3")], pause=0.6))
b.append(beat(clear=True, show=title("70, 80, 90") + note(
    "Bu sayıları sesli tekrar ederek çalış. Belçika ve İsviçre'de « septante » (70) ve « nonante » (90) denir. Duyarsan şaşırma.", y=360),
              say=TR("Benim tavsiyem: bu sayıları sesli tekrar ederek çalış. Belçika ve İsviçre'de yetmiş için septaⁿt, doksan için nonaⁿt denir. Duyarsan şaşırma."), pause=0.8))
PH = ["06", "45", "18", "72", "30"]
ph = [Box(f"pb{k}", 330 + k * 270, 360, 230, 150, fill="tint", outline="brand") for k in range(5)]
ph += [T(f"pt{k}", PH[k], 330 + k * 270 + 115, 385, size=80, font="display", color="brand_dark", align="center") for k in range(5)]
b.append(beat(clear=True, show=title("Telefon numarası ikişer ikişer okunur",
                                     "Fransa'da cep telefonu numarası 10 rakamdır ve 06 veya 07 ile başlar.") + ph,
              say=TR("Fransa'da telefon numarası on rakamdır. Rakamlar tek tek değil, ikişer ikişer okunur."), pause=0.3))
b.append(beat(show=[T("pr", "zéro six · quarante-cinq · dix-huit · [soixante-douze|hl] · trente", CX, 590, size=44, align="center", max_w=1700)],
              say=F("nombres/tel-exemple.mp3"), pause=0.5))
b.append(beat(show=[Badge("p72", "72 = 60 + 12", 1350, 720, size=32, fill="gold", color="ink"),
                    Arrow("ar10", {"id": "p72", "side": "top"}, {"id": "pt3", "side": "bottom"}, curve=-30)],
              say=TR("Yetmiş iki: altmış artı on iki, yani suasaⁿt duz."), pause=0.6))
b.append(beat(clear=True, show=title("E-posta adresi nasıl okunur?") + [
    T("ml", "emre[.|hl]yilmaz[@|gold]gmail[.|hl]com", CX, 360, size=78, font="display", align="center"),
    Badge("at", "@ = arobase", 560, 560, size=36, fill="gold", color="ink"),
    Badge("pt", ". = point", 1060, 560, size=36, fill="tint", color="brand_dark")],
              say=[TR("E-posta adresini söylerken et işaretine arobaz, noktaya puaⁿ denir."), F("nombres/mail-exemple.mp3")], pause=0.8))
SCENES.append(scene("Sayılar", b))

# =============================================================================
# 8. Kelimeler (Mutlaka öğren)
# =============================================================================
b = [beat(show=title(f"Mutlaka öğren: {len(VOC)} kelime", "Diğer 9 kelime « Öğrenmen tavsiye edilir » listesinde, sitede."),
          say=TR("Şimdi bu modülde mutlaka öğrenmen gereken otuz bir kelimeye geçiyoruz. Her kelimeyi dinle, okunuşuna bak "
                 "ve örnek cümleyle birlikte tekrar et. Tavsiye edilen diğer kelimeler sitede."), pause=0.4),
     beat(show=[T("ok1", "Okunuşta küçük [ⁿ|hl] gördüğünde,", CX, 480, size=48, align="center"),
                T("ok2", "o sesi genizden söyle: « n » harfini tam okuma.", CX, 560, size=48, align="center"),
                T("ok3", "Okunuşlar yaklaşıktır. Asıl doğrusu sestir.", CX, 680, size=32, font="regular", color="soft", align="center")],
          say=TR("Hatırlatma: okunuşta küçük bir n harfi gördüğünde, o sesi genizden söyle. Okunuşlar yaklaşıktır, asıl doğrusu sestir."), pause=0.6)]
for k, (num, word, tr, exm, exf, extr) in enumerate(VOC, 1):
    base = f"voc/m2-v{num:02d}"
    head = [Badge("cnt", f"Kelime {k} / {len(VOC)}", 120, 120, size=28, fill="tint", color="brand_dark"),
            T("w", word, CX, 200, size=96, font="display", align="center", max_w=1700)]
    b.append(beat(clear=True, show=head, say=F(base + ".mp3"), lead=0.2, pause=0.4))
    b.append(beat(show=[Badge("wo", "okunuşu:  " + OKUNUS[word], CX, 350, size=34, fill="tint", color="brand_dark", align="center"),
                        T("wm", tr, CX, 450, size=44, font="regular", color="soft", align="center")],
                  say=TR(tr.replace(" / ", ", ")), pause=0.4))
    ex_show = [Box("exb", 200, 580, 1520, 330, fill="card")]
    if exf:
        ex_show += [Badge("exg", "Erkek", 240, 610, size=26, fill="tint", color="brand_dark")]
    ex_show += [T("exf", hl_word(exm, word), CX, 660, size=50, align="center", max_w=1400)]
    b.append(beat(show=ex_show, say=F(base + ("-ex-m.mp3" if exf else "-ex.mp3")), pause=0.4))
    b.append(beat(show=T("ext", extr, CX, 800, size=36, font="regular", color="soft", align="center", max_w=1400),
                  say=TR(extr), pause=0.3))
    b.append(beat(show=Badge("rep", "Tekrar et", 1500, 610, size=26, fill="gold", color="ink"),
                  say=F(base + ("-ex-m.mp3" if exf else "-ex.mp3")), pause=1.2))
    if exf:
        b.append(beat(hide=["rep"], show=[Badge("exg", "Kadın", 240, 610, size=26, fill="gold", color="ink"),
                                          T("exf", diff_mark(exm, exf), CX, 660, size=50, align="center", max_w=1400)],
                      say=F(base + "-ex-f.mp3"), pause=1.2))
SCENES.append(scene("Kelimeler", b))

# =============================================================================
# 9. Telaffuz : liaisons
# =============================================================================
LIA = [("u[n|gold]‿an", "[n]", "telaffuz/m2-t01.mp3", "öⁿ naⁿ"), ("deu[x|gold]‿ans", "[z]", "telaffuz/m2-t02.mp3", "dö zaⁿ"),
       ("troi[s|gold]‿ans", "[z]", "telaffuz/m2-t03.mp3", "trua zaⁿ"), ("di[x|gold]‿ans", "[z]", "telaffuz/m2-t04.mp3", "di zaⁿ"),
       ("neu[f|gold]‿ans", "[v]", "telaffuz/m2-t05.mp3", "nö vaⁿ"), ("ving[t|gold]‿ans", "[t]", "telaffuz/m2-t06.mp3", "veⁿ taⁿ")]
b = [beat(show=title("Sayılarla bağlama: « liaison »"),
          say=TR("Birinci modülde son harflerin çoğu zaman okunmadığını gördük. Ama arkasından sesli harfle başlayan bir kelime gelirse, "
                 "bu harf okunur ve sonraki kelimeye bağlanır. Buna liyezon denir. Yaş söylerken an kelimesiyle çok sık olur."), pause=0.4),
     beat(show=[T("big", "deu[x|gold]‿ans", CX, 330, size=140, font="display", align="center"),
                Badge("bz", "[z] sesi", 1450, 330, size=34, fill="gold", color="ink"),
                Arrow("arz", {"id": "bz", "side": "left"}, {"id": "big", "char": 3, "side": "top"}, curve=-50),
                Badge("bo", "okunuşu:  dö zaⁿ", CX, 600, size=40, fill="tint", color="brand_dark", align="center")],
          say=[TR("Mesela iki yaş. Dö kelimesinin sonundaki x tek başına okunmaz. Ama an kelimesinden önce z gibi okunur: dö zaⁿ."),
               F("telaffuz/m2-t02.mp3")], pause=0.6),
     beat(clear=True, show=title("Bağlanan harf yeni bir ses verir"), say=TR("Şimdi diğer sayıları dinle. Bağlanan harfi takip et."), pause=0.2)]
for i, (mk, snd, f, ok) in enumerate(LIA):
    r, c = divmod(i, 3)
    x, y = 340 + c * 620, 330 + r * 300
    b.append(beat(show=[T(f"l{i}", mk, x, y, size=66, font="display", align="center"),
                        Badge(f"ls{i}", snd + "  ·  " + ok, x, y + 110, size=30, fill="tint", color="brand_dark", align="center")],
                  say=F(f), lead=0.1, pause=0.7))
b.append(beat(show=[Badge("nf", "neuf ans: « f » → [v]", CX, 940, size=32, fill="gold", color="ink", align="center")],
              say=TR("En şaşırtıcısı dokuz yaş: nöf kelimesinin f harfi v gibi okunur: nö vaⁿ."), pause=0.6))
SIX = [("six", "telaffuz/m2-t10.mp3", "tek başına: [s]", "sis"), ("six‿ans", "telaffuz/m2-t11.mp3", "sesli harften önce: [z]", "si zaⁿ"),
       ("si[x|mute] livres", "telaffuz/m2-t12.mp3", "sessiz harften önce: okunmaz", "si livr")]
b.append(beat(clear=True, show=title("Dikkat: [six|hl] ve [dix|hl]"),
              say=TR("Altı ve on sayılarının son harfi üç farklı şekilde okunur. Dinle:"), pause=0.3))
for i, (mk, f, lab, ok) in enumerate(SIX):
    y = 320 + i * 190
    b.append(beat(show=[T(f"x{i}", mk, 200, y, size=64, font="display"),
                        T(f"xl{i}", lab, 800, y + 14, size=36, font="regular", color="soft"),
                        Badge(f"xo{i}", ok, 1500, y + 10, size=30, fill="tint", color="brand_dark")],
                  say=F(f), pause=0.7))
QA = [("J'ai deux ans.", "telaffuz/m2-t13.mp3", ["2", "12", "10"], 0, "deux‿ans: iki yaş."),
      ("J'ai seize ans.", "telaffuz/m2-t14.mp3", ["16", "6", "13"], 0, "seize: on altı."),
      ("J'ai trente ans.", "telaffuz/m2-t15.mp3", ["30", "13", "3"], 0, "trente: otuz. Treize ise on üç."),
      ("J'ai soixante-dix ans.", "telaffuz/m2-t16.mp3", ["70", "60", "17"], 0, "soixante-dix: altmış artı on, yani yetmiş."),
      ("J'ai neuf ans.", "telaffuz/m2-t17.mp3", ["9", "19", "90"], 0, "neuf‿ans: dokuz yaş.")]
b.append(beat(clear=True, show=title("Dinle ve seç: kaç yaşında?"),
              say=TR("Şimdi küçük bir dinleme testi. Kişi kaç yaşında? Dinle ve doğru sayıyı seç."), pause=0.3))
for i, (fr, f, opts, ok, expl) in enumerate(QA, 1):
    show = [Badge("qn", f"Soru {i} / {len(QA)}", 120, 120, size=28, fill="tint", color="brand_dark"),
            T("qq", "Kaç yaşında?", CX, 260, size=60, align="center")]
    for k, o in enumerate(opts):
        x = 340 + k * 450
        show += [Box(f"ob{k}", x, 420, 380, 170, fill="card"), T(f"ot{k}", o, x + 190, 455, size=72, font="display", align="center")]
    b.append(beat(clear=True, show=show, say=F(f), pause=0.2))
    b.append(beat(show=Countdown("cd", 560, 680, 800), wait=4))
    b.append(beat(hide=["cd"], show=[Box(f"ob{ok}", 340 + ok * 450, 420, 380, 170, fill="ok_tint", outline="ok", width=4),
                                     T(f"ot{ok}", opts[ok], 340 + ok * 450 + 190, 455, size=72, font="display", color="ok", align="center"),
                                     T("ex", fr + "   " + expl, CX, 690, size=36, font="regular", color="soft", align="center", max_w=1600)],
                  say=[F(f)], pause=0.6))
b.append(beat(clear=True, show=title("Sayılarla bağlama") + note(
    "« liaison » sadece sayılarla olmaz: « vous‿avez », « les‿enfants » gibi. Diğer bağlamaları ilerleyen modüllerde, özellikle 9. modülde göreceğiz.",
    kind="not", y=360),
              say=TR("Liyezon sadece sayılarla olmaz. Vu zave, le zaⁿfaⁿ gibi örneklerde de var. Diğer bağlamaları ilerleyen modüllerde, "
                     "özellikle dokuzuncu modülde göreceğiz."), pause=0.8))
SCENES.append(scene("Telaffuz", b))

# =============================================================================
# 10. DELF köşesi : formulaire + numéro de téléphone
# =============================================================================
parts = [Box("p1", 120, 300, 820, 200, fill="tint", outline="brand"), T("p1t", "1. Form doldurmak", 150, 340, size=36, max_w=760),
         Box("p2", 980, 300, 820, 200, fill="card"), T("p2t", "2. Kısa bir mesaj yazmak (yaklaşık 40 kelime)", 1010, 340, size=36, color="soft", max_w=760)]
b = [beat(show=title("DELF köşesi: yazılı sınav, 1. alıştırma") + parts,
          say=TR("Şimdi DELF sınavına geçelim. Yazılı anlatım sınavı iki alıştırmadan oluşur: bir form doldurmak ve kısa bir mesaj yazmak. "
                 "Bugün birinci alıştırmaya hazırlanıyoruz."), pause=0.4),
     beat(show=T("p1d", "Bir kayıt formu, bir üyelik kartı veya bir otel fişi.", 150, 420, size=28, font="regular", max_w=760),
          say=TR("Bu bir kayıt formu, bir üyelik kartı ya da bir otel fişi olabilir."), pause=0.4)]
TIPS = [("Ülke ve şehir adlarını Fransızca yaz: [Turquie|hl], « Türkiye » değil.", "Formu okuyan kişi Fransızdır. Ülke ve şehir adlarını Fransızca yaz: türki."),
        ("« Nationalité » dişil: [Nationalité : turque|hl], erkek için de.", "Nasyonalite kelimesi dişildir. Bu yüzden formda uyruğu dişil hâliyle yaz: türk, yani q, u, e ile. Erkeksen bile."),
        ("Tarih: gün / ay / yıl. [05/05/1995|hl]", "Tarih sırası Türkçedeki gibidir: gün, ay, yıl."),
        ("Her kutuyu doldur. İstenen hiçbir bilgiyi atlama.", "Her kutuyu doldur. İstenen hiçbir bilgiyi atlama.")]
for i, (txt, say) in enumerate(TIPS):
    b.append(beat(show=T(f"tip{i}", f"{i + 1}.  {txt}", 150, 560 + i * 90, size=38, max_w=1650), say=TR(say), pause=0.3))
# démonstration : remplir la fiche de Leyla
MSG = ("Bonjour ! Je m'appelle Leyla Demir. J'ai vingt-quatre ans et je suis turque. Je suis née à Izmir, mais maintenant "
       "j'habite à Bordeaux. Je suis étudiante. Mon numéro de téléphone, c'est le 07 12 34 56 78.")
FIELDS = [("NOM", "Demir"), ("PRÉNOM", "Leyla"), ("ÂGE", "24 ans"), ("NATIONALITÉ", "turque"),
          ("LIEU DE NAISSANCE", "Izmir"), ("VILLE", "Bordeaux"), ("PROFESSION", "étudiante"), ("TÉLÉPHONE", "07 12 34 56 78")]
SAYF = ["Soyad: Demir.", "Ad: Leyla.", "Yaş: yirmi dört. Rakamla yaz ve an kelimesini ekle.", "Uyruk: türk, dişil hâliyle.",
        "Doğum yeri: İzmir.", "Oturduğu şehir: Bordo. Doğduğu şehir değil!", "Meslek: öğrenci, Leyla kadın olduğu için etüdyant.",
        "Telefon: on rakam, ikişer ikişer."]
b.append(beat(clear=True, show=title("Örnek: Leyla için formu dolduralım") + [
    Box("mb", 120, 260, 1680, 230, fill="tint", outline="brand"), T("msg", MSG, 160, 290, size=32, font="regular", max_w=1600)],
              say=TR("Leyla'nın mesajını oku. Sonra formu onun için birlikte dolduralım."), wait=6, pause=0.5))
form = [Box("fb", 120, 530, 1680, 470, fill="card", outline="ink", width=3),
        T("ftit", "MÉDIATHÈQUE DE BORDEAUX · Fiche d'inscription", 160, 555, size=30)]
for k, (lab, _) in enumerate(FIELDS):
    r, c = divmod(k, 2)
    x, y = 160 + c * 820, 630 + r * 90
    form.append(T(f"fl{k}", lab + " :", x, y, size=28, color="soft"))
b.append(beat(show=form, pause=0.3))
for k, (lab, val) in enumerate(FIELDS):
    r, c = divmod(k, 2)
    x, y = 160 + c * 820 + 360, 625 + r * 90
    b.append(beat(show=T(f"fv{k}", val, x, y, size=36, color="brand"), say=TR(SAYF[k]), pause=0.3))
    if lab == "NATIONALITÉ":
        b.append(beat(show=[Badge("fem", "dişil hali!", 1350, 470, size=30, fill="gold", color="ink"),
                            Arrow("arf", {"id": "fem", "side": "bottom"}, {"id": f"fv{k}", "side": "right"}, curve=40)],
                      say=TR("Hatırla: türk değil, türk; q, u, e ile yazılan dişil hâl."), pause=0.5))
b.append(beat(hide=["fem", "arf"], show=Badge("okf", "Form tamam!", 1500, 120, size=32, fill="ok", color="white"),
              say=TR("Form tamam. Sitede aynı formu kendin doldurabilir ve cevaplarını kontrol edebilirsin."), pause=0.6))
# dictée de numéros
TEL = [("06 12 85 40 77", "delf/m2-tel01.mp3"), ("07 63 20 91 14", "delf/m2-tel02.mp3"), ("01 45 33 70 26", "delf/m2-tel03.mp3")]
b.append(beat(clear=True, show=title("Dinleme: telefon numarasını yaz"),
              say=TR("Dinleme sınavında da sık sık bir numarayı not etmen istenir. Kâğıt kalem al. Numarayı dinle ve yaz."), pause=0.4))
for i, (num, f) in enumerate(TEL, 1):
    b.append(beat(clear=True, show=title("Dinleme: telefon numarasını yaz") + [
        Badge("qn", f"Numara {i} / {len(TEL)}", 120, 260, size=28, fill="tint", color="brand_dark"),
        T("blank", "__ __ __ __ __", CX, 400, size=90, font="display", color="mute", align="center")], say=F(f), pause=0.2))
    b.append(beat(show=Countdown("cd", 560, 640, 800), say=F(f), wait=6))
    pairs = num.split()
    b.append(beat(hide=["cd"], show=[T("blank", "  ".join(pairs), CX, 400, size=90, font="display", color="ok", align="center")],
                  say=TR("Doğru cevap ekranda."), pause=0.8))
b.append(beat(clear=True, show=title("DELF köşesi") + note(
    "Yazılı sınavın ikinci bölümünde kısa bir mesaj yazmak istenir (yaklaşık 40 kelime). Bunu 10. modülde çalışacağız.", kind="not", y=360),
              say=TR("Yazılı sınavın ikinci bölümünde kısa bir mesaj yazmak istenir. Bunu onuncu modülde çalışacağız."), pause=0.8))
SCENES.append(scene("DELF köşesi", b))

# =============================================================================
# 11. Mini test
# =============================================================================
QUIZ = [("« 20 yaşındayım » nasıl denir?", ["J'ai vingt ans.", "Je suis vingt ans.", "J'ai vingt."], 0,
         "Doğru cevap: je veⁿ taⁿ. Yaş avuar ile ve an kelimesiyle söylenir.", None),
        ("J'habite ___ Turquie.", ["à", "en", "au"], 1, "Doğru cevap: aⁿ. Türkiye dişil bir ülke.", None),
        ("___ est votre adresse ?", ["Quel", "Quelle", "Où"], 1, "Doğru cevap: ikinci seçenek. Adres dişil bir isim.", None),
        ("Dinle: hangi sayı?", ["80", "24", "90"], 0, "Doğru cevap: seksen. Katr veⁿ, yani dört kere yirmi.", "quiz/m2-q01.mp3"),
        ("Formda « Nationalité » kutusuna Türk bir erkek ne yazar?", ["turc", "turque", "Turquie"], 1,
         "Doğru cevap: ikinci seçenek. Nasyonalite dişil bir kelime.", None)]
QSAY = ["Yirmi yaşındayım nasıl denir?", "Boşluğa hangi edat gelir?", "Boşluğa hangi kelime gelir?", "Dinle: hangi sayı?",
        "Formda nasyonalite kutusuna Türk bir erkek ne yazar?"]
b = [beat(show=title("Mini test: 5 soru"), say=TR("Şimdi kendini test etme zamanı. Beş soru var. Her soru için beş saniyen olacak."), pause=0.4)]
for i, (q, opts, ok, expl, audio) in enumerate(QUIZ, 1):
    show = [Badge("qn", f"Soru {i} / {len(QUIZ)}", 120, 120, size=28, fill="tint", color="brand_dark"),
            T("qq", q, CX, 260, size=56, align="center", max_w=1600)]
    for k, o in enumerate(opts):
        x = 140 + k * 560
        show += [Box(f"ob{k}", x, 450, 520, 150, fill="card"), T(f"ot{k}", o, x + 260, 495, size=38, align="center", max_w=480)]
    says = [TR(QSAY[i - 1])] + ([F(audio)] if audio else [])
    b.append(beat(clear=True, show=show, say=says, pause=0.2))
    b.append(beat(show=Countdown("cd", 560, 700, 800), wait=5))
    b.append(beat(hide=["cd"], show=[Box(f"ob{ok}", 140 + ok * 560, 450, 520, 150, fill="ok_tint", outline="ok", width=4),
                                     T(f"ot{ok}", opts[ok], 140 + ok * 560 + 260, 495, size=38, color="ok", align="center", max_w=480),
                                     T("ex", expl, CX, 700, size=34, font="regular", color="soft", align="center", max_w=1600)],
                  say=TR(expl), pause=0.6))
SCENES.append(scene("Mini test", b))

# =============================================================================
# 12. Kapanış
# =============================================================================
SCENES.append(scene("Kapanış", [
    beat(show=title("Bugün neler öğrendik?") + [
        T("r1", "•  Yaşını söylemek: [avoir|hl] fiili", 140, 280, size=44),
        T("r2", "•  [quel|hl], [où|hl], [comment|hl], [combien|hl] ile soru sormak", 140, 370, size=44),
        T("r3", "•  Şehirler ve ülkeler: [à|hl], [en|hl], [au|hl]", 140, 460, size=44),
        T("r4", "•  0'dan 1000'e sayılar ve telefon numarası", 140, 550, size=44),
        T("r5", "•  DELF yazılı sınavı: form doldurma", 140, 640, size=44)],
         say=TR("Bugün yaşını söylemeyi ve avuar fiilini, soru sormayı, şehir ve ülkelerle doğru edatı, sıfırdan bine kadar sayıları "
                "ve DELF yazılı sınavındaki form doldurmayı öğrendik."), pause=0.5),
    beat(show=Badge("url", "Alıştırmalar, kelime testi ve modül testi:  kolayfransizca.app", 140, 760, size=34, fill="gold", color="ink"),
         say=TR("Şimdi sıra alıştırmalarda. Sitemizde bu modülün alıştırmalarını, kelime testini, kendi kayıt formunu doldurma ödevini "
                "ve DELF tarzı testi ücretsiz olarak bulabilirsin."), pause=0.5),
    beat(clear=True, show=[T("t1", "Bu kurs tamamen [ücretsiz|hl].", CX, 300, size=64, font="display", align="center"),
                           T("t2", "Teşekkür etmenin en güzel yolu: kanala abone olmak.", CX, 420, size=44, align="center"),
                           Badge("nx", "Sonraki ders: Modül 3 · Ailem ve çevremdeki insanlar", CX, 600, size=34, fill="tint", color="brand_dark", align="center")],
         say=[TR("Bu kurs tamamen ücretsiz. Bana teşekkür etmenin en güzel yolu kanala abone olmak. Üçüncü modülde, ailemizi tanıtmayı öğreneceğiz. "
                 "Görüşmek üzere!")], pause=1.5),
]))
