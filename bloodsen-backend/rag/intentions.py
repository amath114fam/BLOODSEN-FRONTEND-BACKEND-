import re
from demandes.models import Demande


# =====================================================
# DÉTECTION D'INTENTION
# =====================================================
# Avant de lancer le RAG, on détecte si la question relève
# d'une intention connue (salutation, création de compte, etc.).
# Cela permet de répondre précisément sans dépendre du RAG.
# =====================================================


# ---- Salutations ----

SALUTATIONS = [
    'bonjour', 'salut', 'hello', 'bonsoir', 'coucou',
    'hey', 'hi', 'yo', 'slt', 'bjr',
]


def detecter_salutation(question):
    """
    Détecte si la question est une simple salutation.
    Renvoie True si c'est le cas.
    """
    q = question.strip().lower()

    # Retirer la ponctuation de fin
    q = re.sub(r'[!?.,;]+$', '', q)

    # Si la question contient plus de 4 mots, c'est probablement
    # une vraie question, pas juste une salutation
    if len(q.split()) > 4:
        return False

    return q in SALUTATIONS


def repondre_salutation():
    """
    Réponse fixe aux salutations.
    """
    return (
        "Bonjour ! Je suis l'assistant BloodSen. "
        "Je peux répondre à vos questions sur le don de sang "
        "et sur l'utilisation de la plateforme. "
        "Comment puis-je vous aider ?"
    )


# ---- Création de compte ----

MOTS_CREATION_COMPTE = [
    "créer un compte", "creer un compte", "créer un compte",
    "s'inscrire", "sinscrire", "inscription", "inscrire",
    "comment s'inscrire", "comment sinscrire",
    "créer mon compte", "creer mon compte",
    "comment créer", "comment creer",
]


def detecter_creation_compte(question):
    """
    Détecte si la question porte sur la création d'un compte.
    """
    q = question.lower()
    return any(mot in q for mot in MOTS_CREATION_COMPTE)


def repondre_creation_compte():
    """
    Réponse à la question 'comment créer un compte ?'.
    """
    return (
        "Pour créer un compte sur BloodSen, rendez-vous sur la page "
        "d'inscription. Vous pourrez choisir entre un compte donneur "
        "bénévole ou une structure de santé, puis renseigner vos "
        "informations. Un email de vérification vous sera envoyé pour "
        "activer votre compte.\n\n"
        "Lien vers l'inscription : http://localhost:5173/inscription"
    )


# ---- Demandes en cours ----

MOTS_DEMANDES_EN_COURS = [
    "demandes en cours", "demande en cours",
    "quelles demandes", "quelles sont les demandes",
    "liste des demandes", "voir les demandes",
    "demandes actives", "demandes ouvertes",
    "y a-t-il des demandes", "y a t il des demandes",
    "besoins en cours", "besoins actuels",
]


def detecter_demandes_en_cours(question):
    """
    Détecte si la question porte sur les demandes en cours.
    """
    q = question.lower()
    return any(mot in q for mot in MOTS_DEMANDES_EN_COURS)


def repondre_demandes_en_cours():
    """
    Répond en listant les demandes en cours :
    groupe sanguin, structure, statut.
    """
    demandes = Demande.objects.filter(
        statut=Demande.StatutDemande.EN_COURS,
    ).order_by('-date_creation')[:10]

    if not demandes:
        return "Aucune demande de sang n'est actuellement en cours sur la plateforme."

    lignes = ["Voici les demandes de sang actuellement en cours :", ""]

    for d in demandes:
        if d.structure:
            structure = d.structure.nom_structure
        else:
            structure = d.lieu_prise_en_charge or "Structure non précisée"

        lignes.append(
            f"- Groupe {d.groupe_sanguin} — {structure} — statut : {d.get_statut_display()}"
        )

    return "\n".join(lignes)


# =====================================================
# FONCTION PRINCIPALE
# =====================================================

def detecter_intention(question):
    """
    Détecte l'intention de la question.

    Renvoie un tuple (intention, reponse) :
      - intention : 'salutation' | 'creation_compte' | 'demandes_en_cours' | None
      - reponse : la réponse à renvoyer (si intention détectée) ou None
    """
    if detecter_salutation(question):
        return ('salutation', repondre_salutation())

    if detecter_creation_compte(question):
        return ('creation_compte', repondre_creation_compte())

    if detecter_demandes_en_cours(question):
        return ('demandes_en_cours', repondre_demandes_en_cours())

    return (None, None)