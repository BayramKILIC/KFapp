# -*- coding: utf-8 -*-
"""Contenu des fiches résumé, module par module. Balisage [mot|style] : hl (violet), no (rouge), ok (vert), gold, mute (barré)."""

M1_GRAMMAR = [
    """<div class="grid2">
  <div class="box"><h2><span class="n">1</span>« Tu » mu, « vous » mu?</h2>
    <div class="vs"><div class="a"><b class="big">tu = sen</b><span class="sm">arkadaş, aile, çocuk, yaşıt</span><br>
      <span class="fr">Salut ! Tu t'appelles comment ?</span><br><span class="tr sm">Selam! Adın ne?</span></div>
    <div class="b"><b class="big">vous = siz</b><span class="sm">tanımadığın kişi, büyükler, resmi</span><br>
      <span class="fr">Bonjour ! Vous vous appelez comment ?</span><br><span class="tr sm">Merhaba! Adınız ne?</span></div></div>
    <p class="sm" style="margin-top:1.6mm">Emin değilsen her zaman <b>vous</b> kullan.</p></div>
  <div class="box"><h2><span class="n">2</span>Sıfat kişiye uyar</h2>
    <table class="mf"><tr><th class="m">Erkek</th><th class="f">Kadın</th><th class="t">Türkçe</th></tr>
      <tr><td>Je suis turc.</td><td>Je suis tur<span class="no">que</span>.</td><td class="tr">Türküm.</td></tr>
      <tr><td>Je suis content.</td><td>Je suis content<span class="no">e</span>.</td><td class="tr">Mutluyum.</td></tr>
      <tr><td>Enchanté !</td><td>Enchanté<span class="no">e</span> !</td><td class="tr">Memnun oldum!</td></tr>
      <tr><td>Je suis désolé.</td><td>Je suis désolé<span class="no">e</span>.</td><td class="tr">Üzgünüm.</td></tr></table>
    <p class="sm" style="margin-top:1.4mm">Genel kural: dişil için sona <b>e</b> eklenir. « content » kelimesinde t okunmaz, « contente » kelimesinde okunur.</p></div>
</div>""",
    """<div class="grid3">
  <div class="box"><h2><span class="n">3</span>être <span class="tr sm">(olmak)</span></h2><table class="conj">
    <tr><td>je</td><td>suis</td></tr><tr><td>tu</td><td>es</td></tr>
    <tr><td>il / elle</td><td>est</td></tr><tr><td>nous</td><td>sommes</td></tr>
    <tr><td>vous</td><td>êtes</td></tr><tr><td>ils / elles</td><td>sont</td></tr></table></div>
  <div class="box"><h2><span class="n">4</span>s'appeler <span class="tr sm">(adı ... olmak)</span></h2><table class="conj">
    <tr><td>je</td><td>m'appelle</td></tr><tr><td>tu</td><td>t'appelles</td></tr>
    <tr><td>il / elle</td><td>s'appelle</td></tr><tr><td>nous</td><td>nous appelons</td></tr>
    <tr><td>vous</td><td>vous appelez</td></tr><tr><td>ils / elles</td><td>s'appellent</td></tr></table></div>
  <div class="box"><h2><span class="n">5</span>Vurgulu zamirler</h2>
    <p><span class="fr"><span class="hl">Moi</span>, je m'appelle Emre.</span><br><span class="tr sm">Ben, benim adım Emre.</span></p>
    <p style="margin-top:1.4mm"><span class="fr">Et <span class="hl">toi</span> ?</span> <span class="tr sm">Ya sen?</span></p>
    <p style="margin-top:1.4mm"><span class="fr">Et <span class="hl">vous</span> ?</span> <span class="tr sm">Ya siz?</span></p>
    <p class="sm" style="margin-top:1.8mm">Kişiyi vurgulamak veya soruyu geri sormak için.</p></div>
</div>""",
    """<div class="box"><h2><span class="n">6</span>Alfabe: adını harf harf söyle</h2>
  <div class="abc">""" + "".join(
        f'<div class="{"hard" if l in "EGJQRUWY" else ""}"><b>{l}</b><span>{o}</span></div>'
        for l, o in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                        ["a", "be", "se", "de", "ö", "ef", "je", "aş", "i", "ji", "ka", "el", "em", "en", "o", "pe", "kü",
                         "er", "es", "te", "ü", "ve", "dubl ve", "iks", "igrek", "zed"])) + """</div>
  <p class="sm" style="margin-top:1.6mm"><span class="fr">Vous pouvez épeler votre nom, s'il vous plaît ?</span> <span class="tr">Adınızı harf harf söyleyebilir misiniz?</span>
  · Sarı harfler Türkçeden en farklı okunanlar.</p></div>""",
]

