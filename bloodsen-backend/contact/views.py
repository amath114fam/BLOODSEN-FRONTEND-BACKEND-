from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from .serializers import MessageContactSerializer
from .utils import envoyer_email_contact


# =====================================================
# VUE : formulaire de contact
# =====================================================

@extend_schema(
    request=MessageContactSerializer,
    responses=None,
    description="Reçoit un message depuis le formulaire de contact public.",
)
class ContactView(APIView):
    """
    POST /api/contact/

    Reçoit un message depuis le formulaire de contact de la page d'accueil.
    Accessible à tous (pas besoin d'être connecté).

    Effets :
      - Enregistre le message en base (table MessageContact)
      - Envoie un email à l'administrateur
      - Envoie un accusé de réception à l'utilisateur
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Valider les données
        serializer = MessageContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Enregistrer en base
        message_contact = serializer.save()

        # 3. Envoyer les emails (hors du bloc "critical")
        #    Si l'email échoue, le message est quand même enregistré.
        try:
            envoyer_email_contact(message_contact)
        except Exception as e:
            print(f"Erreur lors de l'envoi des emails de contact : {e}")

        # 4. Réponse
        return Response(
            {
                "message": "Votre message a bien été envoyé. "
                           "Vous recevrez une réponse dans les plus brefs délais."
            },
            status=status.HTTP_201_CREATED,
        )