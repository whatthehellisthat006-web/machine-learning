from classifieur import classer
from groq import APIStatusError


MODELE = "openai/gpt-oss-20b"
TICKETS_TEST = [
    "Ma facture est trop élevée",
    "Je ne peux plus me connecter à mon compte",
    "L'application ne fonctionne plus",
    "Je souhaite changer mon abonnement",
    "bonjour !",
]


for texte in TICKETS_TEST:
    try:
        resultat = classer(texte, MODELE)
    except APIStatusError as error:
        print(f"Groq API error ({error.status_code}): {error.body}")
        raise SystemExit(1) from error
    print(f"Ticket : {texte}")
    print(f"Catégorie : {resultat}\n")
