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


M3_P1 = [
    """<div class="box"><h2><span class="n">1</span>İyelik sıfatları: mon, ma, mes</h2>
  <div class="grid2" style="grid-template-columns:1.25fr 1fr;align-items:start">
  <table class="mf"><tr><th class="t"></th><th class="m">Eril tekil</th><th class="f">Dişil tekil</th><th class="t">Çoğul</th></tr>
    <tr><td class="tr">benim</td><td><span class="hl">mon</span> père</td><td><span class="no">ma</span> mère</td><td><b>mes</b> parents</td></tr>
    <tr><td class="tr">senin</td><td><span class="hl">ton</span> frère</td><td><span class="no">ta</span> sœur</td><td><b>tes</b> amis</td></tr>
    <tr><td class="tr">onun</td><td><span class="hl">son</span> fils</td><td><span class="no">sa</span> fille</td><td><b>ses</b> enfants</td></tr>
    <tr><td class="tr">bizim</td><td colspan="2"><b>notre</b> famille</td><td><b>nos</b> enfants</td></tr>
    <tr><td class="tr">sizin</td><td colspan="2"><b>votre</b> nom</td><td><b>vos</b> parents</td></tr>
    <tr><td class="tr">onların</td><td colspan="2"><b>leur</b> fille</td><td><b>leurs</b> enfants</td></tr></table>
  <div class="sm">
    <p><b>Sahip olunan şeye bakılır:</b> « père » eril → <b>mon</b> père; « mère » dişil → <b>ma</b> mère. Bir kadın da « mon père » der.</p>
    <p style="margin-top:1.2mm"><b>Çoğulda tek biçim:</b> mes frères, mes sœurs.</p>
    <p style="margin-top:1.2mm"><b>Sesli harften önce</b> ma → <b>mon</b>: mon amie, ton amie, son amie.</p>
    <p style="margin-top:1.2mm"><b>son, sa, ses</b> = « onun »: sahibin erkek mi kadın mı olduğunu söylemez.</p></div></div></div>""",
    """<div class="grid2">
  <div class="box"><h2><span class="n">2</span>Eril, dişil, çoğul</h2>
    <table class="mf"><tr><th class="m">Eril</th><th class="f">Dişil</th></tr>
      <tr><td>le père</td><td>la mère</td></tr><tr><td>le frère</td><td>la sœur</td></tr>
      <tr><td>le fils</td><td>la fille</td></tr><tr><td>le mari</td><td>la femme</td></tr>
      <tr><td>le cousin</td><td>la cousine</td></tr><tr><td>l'ami</td><td>l'amie <span class="tr sm">(aynı okunur)</span></td></tr></table>
    <p class="sm" style="margin-top:1.4mm">Çoğul: <b>les</b> + isim + <b>s</b> (s okunmaz): les frère<span class="mute">s</span>. Duyduğun fark « le / les ».<br>
    les‿enfants [z] bağlanır · un œil → <b>les yeux</b> · saç hep çoğul: <b>les cheveux</b>.</p></div>
  <div class="box"><h2><span class="n">3</span>Sıfat kişiye uyar</h2>
    <table class="mf"><tr><th class="m">Erkek</th><th class="f">Kadın</th><th class="t">Kural</th></tr>
      <tr><td>grand</td><td>grand<span class="no">e</span></td><td class="tr sm">sona « e »</td></tr>
      <tr><td>âgé</td><td>âgé<span class="no">e</span></td><td class="tr sm">sona « e »</td></tr>
      <tr><td>jeune</td><td>jeune</td><td class="tr sm">« e » ile biten değişmez</td></tr>
      <tr><td>genti<span class="hl">l</span></td><td>genti<span class="no">lle</span></td><td class="tr sm">son harf ikilenir</td></tr>
      <tr><td>sérieu<span class="hl">x</span></td><td>sérieu<span class="no">se</span></td><td class="tr sm">-eux → -euse</td></tr>
      <tr><td>beau</td><td><span class="no">belle</span></td><td class="tr sm">düzensiz</td></tr></table>
    <p class="sm" style="margin-top:1.4mm">Çoğulda sona <b>s</b>: Ils sont grand<span class="hl">s</span>. Elles sont petite<span class="hl">s</span>.</p></div>
</div>""",
    """<div class="box"><h2><span class="n">4</span>Sıfat nereye gelir?</h2>
  <div class="grid2">
    <div class="sm"><p>Çoğu sıfat <b>isimden sonra</b> gelir:</p>
      <p><span class="fr">une femme <span class="hl">blonde</span></span> <span class="tr">sarışın bir kadın</span></p>
      <p><span class="fr">un ami <span class="hl">sympathique</span></span> <span class="tr">sempatik bir arkadaş</span></p></div>
    <div class="sm"><p>Kısa sıfatlar <b>önce</b> gelir: grand, petit, jeune, beau.</p>
      <p><span class="fr">un <span class="hl">grand</span> frère</span> <span class="tr">ağabey</span> · <span class="fr">une <span class="hl">petite</span> sœur</span> <span class="tr">küçük kız kardeş</span></p>
      <p><span class="fr">une <span class="hl">belle</span> photo</span> <span class="tr">güzel bir fotoğraf</span></p></div></div></div>""",
]

