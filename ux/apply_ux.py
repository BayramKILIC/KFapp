# -*- coding: utf-8 -*-
"""
Ajoute (ou met à jour) la couche UX commune dans les pages des modules : grammaire repliable, barre mobile,
progression mémorisée, reprise, un seul audio à la fois, objectifs raccourcis, boutons après le test.
Le code est dans ux/ux.css et ux/ux.js ; il est inséré entre des repères, donc on peut relancer sans risque.

Lancement, depuis la racine KFapp :   py ux/apply_ux.py
Pour une seule page :                 py ux/apply_ux.py chemin/vers/modul-7-xxx/index.html
À relancer après avoir reconstruit la page d'un module.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CSS = (HERE / "ux.css").read_text(encoding="utf-8")
JS = (HERE / "ux.js").read_text(encoding="utf-8")
C0, C1 = "/* UX-CSS-DEBUT */", "/* UX-CSS-FIN */"
J0, J1 = "/* UX-JS-DEBUT */", "/* UX-JS-FIN */"

import sys
PAGES = [Path(a) for a in sys.argv[1:]] or sorted((ROOT / "delf-a1").glob("modul-*/index.html"))

for page in PAGES:
    page = page.resolve()
    n = int(re.match(r"modul-(\d+)", page.parent.name).group(1))
    h = page.read_text(encoding="utf-8")
    h = re.sub(re.escape(C0) + ".*?" + re.escape(C1) + "\n?", "", h, flags=re.S)
    h = re.sub(re.escape(J0) + ".*?" + re.escape(J1) + "\n?", "", h, flags=re.S)
    i = h.index("</style>")                       # première feuille de style : celle de la page
    h = h[:i] + C0 + "\n" + CSS + "\n" + C1 + "\n" + h[i:]
    j = h.rindex("</script>")                     # dernier script : celui de la page
    h = h[:j] + J0 + "\n" + JS.replace("__N__", str(n)) + J1 + "\n" + h[j:]
    page.write_text(h, encoding="utf-8")
    print("ok", page.parent.name)
