import logging
import re
from django.conf import settings
from groq import Groq, APIError

logger = logging.getLogger(__name__)


PROMPT_SYSTEME = (
    "Tu es un analyste de la coordination du don de sang pour la "
    "plateforme BloodSen au Sénégal.\n\n"
    "RÈGLES :\n"
    "1. Appuie-toi uniquement sur les statistiques fournies. "
    "N'invente aucun chiffre ni aucune région.\n"
    "2. Si les données sont insuffisantes pour conclure, dis-le clairement.\n"
    "3. Donne 3 à 5 recommandations concrètes et actionnables, en citant "
    "les régions et les groupes sanguins concernés.\n"
    "4. Ne donne aucun conseil médical. Ne recommande jamais de solliciter "
    "les donneurs plus souvent que les délais médicaux entre deux dons.\n"
    "5. Termine par une courte synthèse factuelle, sans minimiser les alertes.\n"
    "6. Réponds en français, sans introduction.\n"
    "7. FORMAT : écris uniquement en texte brut. N'utilise jamais "
    "d'astérisques, de dièses, de tirets en début de ligne, de guillemets "
    "ni aucune mise en forme Markdown. Numérote les recommandations "
    "avec 1., 2., 3., chacune sur sa propre ligne, et écris les groupes "
    "sanguins en toutes lettres (par exemple O+, A-)."
)


# ==========================================
# MISE EN FORME DU CONTEXTE
# ==========================================

def _section(titre, lignes):
    """Un bloc de texte : un titre, puis une ligne par élément."""
    if not lignes:
        lignes = ["(aucune donnée)"]
    return "\n".join([f"{titre} :"] + lignes)

def _formater_contexte(stats):
    """Transforme le dict des statistiques en texte lisible pour le LLM."""
    globales = stats.get("stats_globales", {})
    taux = globales.get("taux_satisfaction")

    chiffres = [
        f"Total demandes : {globales.get('total_demandes', 0)}",
        f"Total dons confirmés : {globales.get('total_dons', 0)}",
        f"Taux de satisfaction : {f'{taux}%' if taux is not None else 'non disponible'}",
    ]

    regions = [
        f"{r['region']} : {r['demandes']} demandes, "
        f"{r['donneurs_disponibles']} donneurs disponibles"
        for r in stats.get("par_region", [])
    ]

    groupes = [
        f"{g['groupe'].replace('_', ' ')} : {g['demandes']} demandes, "
        f"{g['donneurs']} donneurs disponibles"
        f"{' (ALERTE : déficit)' if g['alerte'] else ''}"
        for g in stats.get("par_groupe", [])
    ]

    zones = [
        f"{z['region']} : {z['raison']}"
        for z in stats.get("zones_critiques", [])
    ]

    return "\n\n".join([
        _section("Chiffres globaux", chiffres),
        _section("Par région", regions),
        _section("Par groupe sanguin", groupes),
        _section("Zones critiques", zones),
    ])

def _nettoyer_texte(texte):
    """
    Retire le formatage que le modèle ajoute parfois malgré les consignes :
    astérisques, dièses, guillemets et tirets de liste en début de ligne.
    """
    texte = re.sub(r'[*#"“”]', "", texte)
    texte = re.sub(r"^[ \t]*[-–—•][ \t]+", "", texte, flags=re.MULTILINE)
    return texte.strip()
# ==========================================
# GÉNÉRATION DES RECOMMANDATIONS
# ==========================================

def generer_recommandations_predictions(stats):
    """
    Renvoie un texte de 3 à 5 recommandations généré par Groq,
    ou None si le service est indisponible.
    """
    if not settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY manquante : recommandations IA désactivées.")
        return None

    contexte = _formater_contexte(stats)


    try:
        client = Groq(api_key=settings.GROQ_API_KEY, timeout=15.0, max_retries=1)
        reponse = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": PROMPT_SYSTEME},
                {
                    "role": "user",
                    "content": f"STATISTIQUES ACTUELLES :\n\n{contexte}\n\n"
                               "Génère tes recommandations maintenant.",
                },
            ],
            temperature=0.4,
            max_tokens=600,
        )
        texte = _nettoyer_texte(reponse.choices[0].message.content or "")
    except APIError:
        logger.exception("Appel Groq échoué")
        return None

    return texte or None