_TREE = """<div class="tree">
  <div class="row"><div class="p m"><b>Mehmet</b><span>le grand-père</span></div><span class="plus">+</span><div class="p f"><b>Zeynep</b><span>la grand-mère</span></div></div>
  <div class="row"><div class="p m"><b>Ahmet</b><span>le père</span></div><span class="plus">+</span><div class="p f"><b>Fatma</b><span>la mère</span></div><div class="p f"><b>Selma</b><span>la tante</span></div></div>
  <div class="row"><div class="p me"><b>Emre</b><span>moi</span></div><div class="p f"><b>Elif</b><span>la sœur</span></div><div class="p m"><b>Deniz</b><span>le frère</span></div></div>
</div>"""

M3_P2 = [
    """<div class="grid2">
  <div class="box"><h2><span class="n">5</span>Qui est-ce ? Birini tanıtmak</h2>
    <table class="kv">
      <tr><td>Qui est-ce ?</td><td><span class="fr">C'est mon père.</span> <span class="tr sm">Bu kim? Bu benim babam.</span></td></tr>
      <tr><td>c'est + 1 kişi</td><td><span class="fr">C'est ma sœur Elif.</span></td></tr>
      <tr><td>ce sont + 2+ kişi</td><td><span class="fr">Ce sont mes parents.</span></td></tr>
      <tr><td>voici / voilà</td><td><span class="fr">Voici mon mari.</span> <span class="tr sm">İşte eşim.</span></td></tr>
      <tr><td>lui / elle</td><td><span class="fr">Lui, c'est mon frère.</span><br><span class="fr">Elle, c'est ma tante.</span></td></tr></table>
    <p class="sm" style="margin-top:1.2mm">Kişiyi sormak: <b>Il / Elle est comment ?</b> <span class="tr">O nasıl biri?</span></p></div>
  <div class="box"><h2><span class="n">6</span>être mi, avoir mı?</h2>
    <p class="sm">Kişiyi anlatırken <b>être</b>:</p>
    <p><span class="fr">Il <span class="hl">est</span> grand et brun.</span> <span class="tr sm">O uzun boylu ve esmer.</span></p>
    <p><span class="fr">Elle <span class="hl">est</span> gentille.</span> <span class="tr sm">O iyi kalpli.</span></p>
    <p class="sm" style="margin-top:1.4mm">Saç ve gözler için <b>avoir</b>:</p>
    <p><span class="fr">Il <span class="ok">a</span> les cheveux bruns.</span> <span class="tr sm">Saçları kahverengi.</span></p>
    <p><span class="fr">Elle <span class="ok">a</span> les yeux verts.</span> <span class="tr sm">Gözleri yeşil.</span></p>
    <p class="sm" style="margin-top:1mm"><span class="mute">Il est les cheveux bruns.</span> <span class="no">Yanlış</span></p></div>
</div>""",
    """<div class="box"><h2><span class="n">7</span>Aile ağacı ve « de » (-nin)</h2>
  <div class="grid2" style="grid-template-columns:1.1fr 1fr;align-items:center">""" + _TREE + """
    <div class="sm">
      <p><span class="fr">Ahmet est <span class="hl">le mari de</span> Fatma.</span><br><span class="tr">Ahmet, Fatma'nın kocası.</span></p>
      <p style="margin-top:1.2mm"><span class="fr">Selma est la tante <span class="hl">d'</span>Emre.</span><br><span class="tr">Selma, Emre'nin halası. (sesli harften önce d')</span></p>
      <p style="margin-top:1.2mm"><span class="fr">Emre et Elif sont frère et sœur.</span><br><span class="tr">Emre ve Elif kardeş.</span></p>
      <p style="margin-top:1.2mm"><span class="fr">Ahmet et Fatma sont mariés.</span><br><span class="tr">Ahmet ve Fatma evli.</span></p>
      <p style="margin-top:1.4mm">amca, dayı → <b>l'oncle</b> · hala, teyze → <b>la tante</b></p></div></div></div>""",
    """<div class="grid2">
  <div class="tip"><b>Öğretmenin tavsiyesi</b>Bir fotoğrafı anlatmak için iki soru yeter: « Qui est-ce ? » (Bu kim?) ve « Il / Elle est comment ? » (O nasıl biri?). Kendi aile fotoğraflarından birini aç ve her kişi için bu iki soruya Fransızca cevap ver.</div>
  <div class="tip"><b>Öğretmenin tavsiyesi</b>« mon, ma, mes » sahip olana göre değil, sahip olunan şeye göre değişir. Kendine şu soruyu sor: « Bu isim eril mi, dişil mi? »</div>
</div>""",
]

