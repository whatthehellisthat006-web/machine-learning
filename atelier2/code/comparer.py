import json
from pathlib import Path


RESULTS_DIR = Path(__file__).resolve().parent.parent / "resultats"


def charger_resultats():
    resultats = []
    for fichier in sorted(RESULTS_DIR.glob("*.json")):
        with fichier.open(encoding="utf-8") as json_file:
            resultat = json.load(json_file)
        if {"ids", "predits", "macro_f1", "accuracy"} <= resultat.keys():
            resultats.append(resultat)
    return resultats


def afficher_comparaison(resultats):
    if not resultats:
        print("No comparable result files found.")
        return

    classes = sorted(resultats, key=lambda resultat: resultat["macro_f1"], reverse=True)
    print("Système                        Accuracy   Macro-F1   Invalides   Durée (s)")
    for resultat in classes:
        nom = resultat.get("etiquette", resultat["modele"])
        print(
            f"{nom:<30}"
            f"{resultat['accuracy']:>9.3f}"
            f"{resultat['macro_f1']:>11.3f}"
            f"{resultat.get('invalides', 0.0):>11.3f}"
            f"{resultat.get('duree_s', 0):>12.1f}"
        )

    if len(classes) > 1:
        ecart_macro_f1 = classes[0]["macro_f1"] - classes[1]["macro_f1"]
        ecart_tickets = ecart_macro_f1 * len(classes[0]["ids"])
        print(
            f"\nTop-two macro-F1 gap: {ecart_macro_f1:.3f} "
            f"(about {ecart_tickets:.2f} tickets by the TP's rule; "
            f"five tickets is the threshold)."
        )

    predictions_par_id = {}
    for resultat in resultats:
        nom = resultat.get("etiquette", resultat["modele"])
        for ticket_id, prediction in zip(resultat["ids"], resultat["predits"]):
            predictions_par_id.setdefault(ticket_id, {})[nom] = prediction

    divergences = {
        ticket_id: predictions
        for ticket_id, predictions in predictions_par_id.items()
        if len(set(predictions.values())) > 1
    }
    print(f"\nTickets with differing predictions: {len(divergences)}")
    for ticket_id, predictions in sorted(divergences.items()):
        detail = ", ".join(f"{modele}: {prediction}" for modele, prediction in predictions.items())
        print(f"{ticket_id}: {detail}")


if __name__ == "__main__":
    afficher_comparaison(charger_resultats())