M1_TELAFFUZ = """<div class="box"><h3>Telaffuz: sondaki harf</h3>
  <p class="sm">Sondaki <b>-s, -t, -x, -d, -z, -p</b> çoğu zaman okunmaz:
  salu<span class="mute">t</span>, vou<span class="mute">s</span>, commen<span class="mute">t</span>, deu<span class="mute">x</span>.</p>
  <p class="sm" style="margin-top:1mm"><b>-c, -r, -f, -l</b> genelde okunur (« CaReFuL »): ave<span class="hl">c</span>, bonjou<span class="hl">r</span>, neu<span class="hl">f</span>, i<span class="hl">l</span>.
  İstisna: -er fiiller (répéte<span class="mute">r</span>).</p>
  <p class="sm" style="margin-top:1mm">Dişil « e » harfi önceki harfi okutur: françai<span class="mute">s</span> / françai<span class="hl">s</span>e.</p></div>"""

MODULES = {
    1: dict(
        num=1, title="Selamlaşma ve tanışma", title_fr="Saluer et se présenter",
        video="https://youtu.be/q2jWhZZVggY",
        goals=[
            "Günün saatine göre selam verip vedalaşmak",
            "« tu » ve « vous » arasında seçim yapmak",
            "Adımı söylemek, karşımdakinin adını sormak",
            "Birini tanıştırmak",
            "Teşekkür etmek ve özür dilemek",
            "Adımı harf harf söylemek",
            "Anlamadığımda tekrar etmesini istemek",
            "« être » ve « s'appeler » fiillerini çekmek",
            "« moi, toi, vous » vurgulu zamirlerini kullanmak",
            "Kendimi tanıtan 3-4 cümle yazmak",
        ],
        grammar=M1_GRAMMAR,
        phrases=[
            ("Bonjour ! Je m'appelle Elif.", "Merhaba! Benim adım Elif."),
            ("Et toi, tu t'appelles comment ?", "Ya sen, senin adın ne?"),
            ("Pardon ? Tu peux répéter, s'il te plaît ?", "Pardon? Tekrar edebilir misin, lütfen?"),
            ("Emre. E, M, R, E.", "Emre. E, M, R, E."),
            ("Enchanté. / Enchantée.", "Memnun oldum."),
            ("Ça va très bien, merci. Et toi ?", "Çok iyiyim, teşekkürler. Ya sen?"),
            ("Voilà notre professeur, madame Martin.", "İşte öğretmenimiz, Bayan Martin."),
            ("Vous êtes Elif et Emre ? Oui, madame.", "Siz Elif ve Emre misiniz? Evet, hanımefendi."),
        ],
        voc_must=[
            ("bonjour", "boⁿjur", "merhaba / günaydın"), ("bonsoir", "boⁿsuar", "iyi akşamlar"),
            ("salut", "salü", "selam"), ("au revoir", "o rövuar", "hoşça kal"),
            ("merci", "mersi", "teşekkürler"), ("s'il vous plaît", "sil vu ple", "lütfen (resmi)"),
            ("pardon", "pardoⁿ", "pardon"), ("excusez-moi", "eksküze mua", "affedersiniz"),
            ("oui", "ui", "evet"), ("non", "noⁿ", "hayır"),
            ("monsieur", "mösyö", "bey / beyefendi"), ("madame", "madam", "hanım / hanımefendi"),
            ("le nom", "lö noⁿ", "soyad"), ("le prénom", "lö prenoⁿ", "ad"),
            ("je m'appelle", "jö mapel", "benim adım..."), ("comment", "komaⁿ", "nasıl"),
            ("et toi ?", "e tua", "ya sen?"), ("et vous ?", "e vu", "ya siz?"),
            ("enchanté / enchantée", "aⁿşaⁿte", "memnun oldum"), ("ça va ?", "sa va", "nasılsın?"),
            ("très bien", "tre byeⁿ", "çok iyi"), ("être", "etr", "olmak"),
            ("répéter", "repete", "tekrar etmek"), ("épeler", "eple", "harf harf söylemek"),
            ("moi", "mua", "ben"), ("toi", "tua", "sen"),
        ],
        voc_rec=[
            ("à bientôt", "a byeⁿto", "yakında görüşürüz"), ("à demain", "a dömeⁿ", "yarın görüşürüz"),
            ("bonne journée", "bon jurne", "iyi günler"), ("bonne soirée", "bon suare", "iyi akşamlar"),
            ("s'il te plaît", "sil tö ple", "lütfen (samimi)"), ("désolé / désolée", "dezole", "üzgünüm"),
            ("content / contente", "koⁿtaⁿ / koⁿtaⁿt", "mutlu"), ("lentement", "laⁿtmaⁿ", "yavaşça"),
            ("comprendre", "koⁿpraⁿdr", "anlamak"), ("voilà", "vuala", "işte"),
        ],
        telaffuz=M1_TELAFFUZ,
        tips=[
            "Bir dükkâna veya ofise girince önce « Bonjour » de. Selam vermeden bir şey istemek kaba sayılır.",
            "« Je m'appelle » kalıbını şimdilik olduğu gibi ezberle.",
            "Her kelimeyi mutlaka sesiyle birlikte öğren: « salut » kelimesinde « t » söylenmez.",
        ],
        delf=dict(
            title="Sözlü sınav, 1. bölüm",
            points=[
                "Görevliyi selamla ve ona « vous » ile hitap et.",
                "Sadece « Oui » deme, kısa ve tam bir cümle kur: « Oui, je suis turc. »",
                "Anlamadığında sessiz kalma, tekrar etmesini iste.",
                "Sonunda vedalaşmayı unutma: « Merci, au revoir ! »",
            ],
            key="« Pardon, vous pouvez répéter, s'il vous plaît ? »",
            key_tr="Pardon, tekrar edebilir misiniz, lütfen?",
        ),
    ),
}