M3_TELAFFUZ = """<div class="box"><h3>Telaffuz: petit / petite</h3>
  <p class="sm">Dişil « e » okunmaz ama önceki harfi okutur. Dişili sondaki sesten duyarsın:</p>
  <p class="sm" style="margin-top:1mm">peti<span class="mute">t</span> → peti<span class="hl">t</span>e · gran<span class="mute">d</span> → gran<span class="hl">d</span>e · blon<span class="mute">d</span> → blon<span class="hl">d</span>e · sérieu<span class="mute">x</span> → sérieu<span class="hl">s</span>e</p>
  <p class="sm" style="margin-top:1mm"><b>âgé / âgée</b> aynı okunur · <b>jeune</b> değişmez · <b>brun / brune</b>: erkekte genizden gelen ses var, kadında kaybolur ve n okunur · <b>beau / belle</b> [bo] / [bel].</p></div>"""

MODULES[3] = dict(
    num=3, title="Ailem ve çevremdeki insanlar", title_fr="Ma famille, les gens",
    video="https://youtu.be/H2VOmLVxmAA",
    goals=[
        "Aile üyelerimi adlandırmak",
        "« mon, ma, mes » iyelik sıfatlarını kullanmak",
        "Eril / dişil, tekil / çoğul ayırt etmek",
        "Sıfatı uyumlu yapmak ve doğru yere koymak",
        "Bir kişinin görünüşünü ve karakterini anlatmak",
        "« Qui est-ce ? C'est... » ile birini sormak, tanıtmak",
        "İki kişi arasındaki ilişkiyi söylemek: le mari de Fatma",
        "« lui » ve « elle » ile birini göstermek",
        "Bir aileyi tanıtan kısa bir metni anlamak",
        "Ailemi tanıtan 4-5 cümle yazmak",
    ],
    grammar_pages=[M3_P1, M3_P2],
    phrases=[
        ("C'est une photo de ta famille ?", "Bu senin ailenin fotoğrafı mı?"),
        ("Et lui, qui est-ce ?", "Peki bu (erkek) kim?"),
        ("Lui, c'est mon père. Il est grand et très gentil.", "O benim babam. Uzun boylu ve çok iyi kalpli."),
        ("Voici ma mère : elle est petite et brune.", "İşte annem: kısa boylu ve esmer."),
        ("Ce sont ma sœur Elif et mon frère Deniz.", "Bunlar kız kardeşim Elif ve erkek kardeşim Deniz."),
        ("Ta sœur a quel âge ? Elle a vingt-six ans.", "Kız kardeşin kaç yaşında? Yirmi altı yaşında."),
        ("Il est blond, comme ma tante.", "Halam gibi sarışın."),
        ("Tu as une grande famille !", "Kalabalık bir ailen var!"),
    ],
    voc_must=[
        ("la famille", "la famiy", "aile"), ("les parents", "le paraⁿ", "anne baba"),
        ("le père", "lö per", "baba"), ("la mère", "la mer", "anne"),
        ("le frère", "lö frer", "erkek kardeş"), ("la sœur", "la sör", "kız kardeş"),
        ("le fils", "lö fis", "oğul"), ("la fille", "la fiy", "kız (evlat)"),
        ("l'enfant", "laⁿfaⁿ", "çocuk"), ("le mari", "lö mari", "koca / eş"),
        ("la femme", "la fam", "kadın / eş"), ("l'ami / l'amie", "lami", "arkadaş"),
        ("grand / grande", "graⁿ / graⁿd", "uzun boylu / büyük"), ("petit / petite", "pöti / pötit", "kısa boylu / küçük"),
        ("jeune", "jön", "genç"), ("âgé / âgée", "aje", "yaşlı"),
        ("beau / belle", "bo / bel", "yakışıklı / güzel"), ("gentil / gentille", "jaⁿti / jaⁿtiy", "nazik / iyi kalpli"),
        ("sympathique", "seⁿpatik", "sempatik"), ("les cheveux", "le şövö", "saç"),
        ("les yeux", "le zyö", "gözler"), ("brun / brune", "bröⁿ / brün", "esmer / kumral"),
        ("blond / blonde", "bloⁿ / bloⁿd", "sarışın"), ("mon, ma, mes", "moⁿ, ma, me", "benim"),
        ("qui", "ki", "kim"), ("c'est", "se", "bu ...-dır"),
        ("lui", "lüi", "o (erkek)"), ("elle", "el", "o (kadın)"),
    ],
    voc_rec=[
        ("le grand-père", "lö graⁿ per", "dede"), ("la grand-mère", "la graⁿ mer", "büyükanne"),
        ("l'oncle", "loⁿkl", "amca / dayı"), ("la tante", "la taⁿt", "hala / teyze"),
        ("le cousin / la cousine", "kuzeⁿ / kuzin", "kuzen"), ("le voisin / la voisine", "vuazeⁿ / vuazin", "komşu"),
        ("sérieux / sérieuse", "seryö / seryöz", "ciddi"), ("drôle", "drol", "komik"),
        ("ensemble", "aⁿsaⁿbl", "birlikte"),
    ],
    telaffuz=M3_TELAFFUZ,
    tips=[
        "« la femme » hem « kadın » hem « eş », « la fille » hem « kız » hem « kız evlat » demektir. Anlamı cümleden çıkar: « Voici ma femme » = İşte eşim.",
        "Her sıfatı iki haliyle öğren: listende hep « petit / petite » diye yaz.",
    ],
    delf=dict(
        title="Okuduğunu anlama",
        points=[
            "Okuma sınavı 30 dakika, 25 puan. İlk metin çoğu zaman bir arkadaştan gelen kısa bir e-postadır.",
            "Metinden önce soruları oku.",
            "İsimlerin, sayıların ve yerlerin altını çiz.",
            "Bilmediğin kelimede durma, anlamı tahmin et.",
            "Her soruya cevap ver: yanlış cevap puan kaybettirmez.",
        ],
        key="Metin: « mon mari, Paul » → Soru: « Qui est Paul ? »",
        key_tr="Cevap metinde aynı kelimelerle yazmayabilir.",
    ),
)


