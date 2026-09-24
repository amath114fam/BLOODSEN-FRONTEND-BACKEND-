from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    InscrireDonneurView,
    InscrireStructureView,
    VerifierEmailView,
    EmailTokenObtainPairView,
    MoiView,
    ChangerMotDePasseView
)

urlpatterns = [
    # --- Inscriptions (accessibles sans être connecté) ---
    path(
        'inscription/donneur/',
        InscrireDonneurView.as_view(),
        name='inscription-donneur',
    ),
    path(
        'inscription/structure/',
        InscrireStructureView.as_view(),
        name='inscription-structure',
    ),

    # --- Vérification de l'email (création réelle du compte) ---
    path(
        'verifier-email/',
        VerifierEmailView.as_view(),
        name='verifier-email',
    ),

    # --- Connexion / rafraîchissement de token ---
    path(
        'connexion/',
        EmailTokenObtainPairView.as_view(),
        name='connexion',
    ),
    # TokenRefreshView : vue fournie par SimpleJWT. Elle prend un refresh_token
    # en entrée et renvoie un nouveau access_token (utilisé quand l'access
    # a expiré mais que le refresh est encore valide).
    path(
        'connexion/rafraichir/',
        TokenRefreshView.as_view(),
        name='rafraichir-token',
    ),

    # --- Infos de l'utilisateur connecté ---
   path('moi/', MoiView.as_view(), name='moi'),
   path('changer-mot-de-passe/', ChangerMotDePasseView.as_view(), name='changer-mot-de-passe'),
]