def _nums(items):
    return '<div class="nums">' + "".join(f"<div><b>{n}</b><span>{w}</span></div>" for n, w in items) + "</div>"


M2_GRAMMAR = [
    """<div class="grid2">
  <div class="box"><h2><span class="n">1</span>avoir <span class="tr sm">(sahip olmak)</span></h2>
    <table class="conj"><tr><td>j'</td><td>ai</td></tr><tr><td>tu</td><td>as</td></tr><tr><td>il / elle</td><td>a</td></tr>
    <tr><td>nous</td><td>avons</td></tr><tr><td>vous</td><td>avez</td></tr><tr><td>ils / elles</td><td>ont</td></tr></table>
    <p class="sm" style="margin-top:1.4mm">je + ai = <b>j'ai</b>. Yaş <b>avoir</b> ile söylenir:</p>
    <p><span class="fr"><span class="hl">J'ai</span> vingt-huit <span class="hl">ans</span>.</span> <span class="tr sm">28 yaşındayım.</span></p>
    <p class="sm"><span class="mute">Je suis vingt-huit ans.</span> <span class="no">Yanlış</span> · « ans » kelimesini unutma.</p></div>
  <div class="box"><h2><span class="n">2</span>Soru kelimeleri</h2>
    <table class="kv">
      <tr><td>quel / quelle</td><td>hangi, ne<br><span class="fr">Quelle est votre adresse ?</span><br><span class="tr sm">Adresiniz nedir?</span></td></tr>
      <tr><td>où</td><td>nerede<br><span class="fr">Vous habitez où ?</span> <span class="tr sm">Nerede oturuyorsunuz?</span></td></tr>
      <tr><td>comment</td><td>nasıl<br><span class="fr">Vous vous appelez comment ?</span> <span class="tr sm">Adınız ne?</span></td></tr>
      <tr><td>combien</td><td>kaç, ne kadar<br><span class="fr">Vous avez combien d'enfants ?</span> <span class="tr sm">Kaç çocuğunuz var?</span></td></tr></table>
    <p class="sm" style="margin-top:1.2mm">Eril isim: <b>quel</b> âge · dişil isim: <b>quelle</b> nationalité. İkisi de [kel] okunur.</p></div>
</div>""",
    """<div class="grid2">
  <div class="box"><h2><span class="n">3</span>Nerede? à, en, au, aux</h2>
    <table class="kv">
      <tr><td>à + şehir</td><td><span class="fr">J'habite à Lyon.</span> <span class="tr sm">à Paris, à Kayseri</span></td></tr>
      <tr><td>en + dişil ülke</td><td><span class="fr">J'habite en France.</span> <span class="tr sm">en Turquie</span></td></tr>
      <tr><td>au + eril ülke</td><td><span class="fr">J'habite au Canada.</span> <span class="tr sm">au Maroc</span></td></tr>
      <tr><td>aux + çoğul ülke</td><td><span class="fr">J'habite aux États-Unis.</span></td></tr></table>
    <p class="sm" style="margin-top:1.2mm">« e » ile biten ülkeler genelde dişildir: la France, la Turquie. İstisna: le Mexique.</p></div>
  <div class="box"><h2><span class="n">4</span>Nereli? venir de</h2>
    <table class="kv">
      <tr><td>de / d'</td><td><span class="fr">Je viens d'Ankara.</span> <span class="tr sm">şehir</span></td></tr>
      <tr><td>de</td><td><span class="fr">Je viens de Turquie.</span> <span class="tr sm">dişil ülke</span></td></tr>
      <tr><td>du</td><td><span class="fr">Il vient du Maroc.</span> <span class="tr sm">eril ülke (de + le)</span></td></tr>
      <tr><td>des</td><td><span class="fr">Elle vient des États-Unis.</span> <span class="tr sm">çoğul (de + les)</span></td></tr></table></div>
</div>""",
    """<div class="box"><h2><span class="n">5</span>Uyruk ve meslek kişiye uyar</h2>
  <div class="grid2"><table class="mf"><tr><th class="m">Erkek</th><th class="f">Kadın</th><th class="t">Kural</th></tr>
      <tr><td>français</td><td>français<span class="no">e</span></td><td class="tr sm">sona « e » eklenir</td></tr>
      <tr><td>étudiant</td><td>étudiant<span class="no">e</span></td><td class="tr sm">son harf okunur olur</td></tr>
      <tr><td>algér<span class="hl">ien</span></td><td>algér<span class="no">ienne</span></td><td class="tr sm">-ien → -ienne</td></tr></table>
    <table class="mf"><tr><th class="m">Erkek</th><th class="f">Kadın</th><th class="t">Kural</th></tr>
      <tr><td>vend<span class="hl">eur</span></td><td>vend<span class="no">euse</span></td><td class="tr sm">-eur → -euse</td></tr>
      <tr><td>belge</td><td>belge</td><td class="tr sm">« e » ile biten değişmez</td></tr>
      <tr><td>turc</td><td>tur<span class="no">que</span></td><td class="tr sm">düzensiz</td></tr></table></div>
  <p class="sm" style="margin-top:1.4mm">Uyruk küçük harfle yazılır (<b>turc</b>), ülke büyük harfle (<b>la Turquie</b>). « né / née » da uyar, okunuşu aynıdır.</p></div>""",
    """<div class="grid2"><div class="box"><h2><span class="n">6</span>Telaffuz: bağlama (liaison)</h2>
  <p class="sm">Sesli harften önce son harf okunur ve bağlanır:
  u<span class="hl">n</span>‿an [n] · deu<span class="hl">x</span>‿ans [z] · troi<span class="hl">s</span>‿ans [z] · neu<span class="hl">f</span>‿ans [v] · ving<span class="hl">t</span>‿ans [t]</p>
  <p class="sm" style="margin-top:1mm"><b>six / dix</b>: tek başına [s] · six‿ans [z] · si<span class="mute">x</span> livres okunmaz.</p></div>
  <div class="tip"><b>Öğretmenin tavsiyesi</b>Yaş « avoir » ile söylenir: « J'ai 30 ans ». « Je suis 30 ans » en sık yapılan hatalardan biridir.</div></div>""",
]