M4_P1 = [
    """<div class="grid2" style="grid-template-columns:1fr 1.15fr">
  <div class="box"><h2><span class="n">1</span>-er fiilleri: şimdiki zaman</h2>
    <table class="conj">
      <tr><td>j'</td><td>aim<span class="no">e</span></td><td class="tr sm">severim</td></tr>
      <tr><td>tu</td><td>aim<span class="no">es</span></td><td class="tr sm">seversin</td></tr>
      <tr><td>il / elle</td><td>aim<span class="no">e</span></td><td class="tr sm">sever</td></tr>
      <tr><td>nous</td><td>aim<span class="hl">ons</span></td><td class="tr sm">severiz</td></tr>
      <tr><td>vous</td><td>aim<span class="hl">ez</span></td><td class="tr sm">seversiniz</td></tr>
      <tr><td>ils / elles</td><td>aim<span class="no">ent</span></td><td class="tr sm">severler</td></tr></table>
    <p class="sm" style="margin-top:1.4mm">-er atılır, son ek eklenir: aimer, regarder, jouer, parler, habiter…</p></div>
  <div class="box"><h2><span class="n">2</span>Dört biçim, tek ses</h2>
    <p class="sm">Kırmızı son ekler (<span class="no">-e, -es, -e, -ent</span>) <b>okunmaz</b>: j'aime, tu aimes, il aime, ils aiment aynı okunur [em]. Sadece <span class="hl">-ons</span> ve <span class="hl">-ez</span> duyulur.</p>
    <p class="sm" style="margin-top:1.2mm">Sesli harfle başlayan fiilde bağlama: nous‿aimons, ils‿aiment [z].</p>
    <p class="sm" style="margin-top:1.2mm">Sesli harften önce je → <b>j'</b>: j'aime, j'adore, j'habite.</p>
    <p class="sm" style="margin-top:1.2mm"><b>préférer</b>: je préf<span class="hl">è</span>re, tu préf<span class="hl">è</span>res, ils préf<span class="hl">è</span>rent · nous préf<span class="hl">é</span>rons, vous préf<span class="hl">é</span>rez.</p>
    <p class="sm" style="margin-top:1.2mm">İki fiil yan yana: ikincisi çekilmez. <span class="fr">J'aime cuisiner.</span> <span class="tr">Yemek yapmayı severim.</span></p>
    <p class="sm" style="margin-top:1.2mm">Düzensiz, ezberle: <b>je fais, tu fais</b> (yapmak) · <b>je lis, tu lis</b> (okumak).</p></div>
</div>""",
    """<div class="box"><h2><span class="n">3</span>Zevklerini söylemek: sevgiden nefrete</h2>
  <div class="grid2" style="grid-template-columns:1.2fr 1fr;align-items:start">
  <table class="kv">
    <tr><td><span class="ok">❤❤</span> adorer</td><td><span class="fr">J'adore la lecture.</span> <span class="tr sm">Okumaya bayılırım.</span></td></tr>
    <tr><td><span class="ok">❤</span> aimer beaucoup</td><td><span class="fr">J'aime beaucoup le vélo.</span> <span class="tr sm">Bisikleti çok severim.</span></td></tr>
    <tr><td><span class="ok">❤</span> aimer</td><td><span class="fr">J'aime le cinéma.</span> <span class="tr sm">Sinemayı severim.</span></td></tr>
    <tr><td>~ aimer un peu</td><td><span class="fr">J'aime un peu le football.</span> <span class="tr sm">Futbolu biraz severim.</span></td></tr>
    <tr><td><span class="no">✗</span> ne pas aimer</td><td><span class="fr">Je n'aime pas la natation.</span> <span class="tr sm">Yüzmeyi sevmem.</span></td></tr>
    <tr><td><span class="no">✗✗</span> détester</td><td><span class="fr">Je déteste la télévision.</span> <span class="tr sm">Televizyondan nefret ederim.</span></td></tr></table>
  <div class="sm">
    <p>Arkasından <b>isim</b> ya da <b>çekilmemiş fiil</b> gelir:</p>
    <p style="margin-top:1mm"><span class="fr">J'aime le sport.</span> <span class="tr">Sporu severim.</span></p>
    <p><span class="fr">Je préfère lire.</span> <span class="tr">Okumayı tercih ederim.</span></p>
    <p style="margin-top:1.4mm">Bu fiillerden sonra hep <b>belirli tanımlık</b>: <span class="ok">J'aime le sport</span>, <span class="mute">J'aime un sport</span>.</p></div></div></div>""",
]

