from django.core.mail import send_mail
from django.conf import settings


def envoyer_email_confirmation_participation(participation):
    """
    Envoie un email au donneur pour l'informer que sa participation
    a été confirmée par la structure.

    Format : texte brut (plus simple, plus direct).
    """
    sollicitation = participation.sollicitation
    donneur = sollicitation.donneur
    utilisateur = donneur.utilisateur
    demande = sollicitation.demande
    structure = demande.structure

    sujet = f"Votre don a été confirmé - {structure.nom_structure}"

    # Formatage de la date de confirmation
    date_confirmation = participation.date_confirmation.strftime('%d/%m/%Y à %H:%M')

    message = (
        f"Bonjour {donneur.prenom},\n\n"
        f"Nous avons le plaisir de vous informer que votre don de sang "
        f"a été confirmé par « {structure.nom_structure} » "
        f"({structure.ville}, {structure.region}).\n\n"
        f"Détails du don :\n"
        f"  - Groupe sanguin : {demande.groupe_sanguin}\n"
        f"  - Structure : {structure.nom_structure}\n"
        f"  - Date de confirmation : {date_confirmation}\n\n"
        f"Vous avez gagné 100 points d'engagement pour ce don. "
        f"Merci pour votre geste citoyen qui sauve des vies.\n\n"
        f"L'équipe BloodSen"
    )

    send_mail(
        subject=sujet,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
    )