M2_SAYILAR = """<div class="box"><h3>Sayılar 0 – 1000</h3>""" + _nums([
    (0, "zéro"), (1, "un"), (2, "deux"), (3, "trois"), (4, "quatre"), (5, "cinq"), (6, "six"), (7, "sept"), (8, "huit"), (9, "neuf"),
    (10, "dix"), (11, "onze"), (12, "douze"), (13, "treize"), (14, "quatorze"), (15, "quinze"), (16, "seize"), (17, "dix-sept"),
    (18, "dix-huit"), (19, "dix-neuf"), (20, "vingt"), (21, "vingt et un"), (30, "trente"), (40, "quarante"), (50, "cinquante"),
    (60, "soixante"), (100, "cent"), (1000, "mille")]) + """
  <p class="sm" style="margin-top:1.4mm"><b>70</b> soixante-dix (60+10) · <b>80</b> quatre-vingts (4×20) · <b>90</b> quatre-vingt-dix (4×20+10)</p>
  <p class="sm">21, 31… 71: <b>et</b> ile (vingt <b>et</b> un) · 81 ve 91: « et » yok (quatre-vingt-un).</p>
  <p class="sm" style="margin-top:1mm">Telefon ikişer ikişer okunur: <b>06 45 18 72 30</b> = zéro six · quarante-cinq · dix-huit · soixante-douze · trente.
  E-posta: <b>@</b> = arobase, <b>.</b> = point.</p></div>"""

