# -*- coding: utf-8 -*-
"""
Nouveau gabarit des fiches PDF (test) : « Özet ve alıştırma fişi ».
Disposition ligne par ligne, sections numérotées, remarques du professeur en rouge, exercices à la fin.
Pas de couverture pleine page : le titre et le QR code sont en haut de la page 1.

Lancement, depuis la racine KFapp :
  py ozet/build_fis.py 1
  py ozet/build_fis.py 1 2 3 --site     (écrit directement a1/pdf/mNN-ozet.pdf, les fiches du site)
Sortie par défaut : ozet/out/mNN-fis.pdf
"""
import html
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from build_ozet import mk, data_uri, qr_uri, font_css  # noqa: E402
from fis_data import FIS  # noqa: E402

E = html.escape

CSS = """
@page{size:A4;margin:14mm 15mm 17mm;
 @bottom-left{content:"kolayfransizca.app · DELF A1 Hazırlık";font-family:'Jakarta',sans-serif;font-size:7.6pt;color:#5C5873}
 @bottom-right{content:counter(page) " / " counter(pages);font-family:'Jakarta',sans-serif;font-size:7.6pt;color:#5C5873}}
*{box-sizing:border-box;margin:0;padding:0}
:root{--brand:#5B4CC4;--brand-dark:#3F3396;--tint:#EEEBFB;--gold:#E9B53B;--gold-ink:#7A5607;--gold-tint:#FBF3DD;
 --ink:#1D1A33;--soft:#5C5873;--line:#DDD9EC;--no:#C2412D;--ok:#1E8A5A}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Jakarta',sans-serif;color:var(--ink);font-size:10.6pt;line-height:1.35}
h1,h2,.disp{font-family:'Bricolage',sans-serif}
.hl{color:var(--brand);font-weight:800}.no{color:var(--no);font-weight:800}.ok{color:var(--ok);font-weight:800}
.gold{background:var(--gold-tint);color:var(--ink);font-weight:800;padding:0 1mm;border-radius:1mm}
.mute{color:#A9A3C4;text-decoration:line-through}
span.tr{color:var(--soft);font-weight:400}

/* en-tête de la fiche */
.head{display:flex;align-items:flex-start;gap:5mm;padding-bottom:3mm;border-bottom:2px solid var(--brand);margin-bottom:4mm}
.head .num{flex:none;width:19mm;height:19mm;border-radius:4mm;background:var(--brand);color:#fff;font-family:'Bricolage',sans-serif;
 font-weight:800;font-size:30pt;display:flex;align-items:center;justify-content:center}
.head .mid{flex:1}
.head .brand{display:flex;align-items:center;gap:2mm;font-family:'Bricolage',sans-serif;font-weight:800;font-size:10pt;color:var(--brand-dark)}
.head .brand img{width:6mm;height:6mm;border-radius:1.4mm}
.head .brand span{color:var(--gold-ink)}
.head h1{font-size:24pt;font-weight:800;line-height:1.08;margin:1.2mm 0 1mm}
.head .sub{font-size:9.6pt;color:var(--soft)}
.head .sub b{color:var(--brand-dark)}
.head .qr{flex:none;text-align:center;font-size:7.4pt;color:var(--soft);line-height:1.25;width:27mm}
.head .qr img{width:24mm;height:24mm;display:block;margin:0 auto 1mm;border:1.4px solid var(--brand);border-radius:2mm;padding:1mm}

/* sections */
section{margin-bottom:4.4mm;break-inside:avoid}
section.long{break-inside:auto}
h2{font-size:13pt;font-weight:800;display:flex;align-items:center;gap:2.4mm;margin-bottom:1.6mm;break-after:avoid}
h2 .n{flex:none;display:inline-flex;align-items:center;justify-content:center;min-width:6.4mm;height:6.4mm;padding:0 1.2mm;border-radius:1.6mm;
 background:var(--brand);color:#fff;font-size:9.4pt}
h2 small{font-family:'Jakarta',sans-serif;font-weight:400;font-size:9.4pt;color:var(--soft)}
.intro{color:var(--soft);font-size:9.6pt;margin-bottom:1.2mm;break-after:avoid}
.row{display:flex;gap:4mm;align-items:baseline;padding:1.25mm 0;border-bottom:1px solid var(--line);break-inside:avoid}
.row .who{flex:none;width:23mm;font-size:8.6pt;font-weight:700;color:var(--brand-dark)}
.row .fr{flex:1.05;font-weight:700}
.row .tr{flex:1;color:var(--soft);font-size:9.8pt}
.row .k{flex:none;width:42mm;font-weight:800;color:var(--brand-dark)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:0 9mm}
.cols > div > h2{margin-top:0}
.conj .row .p{flex:none;width:21mm;color:var(--soft)}
.conj .row .v{flex:none;width:34mm;font-weight:700}
.conj .row .t{flex:1;color:var(--soft);font-size:9.6pt}
.note{color:var(--no);font-size:9.8pt;margin-top:1.8mm;padding-left:3mm;border-left:2.4px solid var(--no);break-inside:avoid}
.note b{font-weight:800}
.abc{display:grid;grid-template-columns:repeat(13,1fr);border-top:1px solid var(--line);border-left:1px solid var(--line)}
.abc div{border-right:1px solid var(--line);border-bottom:1px solid var(--line);text-align:center;padding:1.2mm 0 1mm}
.abc b{display:block;font-family:'Bricolage',sans-serif;font-size:12.5pt;line-height:1.1}
.abc span{font-size:8pt;color:var(--soft)}
.abc .hard{background:var(--gold-tint)}
.abc .hard span{color:var(--gold-ink);font-weight:700}
.voc{display:grid;grid-template-columns:1fr 1fr;gap:0 7mm}
.voc .row{padding:.75mm 0;gap:2mm;font-size:10pt}
.voc .w{flex:none;width:35mm;font-weight:700}
.voc .o{flex:none;width:21mm;font-size:8.8pt;color:var(--brand);font-style:italic}
.voc .t{flex:1;font-size:9.2pt;color:var(--soft)}
.voc .rec .w::after{content:" ◦";color:var(--gold-ink)}
.row .c{flex:1}.row .c.b{font-weight:700}
.row.th{border-bottom:1.4px solid var(--brand);padding-bottom:.8mm}
.row.th span{font-size:8.2pt;font-weight:800;text-transform:uppercase;letter-spacing:.3px;color:var(--brand-dark)}
.row .s{flex:none;width:24mm;color:var(--soft);font-size:9.6pt}
.grid{display:grid;gap:0 5mm}
.grid div{display:flex;gap:2mm;align-items:baseline;padding:1.1mm 0;border-bottom:1px solid var(--line)}
.grid b{flex:none;min-width:9mm;color:var(--brand-dark);font-weight:800}
.grid.w b{min-width:0;color:var(--ink);font-weight:700}
.grid i{font-style:normal;color:var(--soft);font-size:9.2pt}
.para{margin-top:1.6mm;font-size:10pt}
.para .tr{color:var(--soft)}
ol.pts{margin-left:5mm}
ol.pts li{padding:1.3mm 0;border-bottom:1px solid var(--line)}
.key{margin-top:2mm;font-weight:700}
.key i{display:block;font-style:normal;font-weight:400;color:var(--soft);font-size:9.6pt}

/* exercices */
.ex{margin-top:2mm;break-inside:avoid}
.ex > b{display:block;margin-bottom:.6mm}
.ex .q{display:grid;grid-template-columns:1fr 1fr;gap:0 9mm}
.ex .q.one{grid-template-columns:1fr}
.ex .q div{padding:2.2mm 0 1.2mm;border-bottom:1px solid var(--line)}
.blank{display:inline-block;border-bottom:1.2px solid var(--ink);min-width:24mm;height:4.2mm;vertical-align:baseline;margin:0 1mm}
.blank.wide{min-width:92mm}
.blank.mid{min-width:50mm}
.lines div{height:8.4mm;border-bottom:1.2px solid var(--ink)}
.answers{margin-top:3.5mm;padding-top:2mm;border-top:1px dashed var(--soft);font-size:8.2pt;color:var(--soft)}
.answers b{color:var(--ink)}
"""


