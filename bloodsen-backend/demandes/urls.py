from django.urls import path

from .views import (
    CreerDemandeView,
    ListeDemandesView,
    AccepterSollicitationView,
    RefuserSollicitationView,
    MesSollicitationsView,
)

urlpatterns = [
    # Demandes
    path('creer-demandes/', CreerDemandeView.as_view(), name='creer-demande'),
    path('demandes/', ListeDemandesView.as_view(), name='liste-demandes'),

    # Sollicitations (actions)
    path(
        'sollicitations/<int:pk>/accepter/',
        AccepterSollicitationView.as_view(),
        name='accepter-sollicitation',
    ),
    path(
        'sollicitations/<int:pk>/refuser/',
        RefuserSollicitationView.as_view(),
        name='refuser-sollicitation',
    ),
    path('sollicitations/', MesSollicitationsView.as_view(), name='mes-sollicitations'),
]