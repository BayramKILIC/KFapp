#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige les audios des lettres seules de l'alphabet (module 1).

Problème : ElevenLabs lit mal une lettre seule (« E. », « G. », « Q. »...).
Solution : on lui envoie la prononciation écrite en français (« eu », « gé », « cu »...)
avec exactement les mêmes réglages que generate_audio.py (voix F1, eleven_v4,
[articulated] devant, [short pause] à la fin, ralenti à 90 %).

Les fichiers gardent le même nom et le même emplacement :
    a1/audio/m01/alphabet/a.mp3 ... z.mp3
La page du site et la vidéo les utilisent donc sans rien changer.
Les anciens fichiers sont sauvegardés une fois dans video/cache/alphabet_ancien/
(dossier ignoré par Git et par Vercel).

Utilisation (depuis C:\\Users\\bayii\\KFapp) :
    set ELEVENLABS_API_KEY=ta_cle
    python fix_alphabet.py --dry-run        # affiche ce qui sera envoyé, sans rien générer
    python fix_alphabet.py                  # régénère les 26 lettres
    python fix_alphabet.py E G Q W          # régénère seulement ces lettres

Deux méthodes :
  1. Texte phonétique (« bé », « gé »...) : pour la plupart des lettres.
  2. Méthode « contexte » pour les lettres de CONTEXTE (toutes par défaut) :
     ElevenLabs lit bien les lettres quand elles sont épelées dans une suite
     (comme « E, M, R, E »). On lui fait donc dire « A, Q, A. », on récupère
     les horodatages de chaque caractère (endpoint with-timestamps) et on ne
     garde que la lettre du milieu.
     Pour forcer cette méthode sur d'autres lettres : --contexte
        python fix_alphabet.py E --contexte

Si une lettre est encore mal lue, change son texte dans PRONONCIATION
ou ajoute-la à CONTEXTE, puis relance seulement cette lettre.
"""
import argparse
import base64
import os
import shutil
import sys
import tempfile
import subprocess
import time
from pathlib import Path

import requests

# Mêmes réglages et mêmes fonctions que le script principal
from generate_audio import (VOICES, PREFIX, SUFFIX, SPEED, SPEED_MODE, MODEL_ID, STABILITY,
                            OUTPUT_FORMAT, MAX_RETRIES, PAUSE_BETWEEN_CALLS, synthesize, slow_down)

VOIX = "F1"
DOSSIER = "a1/audio/m01/alphabet"
SAUVEGARDE = "video/cache/alphabet_ancien"

# Texte envoyé à ElevenLabs pour chaque lettre (prononciation française écrite)
PRONONCIATION = {
    "A": "a.",
    "B": "bé.",
    "C": "cé.",
    "D": "dé.",
    "E": "eu.",
    "F": "effe.",
    "G": "gé.",
    "H": "hache.",
    "I": "i.",
    "J": "ji.",
    "K": "ka.",
    "L": "elle.",
    "M": "emme.",
    "N": "enne.",
    "O": "o.",
    "P": "pé.",
    "Q": "cu.",
    "R": "erre.",
    "S": "esse.",
    "T": "té.",
    "U": "u.",
    "V": "vé.",
    "W": "double vé.",
    "X": "ixe.",
    "Y": "i grec.",
    "Z": "zède.",
}


# Méthode « contexte » pour toutes les lettres (meilleur résultat à l'écoute)
CONTEXTE = set(PRONONCIATION)
VOISINE = "A"            # lettre placée avant et après : « A, Q, A. »
VOISINE_POUR_A = "O"     # pour la lettre A elle-même : « O, A, O. »
PAUSE_FIN = 0.35         # silence ajouté après la lettre découpée (secondes)

TS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"


def synthesize_ts(text, voice_id, api_key):
    """Comme synthesize(), mais renvoie aussi l'horodatage de chaque caractère."""
    payload = {"text": text, "model_id": MODEL_ID, "voice_settings": {"stability": STABILITY}}
    last = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.post(TS_URL.format(voice_id=voice_id),
                              params={"output_format": OUTPUT_FORMAT},
                              headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                              json=payload, timeout=120)
        except requests.RequestException as e:
            last = f"réseau : {e}"
        else:
            if r.status_code == 200:
                d = r.json()
                al = d.get("alignment") or d.get("normalized_alignment")
                if not al:
                    raise RuntimeError("réponse sans horodatage (alignment)")
                return (base64.b64decode(d["audio_base64"]), al["characters"],
                        al["character_start_times_seconds"], al["character_end_times_seconds"])
            last = f"HTTP {r.status_code} : {r.text[:300]}"
            if r.status_code not in (429, 500, 502, 503, 504):
                break
        time.sleep(2 * attempt)
    raise RuntimeError(last)