def h2(n, title, small=""):
    return f'<h2><span class="n">{n}</span>{mk(title)}{f" <small>{mk(small)}</small>" if small else ""}</h2>'


def note(text):
    return f'<p class="note"><b>Öğretmenin notu:</b> {mk(text)}</p>'


def rows(items, cls=("fr", "tr")):
    return "".join('<div class="row">' + "".join(f'<span class="{c}">{mk(v)}</span>' for c, v in zip(cls, it)) + "</div>" for it in items)


def render(sec, n):
    k = sec["kind"]
    title = h2(n, sec["title"], sec.get("small", ""))
    intro = f'<p class="intro">{mk(sec["intro"])}</p>' if sec.get("intro") else ""
    nt = sec.get("note")
    tail = "".join(note(x) for x in ([nt] if isinstance(nt, str) else nt)) if nt else ""
    if k == "dialogue":
        body = rows(sec["lines"], ("who", "fr", "tr"))
        return f'<section class="long">{title}{intro}{body}{tail}</section>'
    paras = "".join(f'<p class="para">{mk(p)}</p>' for p in sec.get("paras", []))
    if k == "rows":
        return f'<section>{title}{intro}{rows(sec["rows"], sec.get("cls", ("fr", "tr")))}{paras}{tail}</section>'
    if k == "table":
        cls = sec.get("cls") or ("c b",) * len(sec["rows"][0])
        head = ('<div class="row th">' + "".join(f'<span class="{c.split()[0]}">{mk(h)}</span>' for c, h in zip(cls, sec["head"])) + "</div>") if sec.get("head") else ""
        return f'<section>{title}{intro}{head}{rows(sec["rows"], cls)}{paras}{tail}</section>'
    if k == "grid":
        cells = "".join((f"<div><b>{mk(str(x))}</b><i>{mk(y)}</i></div>" if str(x) else "<span></span>") for x, y in sec["items"])
        return (f'<section>{title}{intro}<div class="grid{" w" if sec.get("words") else ""}" '
                f'style="grid-template-columns:repeat({sec.get("cols", 4)},1fr)">{cells}</div>{paras}{tail}</section>')
    if k == "conj":
        body = rows(sec["rows"], ("p", "v", "t"))
        return f'<section class="conj">{title}{intro}{body}{paras}{tail}</section>'
    if k == "abc":
        cells = "".join(f'<div class="{"hard" if h else ""}"><b>{l}</b><span>{E(o)}</span></div>' for l, o, h in sec["letters"])
        return f'<section>{title}{intro}<div class="abc">{cells}</div>{rows(sec.get("rows", []))}{tail}</section>'
    if k == "voc":
        def col(items):
            return "".join(f'<div class="row{" rec" if r else ""}"><span class="w">{E(w)}</span><span class="o">{E(o)}</span><span class="t">{E(t)}</span></div>'
                           for w, o, t, r in items)
        half = (len(sec["words"]) + 1) // 2
        body = f'<div class="voc"><div>{col(sec["words"][:half])}</div><div>{col(sec["words"][half:])}</div></div>'
        np = ' style="break-before:page"' if sec.get("newpage") else ""
        return f'<section{np}>{title}{intro}{body}{tail}</section>'
    if k == "points":
        pts = "".join(f"<li>{mk(p)}</li>" for p in sec["points"])
        key = f'<p class="key">{mk(sec["key"])}<i>{E(sec["key_tr"])}</i></p>' if sec.get("key") else ""
        return f'<section>{title}{intro}<ol class="pts">{pts}</ol>{key}{tail}</section>'
    if k == "practice":
        out = []
        for ex in sec["exercises"]:
            if ex.get("lines"):
                q = '<div class="lines">' + "<div></div>" * ex["lines"] + "</div>"
            else:
                q = f'<div class="q{" one" if ex.get("one") else ""}">' + "".join(
                    "<div>" + mk(t).replace("___w", '<span class="blank wide"></span>').replace("___m", '<span class="blank mid"></span>').replace("___", '<span class="blank"></span>') + "</div>"
                    for t in ex["items"]) + "</div>"
            out.append(f'<div class="ex"><b>{mk(ex["title"])}</b>{q}</div>')
        ans = f'<p class="answers"><b>Cevaplar.</b> {mk(sec["answers"])}</p>'
        return f'<section class="long">{title}{intro}{"".join(out)}{ans}</section>'
    raise ValueError(k)


