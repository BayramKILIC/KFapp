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