M4_P2 = [
    """<div class="grid2" style="grid-template-columns:1.15fr 1fr">
  <div class="box"><h2><span class="n">4</span>Belirli ve belirsiz: le / un</h2>
    <table class="mf"><tr><th class="t"></th><th class="m">Eril</th><th class="f">Dişil</th><th class="t">Çoğul</th></tr>
      <tr><td class="tr sm">belirli<br>(genel, bilinen)</td><td><span class="hl">le</span> sport</td><td><span class="no">la</span> lecture</td><td><b>les</b> films</td></tr>
      <tr><td class="tr sm">belirsiz<br>(bir, birkaç)</td><td><span class="hl">un</span> livre</td><td><span class="no">une</span> photo</td><td><b>des</b> amis</td></tr></table>
    <p class="sm" style="margin-top:1.4mm"><span class="fr">J'aime les films.</span> <span class="tr">Filmleri severim. (genel olarak)</span><br>
    <span class="fr">Je regarde un film.</span> <span class="tr">Bir film izliyorum. (herhangi bir film)</span></p>
    <p class="sm" style="margin-top:1.2mm">Sesli harften önce le / la → <b>l'</b>: l'ami, l'école.</p></div>
  <div class="box"><h2><span class="n">5</span>Hobiler: faire du / jouer au</h2>
    <table class="kv">
      <tr><td>faire du</td><td><span class="fr">Je fais du sport, du vélo.</span><br><span class="tr sm">Spor yaparım, bisiklete binerim.</span></td></tr>
      <tr><td>faire de la</td><td><span class="fr">Je fais de la natation.</span><br><span class="tr sm">Yüzme yaparım. (dişil isim)</span></td></tr>
      <tr><td>jouer au</td><td><span class="fr">Je joue au football.</span><br><span class="tr sm">Futbol oynarım. (oyunlar, top sporları)</span></td></tr>
      <tr><td>jouer aux</td><td><span class="fr">Je joue aux jeux vidéo.</span><br><span class="tr sm">Video oyunları oynarım.</span></td></tr></table>
    <p class="sm" style="margin-top:1.2mm">de + le = <b>du</b> · à + le = <b>au</b> · à + les = <b>aux</b></p></div>
</div>""",
    """<div class="box"><h2><span class="n">6</span>Olumsuz cümle: ne... pas, ne... jamais</h2>
  <div class="grid2" style="align-items:start">
    <div class="sm"><p>Fransızcada olumsuzluk iki parçadır ve fiili sandviç gibi sarar:</p>
      <p style="margin-top:1.2mm"><span class="fr">Je <span class="no">ne</span> regarde <span class="no">pas</span> la télévision.</span><br><span class="tr">Televizyon izlemem.</span></p>
      <p style="margin-top:1.2mm"><span class="fr">Je <span class="no">n'</span>aime <span class="no">pas</span> le football.</span><br><span class="tr">Futbolu sevmem. (sesli harften önce n')</span></p></div>
    <div class="sm"><p><b>jamais</b> = hiçbir zaman, hiç:</p>
      <p style="margin-top:1.2mm"><span class="fr">Je <span class="no">ne</span> nage <span class="no">jamais</span>.</span> <span class="tr">Hiç yüzmem.</span></p>
      <p style="margin-top:1.2mm"><span class="fr">Tu regardes la télévision ? Non, jamais.</span><br><span class="tr">Televizyon izler misin? Hayır, hiç.</span></p>
      <p style="margin-top:1.4mm">Konuşmada « ne » düşebilir (<span class="mute">J'aime pas</span>), ama sınavda ikisini de yaz.</p></div></div></div>""",
    """<div class="box"><h2><span class="n">7</span>Soru sormanın üç yolu</h2>
  <table class="kv">
    <tr><td>1. Tonlama <span class="tr sm">(günlük)</span></td><td><span class="fr">Tu aimes le sport ? ↗</span> <span class="tr sm">Cümle aynı kalır, ses sonda yükselir.</span></td></tr>
    <tr><td>2. Est-ce que <span class="tr sm">(en net)</span></td><td><span class="fr"><span class="hl">Est-ce que</span> tu aimes le sport ?</span> <span class="tr sm">[eskö] · sesli harften önce est-ce qu'il…</span></td></tr>
    <tr><td>3. Devrik yapı <span class="tr sm">(resmi)</span></td><td><span class="fr">Aimes-tu le sport ?</span> <span class="tr sm">Tanıman yeterli.</span></td></tr></table>
  <p class="sm" style="margin-top:1.4mm"><span class="fr">Qu'est-ce que tu fais le week-end ?</span> <span class="tr">Hafta sonu ne yapıyorsun?</span> ·
  <span class="fr">Pourquoi ? Parce que c'est intéressant.</span> <span class="tr">Neden? Çünkü ilginç.</span></p></div>""",
]