def cut_window(chars, starts, ends, lettre):
    """Trouve le début et la fin de la lettre du milieu dans « A, X, A. »."""
    txt = "".join(chars)
    i = txt.find(f", {lettre},")
    if i < 0:
        raise RuntimeError(f"lettre introuvable dans l'horodatage : {txt!r}")
    k = i + 2                                   # index de la lettre
    prev = max(j for j in range(k) if chars[j].isalpha())
    nxt = min(j for j in range(k + 1, len(chars)) if chars[j].isalpha())
    debut = max(starts[k] - 0.05, ends[prev] + 0.03)
    fin = min(ends[k] + 0.15, starts[nxt] - 0.05)
    if fin - debut < 0.15:
        raise RuntimeError("découpe trop courte, horodatage incohérent")
    return debut, fin


def cut_letter(mp3_bytes, debut, fin, out):
    """Découpe, ajoute fondus + silence final, ralentit à SPEED, écrit le MP3."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(mp3_bytes)
    dur = fin - debut
    filtres = [f"afade=t=in:d=0.015", f"afade=t=out:st={dur - 0.04:.3f}:d=0.04",
               f"apad=pad_dur={PAUSE_FIN}"]
    if SPEED != 1:
        filtres.append(f"atempo={SPEED}")
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{debut:.3f}", "-t", f"{dur:.3f}",
                        "-i", tmp.name, "-filter:a", ",".join(filtres),
                        "-c:a", "libmp3lame", "-b:a", "128k", str(out)], check=True)
    finally:
        os.unlink(tmp.name)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Régénère les audios des lettres de l'alphabet.")
    ap.add_argument("lettres", nargs="*", help="lettres à refaire (défaut : toutes), ex. E G Q")
    ap.add_argument("--root", default=".", help="racine du site (défaut : dossier courant)")
    ap.add_argument("--dry-run", action="store_true", help="afficher sans générer")
    ap.add_argument("--contexte", action="store_true",
                    help="utiliser la méthode « contexte » pour toutes les lettres demandées")
    a = ap.parse_args()

    lettres = [l.upper() for l in a.lettres] or list(PRONONCIATION)
    inconnues = [l for l in lettres if l not in PRONONCIATION]
    if inconnues:
        sys.exit(f"Lettre(s) inconnue(s) : {', '.join(inconnues)}")

    root = Path(a.root).resolve()
    dossier = root / DOSSIER
    if not dossier.is_dir():
        sys.exit(f"Dossier introuvable : {dossier}\nLance le script depuis la racine du site (KFapp).")

    def texte_de(l):
        if a.contexte or l in CONTEXTE:
            v = VOISINE_POUR_A if l == "A" else VOISINE
            return f"{PREFIX}{v}, {l}, {v}.{SUFFIX}", "contexte"
        return f"{PREFIX}{PRONONCIATION[l]}{SUFFIX}", "phonétique"

    print(f"{len(lettres)} lettre(s) à régénérer, voix {VOIX}.")
    if a.dry_run:
        for l in lettres:
            t, m = texte_de(l)
            print(f"  {l}  [{m}]  ->  {t}  ->  {DOSSIER}/{l.lower()}.mp3")
        return

    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        sys.exit("Variable d'environnement ELEVENLABS_API_KEY absente.")
    if SPEED_MODE == "ffmpeg" and SPEED != 1 and not shutil.which("ffmpeg"):
        sys.exit("ffmpeg introuvable dans le PATH.")

    sauvegarde = root / SAUVEGARDE
    sauvegarde.mkdir(parents=True, exist_ok=True)

    ok, erreurs = 0, []
    for n, l in enumerate(lettres, 1):
        out = dossier / f"{l.lower()}.mp3"
        ancien = sauvegarde / out.name
        if out.exists() and not ancien.exists():
            shutil.copy2(out, ancien)  # on garde l'original une seule fois
        texte, methode = texte_de(l)
        try:
            if methode == "contexte":
                audio, chars, starts, ends = synthesize_ts(texte, VOICES[VOIX], api_key)
                debut, fin = cut_window(chars, starts, ends, l)
                cut_letter(audio, debut, fin, out)
                ok += 1
                print(f"[{n}/{len(lettres)}] OK   {l}  (contexte, {debut:.2f}s à {fin:.2f}s)  ->  {out.name}")
                time.sleep(PAUSE_BETWEEN_CALLS)
                continue
            audio = synthesize(texte, VOICES[VOIX], api_key)
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
            print(f"[{n}/{len(lettres)}] OK   {l}  ({PRONONCIATION[l]})  ->  {out.name}")
        except Exception as e:
            erreurs.append((l, str(e)))
            print(f"[{n}/{len(lettres)}] ERREUR {l} : {e}")
        time.sleep(PAUSE_BETWEEN_CALLS)

    print(f"\nTerminé : {ok} lettre(s) régénérée(s), {len(erreurs)} erreur(s).")
    print(f"Originaux sauvegardés dans : {sauvegarde}")
    if erreurs:
        print("Relance avec : python fix_alphabet.py " + " ".join(l for l, _ in erreurs))
        sys.exit(1)


if __name__ == "__main__":
    main()
