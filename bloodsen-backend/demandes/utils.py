from django.core.mail import send_mail
from django.conf import settings


def envoyer_email_sollicitation(sollicitation):
    """
    Envoie un email au donneur pour l'informer qu'il a été sollicité.
    Fonctionne pour les 3 types de demandes : STRUCTURE, PROCHE, PUBLIC.
    """
    demande = sollicitation.demande
    donneur = sollicitation.donneur
    utilisateur = donneur.utilisateur

    # Récupérer le nom et la ville de l'établissement selon le type
    if demande.structure:
        # Cas STRUCTURE : on utilise la structure propriétaire
        nom_etablissement = demande.structure.nom_structure
        ville = demande.structure.ville.nom
    else:
        # Cas PROCHE / PUBLIC : on utilise les infos saisies
        nom_etablissement = demande.lieu_prise_en_charge or "Établissement non précisé"
        ville = demande.ville.nom

    sujet = (
        f"Nouvelle demande de sang {demande.groupe_sanguin} "
        f"à {ville} - BloodSen"
    )

    message = (
        f"Bonjour {donneur.prenom},\n\n"
        f"Une demande de sang {demande.groupe_sanguin} a été publiée.\n\n"
        f"Détails :\n"
        f"  - Groupe recherché : {demande.groupe_sanguin}\n"
        f"  - Quantité : {demande.quantite} poche(s)\n"
        f"  - Niveau d'urgence : {demande.get_urgence_display()}\n"
        f"  - Établissement : {nom_etablissement}\n"
        f"  - Ville : {ville}\n"
        f"  - Message : {demande.message or '(aucun)'}\n\n"
        f"Connectez-vous sur BloodSen pour accepter ou refuser cette sollicitation.\n\n"
        f"L'équipe BloodSen"
    )

    send_mail(
        subject=sujet,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
    )

def envoyer_email_verification_demande(demande):
    """
    Envoie un email au proche pour vérifier sa demande urgente.
    Le lien contient le token de vérification/suivi.
    """

    lien = f"{settings.FRONTEND_URL}/verifier-demande?token={demande.token_suivi}"

    sujet = f"Vérifiez votre demande urgente - BloodSen"

    message = (
        f"Bonjour {demande.nom_demandeur},\n\n"
        f"Nous avons bien reçu votre demande urgente de sang "
        f"{demande.groupe_sanguin}.\n\n"
        f"Pour lancer la recherche de donneurs, cliquez sur ce lien :\n"
        f"{lien}\n\n"
        f"Ce lien vous permettra aussi de suivre l'état de votre demande.\n\n"
        f"L'équipe BloodSen"
    )

    send_mail(
        subject=sujet,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[demande.email_demandeur],
    )