M4_P3 = [
    """<div class="grid2">
  <div class="box"><h2><span class="n">8</span>Bağlaçlar</h2>
    <table class="kv">
      <tr><td>et <span class="tr sm">ve</span></td><td><span class="fr">J'aime le sport <span class="hl">et</span> la lecture.</span></td></tr>
      <tr><td>ou <span class="tr sm">veya, mı… mı</span></td><td><span class="fr">Le vélo <span class="hl">ou</span> la marche ?</span></td></tr>
      <tr><td>mais <span class="tr sm">ama</span></td><td><span class="fr">J'aime le thé, <span class="hl">mais</span> je n'aime pas le café.</span></td></tr>
      <tr><td>alors <span class="tr sm">o hâlde</span></td><td><span class="fr"><span class="hl">Alors</span>, tu regardes les matchs !</span></td></tr>
      <tr><td>parce que <span class="tr sm">çünkü</span></td><td><span class="fr">J'aime la mer <span class="hl">parce que</span> c'est calme.</span></td></tr></table>
    <p class="sm" style="margin-top:1.2mm">« parce que » + tam cümle · sesli harften önce <b>parce qu'</b>il…</p></div>
  <div class="box"><h2><span class="n">9</span>très, trop, beaucoup, un peu</h2>
    <p class="sm">Sıfattan önce: <b>très</b> (çok, olumlu), <b>trop</b> (fazla, sorun var)</p>
    <p><span class="fr">C'est <span class="ok">très</span> intéressant.</span> <span class="tr sm">Çok ilginç.</span></p>
    <p><span class="fr">C'est <span class="no">trop</span> difficile.</span> <span class="tr sm">Fazla zor.</span></p>
    <p class="sm" style="margin-top:1.4mm">Fiilden sonra: <b>beaucoup</b>, <b>un peu</b></p>
    <p><span class="fr">J'aime <span class="hl">beaucoup</span> le football.</span> <span class="tr sm">Futbolu çok severim.</span></p>
    <p><span class="fr">Je parle <span class="hl">un peu</span> français.</span> <span class="tr sm">Biraz Fransızca konuşurum.</span></p>
    <p class="sm" style="margin-top:1mm"><span class="mute">J'aime très le football.</span> <span class="no">Yanlış</span></p></div>
</div>""",
    """<div class="box"><h2><span class="n">10</span>Katılıyorum, katılmıyorum</h2>
  <div class="grid2" style="align-items:start">
    <div class="sm"><p><span class="fr">Je suis d'accord.</span> <span class="tr">Katılıyorum.</span></p>
      <p><span class="fr">Je ne suis pas d'accord.</span> <span class="tr">Katılmıyorum.</span></p>
      <p><span class="fr">D'accord !</span> <span class="tr">Tamam! (bir öneriyi kabul etmek)</span></p></div>
    <div class="sm"><p><span class="fr">J'aime le cinéma. <span class="ok">Moi aussi !</span></span> <span class="tr">Ben de!</span></p>
      <p><span class="fr">Je n'aime pas la télé. <span class="ok">Moi non plus.</span></span> <span class="tr">Ben de (sevmem).</span></p>
      <p style="margin-top:1mm">Olumlu cümleye <b>moi aussi</b>, olumsuz cümleye <b>moi non plus</b>.</p></div></div></div>""",
    """<div class="grid2">
  <div class="tip"><b>Öğretmenin tavsiyesi</b>« Qu'est-ce que tu fais le week-end ? » birini tanımak için en çok sorulan sorulardan biridir. Kendi cevabını şimdiden hazırla: « Le week-end, je... »</div>
  <div class="tip"><b>Öğretmenin tavsiyesi</b>Soru sormanın en kolay yolu cümlenin sonunda sesini yükseltmektir. « Est-ce que » ile başlamak daha nettir: sınavda bu iki yol yeter.</div>
</div>""",
]

