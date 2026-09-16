from django.core.mail import send_mail
from django.conf import settings


def envoyer_email_sollicitation(sollicitation):
    """
    Envoie un email au donneur pour l'informer qu'il a été sollicité
    pour une demande de sang.

    Prend une Sollicitation en argument et utilise les infos de la
    Demande liée (structure, groupe, urgence, message) pour construire
    le contenu de l'email.
    """
    demande = sollicitation.demande
    donneur = sollicitation.donneur
    utilisateur = donneur.utilisateur  # le compte User associé au profil donneur

    # Sujet : dynamique, avec le groupe et la ville
    sujet = (
        f"Nouvelle demande de sang {demande.groupe_sanguin} "
        f"à {demande.structure.ville} - BloodSen"
    )

    # Corps du message : on assemble les infos de la demande
    message = (
        f"Bonjour {donneur.prenom},\n\n"
        f"L'établissement « {demande.structure.nom_structure} » "
        f"({demande.structure.ville}, {demande.structure.region}) "
        f"recherche du sang {demande.groupe_sanguin}.\n\n"
        f"Détails de la demande :\n"
        f"  - Groupe recherché : {demande.groupe_sanguin}\n"
        f"  - Quantité : {demande.quantite} poche(s)\n"
        f"  - Niveau d'urgence : {demande.get_urgence_display()}\n"
        f"  - Message de la structure : {demande.message or '(aucun)'}\n\n"
        f"Connectez-vous sur BloodSen pour accepter ou refuser cette sollicitation.\n\n"
        f"L'équipe BloodSen"
    )

    # Envoi réel via le backend configuré (Brevo en dev)
    send_mail(
        subject=sujet,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
    )