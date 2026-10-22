import argparse
import csv
import json
import time
from pathlib import Path

from classifieur import CONSIGNE, classer
from evaluation import afficher_rapport


PAUSE = 2.1
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets.csv"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "resultats"


def charger(chemin=DATA_FILE):
    with Path(chemin).open(encoding="utf-8-sig", newline="") as csv_file:
        lignes = list(csv.DictReader(csv_file))

    colonnes_requises = {"id", "texte", "categorie"}
    colonnes_trouvees = set(lignes[0]) if lignes else set()
    colonnes_manquantes = colonnes_requises - colonnes_trouvees
    if colonnes_manquantes:
        raise ValueError(f"CSV is missing required columns: {sorted(colonnes_manquantes)}")
    return lignes


def evaluer(modele, lignes, consigne=CONSIGNE, etiquette=None, nom_resultat=None):
    etiquette = etiquette or modele
    vrais = []
    predits = []
    debut = time.time()

    for numero, ligne in enumerate(lignes, start=1):
        print(f"Ticket {numero}/{len(lignes)}", flush=True)
        predits.append(classer(ligne["texte"], modele, consigne=consigne))
        vrais.append(ligne["categorie"])
        if numero < len(lignes):
            time.sleep(PAUSE)

    resume = afficher_rapport(etiquette, vrais, predits)
    resume.update(
        modele=modele,
        etiquette=etiquette,
        duree_s=round(time.time() - debut, 1),
        predits=predits,
        ids=[ligne["id"] for ligne in lignes],
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    identifiant_resultat = nom_resultat or modele
    nom_fichier = identifiant_resultat.replace("/", "_").replace(":", "_") + ".json"
    fichier_sortie = RESULTS_DIR / nom_fichier
    with fichier_sortie.open("w", encoding="utf-8") as json_file:
        json.dump(resume, json_file, ensure_ascii=False, indent=2)

    print(f"Résultats enregistrés dans : {fichier_sortie}")
    return resume


if __name__ == "__main__":
    parseur = argparse.ArgumentParser()
    parseur.add_argument("modele", help="Groq model ID to evaluate")
    arguments = parseur.parse_args()
    evaluer(arguments.modele, charger())