M4_TELAFFUZ = """<div class="box"><h3>Telaffuz: sorunun tonlaması</h3>
  <p class="sm">Yazıda aynı cümle, sesle soru olur: <span class="fr">Tu aimes le sport.</span> ↘ / <span class="fr">Tu aimes le sport ?</span> ↗ Türkçedeki « mı » ekinin işini ses yapar.</p>
  <p class="sm" style="margin-top:1mm"><b>est-ce que</b> tek kelime gibi okunur: [eskö].</p>
  <p class="sm" style="margin-top:1mm">aim<span class="mute">e</span>, aim<span class="mute">es</span>, aim<span class="mute">ent</span> aynı okunur; aim<span class="hl">ons</span>, aim<span class="hl">ez</span> duyulur.</p></div>"""

MODULES[4] = dict(
    num=4, title="Sevdiklerim ve hobilerim", title_fr="Mes goûts",
    video="https://youtu.be/tXGcDb-_H3Y",
    goals=[
        "Sevdiğim ve sevmediğim şeyleri söylemek",
        "-er ile biten fiilleri şimdiki zamanda çekmek",
        "« ne... pas » ve « ne... jamais » ile olumsuz cümle kurmak",
        "Belirli ve belirsiz tanımlık arasında seçim yapmak: le / un",
        "« est-ce que » ile veya tonlamayla soru sormak",
        "« et, ou, mais, alors, parce que » ile cümleleri bağlamak",
        "« très, trop, beaucoup » ile derecelendirmek",
        "Hobilerimden ve sporlarımdan bahsetmek",
        "Katılıp katılmadığımı söylemek",
    ],
    grammar_pages=[M4_P1, M4_P2, M4_P3],
    phrases=[
        ("Qu'est-ce que tu fais le week-end ?", "Hafta sonu ne yapıyorsun?"),
        ("Le samedi, je joue au football avec des amis.", "Cumartesi günleri arkadaşlarla futbol oynuyorum."),
        ("Moi, je n'aime pas le football. C'est trop fatigant !", "Ben futbolu sevmem. Fazla yorucu!"),
        ("Est-ce que tu fais du sport ?", "Spor yapar mısın?"),
        ("Moi, je ne nage jamais. Je préfère le vélo.", "Ben hiç yüzmem. Bisikleti tercih ederim."),
        ("J'aime le cinéma. Moi aussi !", "Sinemayı severim. Ben de!"),
        ("Je ne suis pas d'accord.", "Katılmıyorum."),
        ("Ils sont très intéressants, parce que les histoires sont belles.", "Çok ilginçler, çünkü hikâyeleri güzel."),
    ],
    voc_must=[
        ("aimer", "eme", "sevmek"), ("adorer", "adore", "bayılmak"),
        ("détester", "deteste", "nefret etmek"), ("préférer", "prefere", "tercih etmek"),
        ("le sport", "lö spor", "spor"), ("le football", "lö futbol", "futbol"),
        ("la lecture", "la lektür", "okuma"), ("le livre", "lö livr", "kitap"),
        ("le cinéma", "lö sinema", "sinema"), ("le film", "lö film", "film"),
        ("la télévision", "la televizyoⁿ", "televizyon"), ("cuisiner", "küizine", "yemek yapmak"),
        ("le voyage", "lö vuayaj", "seyahat"), ("jouer", "jue", "oynamak"),
        ("regarder", "rögarde", "izlemek / bakmak"), ("lire", "lir", "okumak"),
        ("le week-end", "lö uikend", "hafta sonu"), ("beaucoup", "boku", "çok"),
        ("un peu", "öⁿ pö", "biraz"), ("très", "tre", "çok"),
        ("trop", "tro", "fazla / aşırı"), ("mais", "me", "ama"),
        ("parce que", "parskö", "çünkü"), ("d'accord", "dakor", "tamam / katılıyorum"),
        ("souvent", "suvaⁿ", "sık sık"), ("jamais", "jame", "asla / hiç"),
    ],
    voc_rec=[
        ("la natation", "la natasyoⁿ", "yüzme"), ("la marche", "la marş", "yürüyüş"),
        ("le vélo", "lö velo", "bisiklet"), ("le jardin", "lö jardeⁿ", "bahçe"),
        ("la promenade", "la promnad", "gezinti"), ("les jeux vidéo", "le jö video", "video oyunları"),
        ("la photo", "la foto", "fotoğraf"), ("le dessin", "lö deseⁿ", "resim çizme"),
        ("nager", "naje", "yüzmek"), ("marcher", "marşe", "yürümek"),
        ("le temps libre", "lö taⁿ libr", "boş zaman"), ("intéressant / intéressante", "eⁿteresaⁿ(t)", "ilginç"),
    ],
    telaffuz=M4_TELAFFUZ,
    tips=[
        "« trop » her zaman bir sorun olduğunu söyler: « Le film est trop long ». Bir şeyi övmek için « très » kullan: « Le film est très beau ».",
    ],
    delf=dict(
        title="Sözlü sınav, 2. bölüm",
        points=[
            "2. bölümde (yaklaşık 2 dk) soruları sen sorarsın. Görevli kartlar koyar: « Sport ? », « Week-end ? ».",
            "Görevliye [vous|hl] ile hitap et ve karttaki kelimeyi sorunda kullan.",
            "Emin olmak için « est-ce que » ile başla. Doğru ve net bir soru yeter.",
            "Takılırsan sessiz kalma: « Vous aimez... ? » gibi basit bir kalıpla dene.",
        ],
        key="Kart: « Sport ? » → Est-ce que vous aimez le sport ?",
        key_tr="Kartın kelimesi sorunun içinde olmalı",
    ),
)