def pair(a, b, n):
    return f'<div class="cols"><div>{render(a, n)}</div><div>{render(b, n + 1)}</div></div>'


def build(num):
    m = FIS[num]
    qr = (f'<div class="qr"><img src="{qr_uri(m["video"])}" alt="QR">Ders videosu<br>(YouTube)</div>' if m.get("video") else "")
    head = f"""<div class="head"><div class="num">{num}</div><div class="mid">
  <div class="brand"><img src="{data_uri(HERE / 'logo.jpg', 'image/jpeg')}" alt="">Kolay <span>Fransızca</span></div>
  <h1>{E(m['title'])}</h1>
  <p class="sub"><b>Özet ve alıştırma fişi</b> · DELF A1 Hazırlık · Modül {num} · {E(m['title_fr'])}</p></div>{qr}</div>"""
    parts, n = [], 1
    for item in m["sections"]:
        if isinstance(item, tuple):
            parts.append(pair(item[0], item[1], n))
            n += 2
        else:
            parts.append(render(item, n))
            n += 1
    doc = f"""<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><title>Modül {num} · Özet ve alıştırma fişi</title>
<style>{font_css()}{CSS}</style></head><body>{head}{"".join(parts)}</body></html>"""
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    out_html = out / f"m{num:02d}-fis.html"
    out_html.write_text(doc, encoding="utf-8")
    pdf = (ROOT / "a1" / "pdf" / f"m{num:02d}-ozet.pdf") if "--site" in sys.argv else out / f"m{num:02d}-fis.pdf"
    chrome = next((c for c in ("chrome", "google-chrome", "chromium", "chromium-browser",
                                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
                   if shutil.which(c) or Path(c).exists()), None)
    if not chrome:
        sys.exit("Chrome introuvable : ouvre " + str(out_html) + " et imprime en PDF (A4).")
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", out_html.as_uri()], check=True, capture_output=True)
    print("Fiche écrite :", pdf)


if __name__ == "__main__":
    for a in [x for x in sys.argv[1:] if x.isdigit()] or ["1"]:
        build(int(a))
