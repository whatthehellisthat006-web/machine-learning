from classifieur import CONSIGNE_EXEMPLES
from evaluer import charger, evaluer


MODELE = "openai/gpt-oss-20b"


if __name__ == "__main__":
    evaluer(
        MODELE,
        charger(),
        consigne=CONSIGNE_EXEMPLES,
        etiquette="gpt-oss-20b + 4 exemples",
        nom_resultat="gpt-oss-20b_4_exemples",
    )
