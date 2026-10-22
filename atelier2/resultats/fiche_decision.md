# Fiche de décision — Atelier 2

## Tâche et jeu de test

Routage de 72 tickets annotés vers quatre équipes : facturation, technique, compte et commercial. Les catégories sont déséquilibrées.

## Métrique de décision

Macro-F1, choisie avant l'évaluation. Elle donne le même poids aux quatre catégories.

## Résultats

| Système | Accuracy | Macro-F1 | Durée (72 tickets) | F1 le plus faible |
| --- | ---: | ---: | ---: | --- |
| `openai/gpt-oss-20b` | 0.958 | 0.9574 | 209.6 s | Compte : 0.938 |
| `openai/gpt-oss-120b` | 0.944 | 0.9468 | 212.4 s | Technique : 0.919 |
| `qwen/qwen3.8-27b` | 0.958 | 0.9559 | 194.4 s | Commercial : 0.923 |
| GPT-OSS 20B + 4 exemples | 0.958 | 0.9568 | 202.6 s | Commercial : 0.929 |

## Décision

Retenir `openai/gpt-oss-20b` pour cette séance : il obtient le meilleur macro-F1 mesuré, 0.9574. Son avance sur Qwen est de 0.15 point de macro-F1, soit environ 0.11 ticket selon la règle de l'atelier, bien en dessous du seuil de cinq tickets ; les résultats ne montrent donc pas de différence de qualité mesurable. Qwen est le plus rapide (194.4 s contre 209.6 s), mais l'écart observé est modeste. Ajouter quatre exemples à la consigne n'améliore pas le macro-F1.

## Erreurs et limites

Pour GPT-OSS 20B, le F1 le plus faible concerne la catégorie compte (0.938) ; une confusion va de compte vers technique et une autre de technique vers compte. Les conclusions reposent sur 72 tickets et peuvent changer sur d'autres messages. Les résultats sont un benchmark de cours, pas une garantie de performance sur de nouveaux tickets.
