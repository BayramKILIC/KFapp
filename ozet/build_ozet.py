# -*- coding: utf-8 -*-
"""
Génère les « özet fişi » (fiches résumé PDF, 3 pages A4) des modules DELF A1 Hazırlık.
  page 1 : couverture (Fransızca DELF A1 Hazırlık, numéro et titre du module)
  page 2 : objectifs, grammaire, phrases clés
  page 3 : mots à apprendre, prononciation, conseils, DELF, QR code de la vidéo

Lancement, depuis la racine KFapp :
  py ozet/build_ozet.py 1          (module 1)
Sortie : a1/pdf/m01-ozet.pdf  (+ ozet/out/m01-ozet.html pour contrôle)
Nécessite : pip install qrcode   et Google Chrome (ou Chromium) installé.
"""
import base64
import html
import io
import shutil
import subprocess
import sys
from pathlib import Path

import qrcode

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ozet_data import MODULES  # noqa: E402

E = html.escape
SIRA = ["Birinci", "İkinci", "Üçüncü", "Dördüncü", "Beşinci", "Altıncı", "Yedinci", "Sekizinci", "Dokuzuncu", "Onuncu",
        "On Birinci", "On İkinci"]


def mk(text):
    """[mot|style] → <span class="style">mot</span> ; le reste est échappé."""
    out, i = [], 0
    while i < len(text):
        a = text.find("[", i)
        if a < 0:
            out.append(E(text[i:]))
            break
        b = text.find("]", a)
        seg = text[a + 1:b]
        out.append(E(text[i:a]))
        if "|" in seg:
            w, st = seg.rsplit("|", 1)
            out.append(f'<span class="{st}">{E(w)}</span>')
        else:
            out.append(E("[" + seg + "]"))
        i = b + 1
    return "".join(out)


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


def qr_uri(url):
    q = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color="#3F3396", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def font_css():
    css = []
    latin = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
    ext = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"
    for fam, slug, weights in (("Jakarta", "plus-jakarta-sans", (400, 600, 700, 800)), ("Bricolage", "bricolage-grotesque", (500, 700, 800))):
        for w in weights:
            for sub, rng in (("latin", latin), ("latin-ext", ext)):
                f = HERE / "fonts" / f"{slug}-{sub}-{w}-normal.woff2"
                if f.exists():
                    css.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;"
                               f"src:url('{data_uri(f, 'font/woff2')}') format('woff2');unicode-range:{rng}}}")
    return "\n".join(css)


CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
:root{--brand:#5B4CC4;--brand-dark:#3F3396;--tint:#EEEBFB;--gold:#E9B53B;--gold-ink:#7A5607;--gold-tint:#FBF3DD;
 --ink:#1D1A33;--soft:#5C5873;--line:#E4E1EE;--no:#C2412D;--no-tint:#FBE9E5;--ok:#1E8A5A;--ok-tint:#E3F4EC;--paper:#FAF9F5}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Jakarta',sans-serif;color:var(--ink);font-size:9.6pt;line-height:1.38}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:var(--paper);padding:13mm 13mm 16mm}
.page:last-child{page-break-after:auto}
h1,h2,h3,.disp{font-family:'Bricolage',sans-serif}
.foot{position:absolute;left:13mm;right:13mm;bottom:7mm;display:flex;justify-content:space-between;font-size:7.6pt;color:var(--soft);
 border-top:1px solid var(--line);padding-top:2.2mm}
.foot b{color:var(--brand-dark)}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:4.5mm}
.brand{font-family:'Bricolage',sans-serif;font-weight:800;font-size:12pt;color:var(--brand-dark)}
.brand span{color:var(--gold-ink)}
.mtag{font-size:8pt;font-weight:700;color:var(--brand-dark);background:var(--tint);border-radius:99px;padding:1.2mm 3.4mm}
h2{font-size:12.5pt;font-weight:800;color:var(--brand-dark);margin:0 0 2mm;display:flex;align-items:center;gap:2mm}
h2 .n{display:inline-flex;align-items:center;justify-content:center;width:6mm;height:6mm;border-radius:50%;background:var(--brand);color:#fff;font-size:8.5pt}
h3{font-size:10.2pt;font-weight:700;margin:0 0 1.4mm}
.box{background:#fff;border:1px solid var(--line);border-radius:3.2mm;padding:3.2mm 3.6mm;margin-bottom:3.2mm;break-inside:avoid}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:3.2mm}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}
.fr{font-weight:700}
.tr{color:var(--soft)}
.hl{color:var(--brand);font-weight:800}.no{color:var(--no);font-weight:800}.ok{color:var(--ok);font-weight:800}
.gold{color:var(--gold-ink);font-weight:800}.mute{color:#A9A3C4;text-decoration:line-through}
.sm{font-size:8.4pt}
ul.goals{list-style:none;columns:2;column-gap:5mm}
ul.goals li{break-inside:avoid;padding-left:5.4mm;position:relative;margin-bottom:1.1mm;font-size:8.6pt}
ul.goals li::before{content:"";position:absolute;left:0;top:.6mm;width:3.2mm;height:3.2mm;border:1.4px solid var(--brand);border-radius:1mm;background:#fff}
table{border-collapse:collapse;width:100%}
table.conj td{padding:.7mm 1.4mm;border-bottom:1px solid var(--line);font-size:9pt}
table.conj tr:last-child td{border-bottom:0}
table.conj td:first-child{color:var(--soft);width:20mm}
table.conj td:nth-child(2){font-weight:800;color:var(--brand)}
table.conj td:nth-child(3){color:var(--soft);font-size:8.2pt}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:2.6mm}
.vs > div{border-radius:2.4mm;padding:2.4mm 3mm}
.vs .a{background:var(--tint)}.vs .b{background:var(--gold-tint)}
.vs b.big{font-family:'Bricolage',sans-serif;font-size:13pt;display:block}
table.mf td{padding:.9mm 1.4mm;border-bottom:1px solid var(--line);font-size:9pt}
table.mf th{font-size:7.6pt;text-transform:uppercase;letter-spacing:.04em;text-align:left;padding:.8mm 1.4mm;color:#fff}
table.mf th.m{background:var(--brand)}table.mf th.f{background:var(--no)}table.mf th.t{background:var(--soft)}
.abc{display:grid;grid-template-columns:repeat(13,1fr);gap:1mm}
.abc div{background:#fff;border:1px solid var(--line);border-radius:1.6mm;text-align:center;padding:.8mm 0}
.abc b{display:block;font-family:'Bricolage',sans-serif;font-size:10.5pt;color:var(--brand-dark)}
.abc span{font-size:7.2pt;color:var(--soft)}
.abc .hard{border-color:var(--gold);background:var(--gold-tint)}
.phr{display:grid;grid-template-columns:1fr 1fr;gap:1.2mm 4mm}
.phr div{font-size:8.8pt;border-left:2.4px solid var(--brand);padding-left:2mm}
.phr div i{display:block;color:var(--soft);font-style:normal;font-size:8pt}
.voc{display:grid;grid-template-columns:1fr 1fr;column-gap:4mm}
.voc .w{display:grid;grid-template-columns:31mm 23mm 1fr;gap:1.4mm;padding:.75mm 0;border-bottom:1px dashed var(--line);font-size:8.6pt;align-items:baseline}
.voc .w b{font-weight:800}
.voc .w .ok2{color:var(--brand-dark);font-size:8pt}
.voc .w .t{color:var(--soft);font-size:8pt}
.voc.rec .w{font-size:8pt}
.lab{display:inline-block;font-size:7.4pt;font-weight:800;text-transform:uppercase;letter-spacing:.05em;border-radius:99px;padding:.8mm 2.6mm;margin-bottom:1.6mm}
.lab.must{background:var(--brand);color:#fff}.lab.rec{background:var(--gold);color:var(--ink)}
.tip{background:var(--gold-tint);border:1px solid var(--gold);border-radius:3mm;padding:2.6mm 3.2mm;font-size:8.6pt;margin-bottom:2mm;break-inside:avoid}
.tip b{color:var(--gold-ink);display:block;font-size:7.6pt;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.6mm}
.delf{background:var(--tint);border:1px solid var(--brand);border-radius:3mm;padding:3mm 3.4mm;break-inside:avoid}
.delf ul{padding-left:4mm;font-size:8.6pt}
.delf li{margin-bottom:.6mm}
.key{background:#fff;border-radius:2mm;padding:1.8mm 2.6mm;margin-top:1.8mm;font-size:9.4pt}
.qr{display:flex;gap:3.6mm;align-items:center;background:#fff;border:1px solid var(--line);border-radius:3mm;padding:3mm}
.qr img{width:27mm;height:27mm}
.qr > div > b{font-family:'Bricolage',sans-serif;font-size:11pt;color:var(--brand-dark);display:block;margin-bottom:1mm}
.qr code{font-family:'Jakarta',sans-serif;font-weight:700;color:var(--brand);font-size:8.8pt}
.nums{display:grid;grid-template-columns:repeat(7,1fr);gap:.8mm}
.nums div{background:#fff;border:1px solid var(--line);border-radius:1.4mm;text-align:center;padding:.5mm 0;line-height:1.15}
.nums b{display:block;font-family:'Bricolage',sans-serif;font-size:9.5pt;color:var(--brand-dark)}
.nums span{font-size:6.8pt;color:var(--soft)}
table.kv td{padding:.7mm 1.4mm;border-bottom:1px solid var(--line);font-size:8.8pt;vertical-align:top}
table.kv tr:last-child td{border-bottom:0}
table.kv td:first-child{font-weight:800;color:var(--brand);white-space:nowrap}
.dense .voc .w{padding:.45mm 0}.dense .box{margin-bottom:2.6mm}
.tree{display:flex;flex-direction:column;gap:2.4mm;align-items:center}
.tree .row{display:flex;gap:1.6mm;align-items:center}
.tree .p{background:#fff;border:1.4px solid var(--brand);border-radius:2mm;padding:1mm 2mm;text-align:center;line-height:1.15;min-width:19mm}
.tree .p.f{border-color:var(--no)}.tree .p.me{border-color:var(--brand-dark);background:var(--tint);border-width:2px}
.tree .p b{display:block;font-size:9pt}.tree .p span{font-size:7.2pt;color:var(--soft)}
.tree .plus{font-weight:800;color:var(--soft)}
/* couverture */
.cover{background:linear-gradient(160deg,#5B4CC4 0%,#3F3396 62%,#2A2170 100%);color:#fff;padding:0}
.cover .in{position:absolute;inset:0;padding:20mm 18mm}
.cover .cbrand{font-family:'Bricolage',sans-serif;font-weight:800;font-size:15pt;display:flex;align-items:center;gap:5mm}
.cover .logo{width:26mm;height:26mm;border-radius:6mm;border:1.2mm solid #fff;box-shadow:0 3mm 8mm rgba(10,5,40,.4)}
.cover .cbrand .bt{color:#fff}.cover .cbrand .bt span{color:var(--gold)}
.cover .kicker{margin-top:20mm;font-size:13pt;font-weight:700;letter-spacing:.02em;opacity:.92}
.cover .huge{font-family:'Bricolage',sans-serif;font-weight:800;font-size:150pt;line-height:.9;margin-top:4mm;letter-spacing:-.03em}
.cover .huge span{color:var(--gold)}
.cover .sub{font-family:'Bricolage',sans-serif;font-weight:700;font-size:22pt;margin-top:2mm}
.cover .modbox{position:absolute;left:18mm;right:18mm;bottom:58mm;background:#fff;color:var(--ink);border-radius:6mm;padding:9mm 10mm;
 display:flex;gap:8mm;align-items:center;box-shadow:0 6mm 14mm rgba(10,5,40,.35)}
.cover .num{flex:none;width:30mm;height:30mm;border-radius:50%;background:var(--gold);display:flex;align-items:center;justify-content:center;
 font-family:'Bricolage',sans-serif;font-weight:800;font-size:40pt;color:var(--ink)}
.cover .mlab{font-size:11pt;font-weight:800;color:var(--brand);text-transform:uppercase;letter-spacing:.08em}
.cover .mtitle{font-family:'Bricolage',sans-serif;font-weight:800;font-size:27pt;line-height:1.05;margin-top:1.4mm}
.cover .mfr{font-size:12pt;color:var(--soft);margin-top:1.6mm;font-weight:600}
.cover .ozet{position:absolute;left:18mm;bottom:30mm;font-size:12pt;font-weight:700;display:flex;gap:3mm;align-items:center}
.cover .ozet span{background:var(--gold);color:var(--ink);border-radius:99px;padding:1.4mm 4mm;font-weight:800}
.cover .url{position:absolute;left:18mm;right:18mm;bottom:14mm;display:flex;justify-content:space-between;font-size:10pt;opacity:.85}
.cover .ring{position:absolute;right:-40mm;top:-30mm;width:150mm;height:150mm;border-radius:50%;border:16mm solid rgba(255,255,255,.06)}
.cover .ring2{position:absolute;right:20mm;top:95mm;width:46mm;height:46mm;border-radius:50%;background:rgba(233,181,59,.18)}
"""


def page_cover(m):
    n = m["num"]
    return f"""
<section class="page cover"><div class="ring"></div><div class="ring2"></div><div class="in">
  <div class="cbrand"><img class="logo" src="{data_uri(HERE / 'logo.jpg', 'image/jpeg')}" alt="Kolay Fransızca"><span class="bt">Kolay <span>Fransızca</span></span></div>
  <div class="kicker">Fransızca · Sıfırdan A1 seviyesine</div>
  <div class="huge">A<span>1</span></div>
  <div class="sub">DELF A1 Hazırlık</div>
</div>
<div class="modbox"><div class="num">{n}</div><div>
  <div class="mlab">{SIRA[n - 1]} Modül</div>
  <div class="mtitle">{E(m['title'])}</div>
  <div class="mfr">{E(m['title_fr'])}</div></div></div>
<div class="ozet"><span>Özet fişi</span> Dilbilgisi · kelimeler · telaffuz · DELF</div>
<div class="url"><span>kolayfransizca.app</span><span>Ücretsiz kurs · 12 modül</span></div>
</section>"""


def top(m):
    return f'<div class="top"><div class="brand">Kolay <span>Fransızca</span></div><div class="mtag">Modül {m["num"]} · {E(m["title"])}</div></div>'


def foot(m, p, total):
    return f'<div class="foot"><span><b>kolayfransizca.app</b> · DELF A1 Hazırlık · Modül {m["num"]} özet fişi</span><span>{p} / {total}</span></div>'


def page_gram(m, blocks, p, total, first, last):
    goals = "".join(f"<li>{mk(g)}</li>" for g in m["goals"])
    goals_box = f'<div class="box"><h2><span class="n">✓</span>Bu modülün sonunda…</h2><ul class="goals">{goals}</ul></div>' if first else ""
    phr = "".join(f"<div>{mk(f)}<i>{E(t)}</i></div>" for f, t in m.get("phrases", []))
    phr_box = f'<div class="box"><h2><span class="n">»</span>Diyalogdan anahtar cümleler</h2><div class="phr">{phr}</div></div>' if (phr and last) else ""
    return f"""
<section class="page">{top(m)}
  {goals_box}
  {"".join(blocks)}
  {phr_box}
  {foot(m, p, total)}
</section>"""


def qr_block(m):
    if m.get("video"):
        return f"""<div class="qr"><img src="{qr_uri(m['video'])}" alt="QR">
        <div><b>Ders videosunu izle</b><span class="sm">Bu QR kod seni <b>Modül {m['num']}</b> ders videosuna (YouTube) götürür:</span><br><code>{E(m['video'].replace('https://', ''))}</code></div></div>"""
    return """<div class="qr" style="border-style:dashed"><div style="width:27mm;height:27mm;border:1.4px dashed #A9A3C4;border-radius:2mm;display:flex;align-items:center;justify-content:center;color:#A9A3C4;font-weight:800">QR</div>
        <div><b>Ders videosunu izle</b><span class="sm">QR kod, video yayınlandığında eklenecek.</span></div></div>"""


def page_voc(m, p, total):
    def rows(items):
        return "".join(f'<div class="w"><b>{E(w)}</b><span class="ok2">{E(o)}</span><span class="t">{E(t)}</span></div>' for w, o, t in items)
    must, rec = m["voc_must"], m["voc_rec"]
    tips = "".join(f"<div class='tip'><b>Öğretmenin tavsiyesi</b>{mk(t)}</div>" for t in m["tips"])
    d = m["delf"]
    delf = "".join(f"<li>{mk(x)}</li>" for x in d["points"])
    return f"""
<section class="page{' dense' if len(must) + len(rec) > 38 else ''}">{top(m)}
  <div class="box"><span class="lab must">Mutlaka öğren · {len(must)} kelime</span>
    <div class="voc">{rows(must)}</div></div>
  <div class="box"><span class="lab rec">Öğrenmen tavsiye edilir · {len(rec)} kelime</span>
    <div class="voc rec">{rows(rec)}</div></div>
  <div class="grid2">
    <div>{m['telaffuz']}{tips}</div>
    <div>
      <div class="delf"><h3>DELF köşesi · {E(d['title'])}</h3><ul>{delf}</ul><div class="key">{mk(d['key'])}<br><span class="tr sm">{E(d['key_tr'])}</span></div></div>
      <div style="height:3mm"></div>
      {qr_block(m)}
    </div>
  </div>
  <p class="sm tr" style="margin-top:1.6mm">Okunuşlar yaklaşıktır: « ⁿ » genizden söylenen sesi gösterir. Doğru telaffuz için kelimeleri sitede sesli dinle.</p>
  {foot(m, p, total)}
</section>"""


def pages_html(m):
    gp = m.get("grammar_pages") or [m["grammar"]]
    total = 2 + len(gp)
    out = [page_cover(m)]
    for i, blocks in enumerate(gp):
        out.append(page_gram(m, blocks, i + 2, total, i == 0, i == len(gp) - 1))
    out.append(page_voc(m, total, total))
    return "".join(out)


def build(num):
    m = MODULES[num]
    doc = f"""<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><title>Modül {num} özet fişi</title>
<style>{font_css()}{CSS}</style></head><body>{pages_html(m)}</body></html>"""
    out_html = HERE / "out" / f"m{num:02d}-ozet.html"
    out_html.parent.mkdir(exist_ok=True)
    out_html.write_text(doc, encoding="utf-8")
    pdf = ROOT / "a1" / "pdf" / f"m{num:02d}-ozet.pdf"
    pdf.parent.mkdir(parents=True, exist_ok=True)
    chrome = next((c for c in ("chrome", "google-chrome", "chromium", "chromium-browser",
                                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
                   if shutil.which(c) or Path(c).exists()), None)
    if not chrome:
        sys.exit("Chrome introuvable : ouvre " + str(out_html) + " et imprime en PDF (A4, sans marges).")
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", out_html.as_uri()], check=True, capture_output=True)
    print("Fiche écrite :", pdf)


if __name__ == "__main__":
    build(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
