CATEGORIES = ["facturation", "technique", "compte", "commercial"]
PREDICTION_LABELS = CATEGORIES + ["invalide"]


def _verifier_longueurs(vrais, predits):
    if len(vrais) != len(predits):
        raise ValueError("vrais and predits must have the same length")


def accuracy(vrais, predits):
    _verifier_longueurs(vrais, predits)
    if not vrais:
        return 0.0
    return sum(1 for vrai, predit in zip(vrais, predits) if vrai == predit) / len(vrais)


def scores_par_classe(vrais, predits, classes=CATEGORIES):
    _verifier_longueurs(vrais, predits)
    resultat = {}
    for categorie in classes:
        vp = sum(1 for vrai, predit in zip(vrais, predits) if vrai == categorie and predit == categorie)
        fp = sum(1 for vrai, predit in zip(vrais, predits) if vrai != categorie and predit == categorie)
        fn = sum(1 for vrai, predit in zip(vrais, predits) if vrai == categorie and predit != categorie)
        precision = vp / (vp + fp) if (vp + fp) else 0.0
        recall = vp / (vp + fn) if (vp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        resultat[categorie] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": vp + fn,
        }
    return resultat


def f1_macro(scores):
    if not scores:
        return 0.0
    return sum(score["f1"] for score in scores.values()) / len(scores)


def taux_invalides(predits):
    if not predits:
        return 0.0
    return sum(1 for predit in predits if predit == "invalide") / len(predits)


def matrice_confusion(vrais, predits):
    _verifier_longueurs(vrais, predits)
    matrice = {
        vrai: {predit: 0 for predit in PREDICTION_LABELS}
        for vrai in CATEGORIES
    }
    for vrai, predit in zip(vrais, predits):
        if vrai in matrice:
            etiquette_predite = predit if predit in PREDICTION_LABELS else "invalide"
            matrice[vrai][etiquette_predite] += 1
    return matrice


def afficher_rapport(etiquette, vrais, predits):
    scores = scores_par_classe(vrais, predits)
    macro_f1 = f1_macro(scores)
    invalides = taux_invalides(predits)
    matrice = matrice_confusion(vrais, predits)
    resume = {
        "accuracy": accuracy(vrais, predits),
        "macro_f1": macro_f1,
        "invalides": invalides,
        "scores_par_classe": scores,
        "matrice_confusion": matrice,
    }

    print(f"=== {etiquette} ===")
    print(f"accuracy    : {resume['accuracy']:.3f}")
    print(f"macro-F1    : {macro_f1:.3f}")
    print(f"invalides   : {invalides:.3f}")
    print("\ncategorie      precision   recall      F1     n")
    for categorie, score in scores.items():
        print(
            f"{categorie:<13}"
            f"{score['precision']:>10.3f}"
            f"{score['recall']:>9.3f}"
            f"{score['f1']:>9.3f}"
            f"{score['support']:>6}"
        )

    print("\nConfusion matrix (lignes = vérité, colonnes = prédiction)")
    print(f"{'':<14}" + "".join(f"{label[:10]:>11}" for label in PREDICTION_LABELS))
    for vrai, comptes in matrice.items():
        print(f"{vrai:<14}" + "".join(f"{comptes[label]:>11}" for label in PREDICTION_LABELS))

    return resume
