from evaluation import (
    accuracy,
    f1_macro,
    matrice_confusion,
    scores_par_classe,
    taux_invalides,
)


vrais = ["compte", "technique", "compte", "commercial"]
predits = ["compte", "technique", "commercial", "commercial"]

print("Accuracy :", accuracy(vrais, predits))
scores = scores_par_classe(vrais, predits)
print("Scores :", scores)
print("Macro-F1 :", f1_macro(scores))
print("Taux invalides :", taux_invalides(predits))
print("Matrice :", matrice_confusion(vrais, predits))

assert accuracy(vrais, predits) == 0.75
assert matrice_confusion(vrais, predits)["technique"]["commercial"] == 0
assert taux_invalides(["invalide", "compte"]) == 0.5

predits_une_classe = ["compte"] * len(vrais)
assert len(scores_par_classe(vrais, predits_une_classe)) == 4
assert 0.0 <= f1_macro(scores_par_classe(vrais, predits_une_classe)) <= 1.0