MODULES[2] = dict(
    num=2, title="Kişisel bilgilerim", title_fr="Mes informations",
    video="https://youtu.be/KFqDUPxwHSQ",
    goals=[
        "Yaşımı söylemek ve yaş sormak",
        "1000'e kadar saymak ve sayıları anlamak",
        "Uyruğumu ve ülkemi söylemek",
        "Nerede yaşadığımı ve nereli olduğumu söylemek",
        "Mesleğimi ve medeni durumumu söylemek",
        "« avoir » fiilini çekmek",
        "« quel, où, comment, combien » ile soru sormak",
        "Adresimi, telefonumu ve e-postamı vermek",
        "Kişisel bilgilerimle bir form doldurmak",
        "Sayılarla bağlamayı duymak: deux‿ans",
    ],
    grammar=M2_GRAMMAR,
    phrases=[],
    voc_must=[
        ("avoir", "avuar", "sahip olmak"), ("l'âge", "laj", "yaş"),
        ("un an", "öⁿ naⁿ", "yıl / yaş"), ("habiter", "abite", "oturmak / yaşamak"),
        ("l'adresse", "ladres", "adres"), ("la ville", "la vil", "şehir"),
        ("le pays", "lö pei", "ülke"), ("la nationalité", "la nasyonalite", "uyruk"),
        ("turc / turque", "türk", "Türk"), ("français / française", "fraⁿse / fraⁿsez", "Fransız"),
        ("la Turquie", "la türki", "Türkiye"), ("la France", "la fraⁿs", "Fransa"),
        ("venir de", "vönir dö", "-den gelmek"), ("né / née", "ne", "doğmuş"),
        ("la date de naissance", "la dat dö nesaⁿs", "doğum tarihi"), ("la profession", "la profesyoⁿ", "meslek"),
        ("travailler", "travaye", "çalışmak"), ("étudiant / étudiante", "etüdyaⁿ(t)", "öğrenci"),
        ("marié / mariée", "marye", "evli"), ("célibataire", "selibater", "bekâr"),
        ("le numéro de téléphone", "nümero dö telefon", "telefon numarası"), ("le courriel", "lö kuryel", "e-posta"),
        ("parler", "parle", "konuşmak"), ("un, deux, trois", "öⁿ, dö, trua", "bir, iki, üç"),
        ("dix", "dis", "on"), ("vingt", "veⁿ", "yirmi"),
        ("cent", "saⁿ", "yüz"), ("mille", "mil", "bin"),
        ("quel / quelle", "kel", "hangi / ne"), ("où", "u", "nerede"),
        ("combien", "koⁿbyeⁿ", "kaç / ne kadar"),
    ],
    voc_rec=[
        ("la rue", "la rü", "sokak / cadde"), ("le professeur", "lö profesör", "öğretmen"),
        ("ingénieur / ingénieure", "eⁿjenyör", "mühendis"), ("le médecin", "lö medseⁿ", "doktor"),
        ("vendeur / vendeuse", "vaⁿdör / vaⁿdöz", "satış elemanı"), ("ouvrier / ouvrière", "uvriye / uvriyer", "işçi"),
        ("la langue", "la laⁿg", "dil"), ("le formulaire", "lö formüler", "form"),
        ("la signature", "la sinyatür", "imza"),
    ],
    telaffuz=M2_SAYILAR,
    tips=[],
    delf=dict(
        title="Yazılı sınav, 1. alıştırma",
        points=[
            "Sınavın ilk alıştırması bir form doldurmaktır (kayıt formu, üyelik kartı, otel fişi).",
            "Ülke ve şehir adlarını Fransızca yaz: [Turquie|hl], « Türkiye » değil.",
            "« Nationalité » dişildir: erkek için de [Nationalité : turque|hl] yaz.",
            "Tarih sırası Türkçedeki gibidir: gün, ay, yıl (05/05/1995).",
            "Her kutuyu doldur, istenmeyen bilgi yazma.",
        ],
        key="Nom · Prénom · Âge · Nationalité · Adresse · Profession · Téléphone · Courriel",
        key_tr="Formda mutlaka tanıman gereken kelimeler",
    ),
)
