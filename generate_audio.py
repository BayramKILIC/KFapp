#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les audios de la formation DELF A1 Hazırlık avec ElevenLabs
et les enregistre au bon endroit, avec le bon nom.

Utilisation (depuis la racine du dépôt du site) :
    set ELEVENLABS_API_KEY=ta_cle          (Windows cmd)
    export ELEVENLABS_API_KEY=ta_cle       (Git Bash)

    python generate_audio.py audio_m01.xlsx --dry-run     # affiche ce qui sera fait, sans rien générer
    python generate_audio.py audio_m01.xlsx --only M1-D   # seulement le dialogue (test)
    python generate_audio.py audio_m01.xlsx               # tout le manifeste
    python generate_audio.py audio_m01.xlsx --force       # régénère même les fichiers existants

Les fichiers déjà présents sont ignorés : on peut relancer la commande après une erreur.
Dépendances : pip install requests openpyxl   + ffmpeg dans le PATH (pour le ralenti).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests
from openpyxl import load_workbook

# ----------------------------------------------------------------------------
# RÉGLAGES
# ----------------------------------------------------------------------------
VOICES = {
    "F1": "QbsdzCokdlo98elkq4Pc",  # Koraly, E-learning Instructor (voix féminine principale)
    "M1": "69ujSsYIBOGW4duCBBSW",  # Bastien, Calm & Clear French Teacher (voix masculine)
    "F2": "ZtJvTSnGgAdhWKQBViA1",  # Alice (madame Martin, 2e personnage féminin du dialogue)
}
MODEL_ID = "eleven_v4"
STABILITY = 0.50
PREFIX = "[articulated] "       # ajouté devant chaque texte
SUFFIX = " [short pause]"       # ajouté à la fin de chaque texte
SPEED = 0.90                    # 90 % de la vitesse normale
SPEED_MODE = "ffmpeg"           # "ffmpeg" : ralenti après génération (fonctionne avec tous les modèles)
                                # "api"    : ralenti demandé à ElevenLabs (voice_settings.speed)
OUTPUT_FORMAT = "mp3_44100_128"
PAUSE_BETWEEN_CALLS = 0.4       # secondes, pour ménager l'API
MAX_RETRIES = 3
API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
# ----------------------------------------------------------------------------


def read_manifest(path):
    ws = load_workbook(path, read_only=True)["Audio"]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h).strip() for h in rows[0]]
    need = ["ID", "Voix", "Texte", "Chemin"]
    for n in need:
        if n not in head:
            sys.exit(f"Colonne manquante dans le manifeste : {n}")
    idx = {n: head.index(n) for n in need}
    items = []
    for r in rows[1:]:
        if not r or not r[idx["ID"]]:
            continue
        items.append({k.lower(): str(r[i]).strip() for k, i in idx.items()})
    return items


def synthesize(text, voice_id, api_key):
    settings = {"stability": STABILITY}
    if SPEED_MODE == "api":
        settings["speed"] = SPEED
    payload = {"text": text, "model_id": MODEL_ID, "voice_settings": settings}
    url = API_URL.format(voice_id=voice_id)
    last = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.post(
                url,
                params={"output_format": OUTPUT_FORMAT},
                headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                json=payload,
                timeout=120,
            )
        except requests.RequestException as e:
            last = f"réseau : {e}"
        else:
            if r.status_code == 200 and r.content:
                return r.content
            last = f"HTTP {r.status_code} : {r.text[:300]}"
            if r.status_code not in (429, 500, 502, 503, 504):
                break  # erreur définitive (clé, voix, modèle, paramètres) : inutile de réessayer
        time.sleep(2 * attempt)
    raise RuntimeError(last)


def slow_down(src, dst):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
           "-filter:a", f"atempo={SPEED}", "-c:a", "libmp3lame", "-b:a", "128k", str(dst)]
    subprocess.run(cmd, check=True)


def main():
    try:  # console Windows : éviter les erreurs d'affichage des accents
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Génère les audios d'un manifeste Excel.")
    ap.add_argument("manifest", help="fichier Excel du manifeste, feuille « Audio »")
    ap.add_argument("--root", default=".", help="racine du dépôt du site (défaut : dossier courant)")
    ap.add_argument("--only", default="", help="ne traiter que les ID qui commencent par ce texte, ex. M1-D")
    ap.add_argument("--force", action="store_true", help="régénérer même si le fichier existe")
    ap.add_argument("--dry-run", action="store_true", help="afficher sans générer")
    a = ap.parse_args()

    items = read_manifest(a.manifest)
    if a.only:
        items = [i for i in items if i["id"].startswith(a.only)]
    if not items:
        sys.exit("Aucune ligne à traiter.")

    unknown = sorted({i["voix"] for i in items} - set(VOICES))
    if unknown:
        sys.exit(f"Voix inconnue(s) dans le manifeste : {', '.join(unknown)}. À ajouter dans VOICES.")

    root = Path(a.root).resolve()
    todo = []
    for it in items:
        out = root / it["chemin"].lstrip("/")
        if out.exists() and not a.force:
            continue
        todo.append((it, out))

    print(f"{len(items)} lignes, {len(items) - len(todo)} déjà présentes, {len(todo)} à générer.")
    print(f"Dossier de sortie : {root}")
    if a.dry_run:
        for it, out in todo:
            print(f"  {it['id']:<16} {it['voix']:<3} {PREFIX}{it['texte']}{SUFFIX}  ->  {out.relative_to(root)}")
        return

    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        sys.exit("Variable d'environnement ELEVENLABS_API_KEY absente.")
    if SPEED_MODE == "ffmpeg" and SPEED != 1 and not shutil.which("ffmpeg"):
        sys.exit("ffmpeg introuvable dans le PATH. Installe-le ou passe SPEED_MODE à \"api\".")

    ok, errors = 0, []
    for n, (it, out) in enumerate(todo, 1):
        text = f"{PREFIX}{it['texte']}{SUFFIX}"
        try:
            audio = synthesize(text, VOICES[it["voix"]], api_key)
            out.parent.mkdir(parents=True, exist_ok=True)
            if SPEED_MODE == "ffmpeg" and SPEED != 1:
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    tmp.write(audio)
                try:
                    slow_down(tmp.name, out)
                finally:
                    os.unlink(tmp.name)
            else:
                out.write_bytes(audio)
            ok += 1
            print(f"[{n}/{len(todo)}] OK   {it['id']:<16} {out.relative_to(root)}")
        except Exception as e:  # on continue avec les lignes suivantes
            errors.append((it["id"], str(e)))
            print(f"[{n}/{len(todo)}] ERREUR {it['id']} : {e}")
        time.sleep(PAUSE_BETWEEN_CALLS)

    print(f"\nTerminé : {ok} fichiers générés, {len(errors)} erreurs.")
    if errors:
        print("Lignes en erreur (relance la même commande pour les reprendre) :")
        for i, e in errors:
            print(f"  {i} : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
