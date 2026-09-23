from django.urls import path
from .views import ConfirmerParticipationView, MesParticipationsView, StructureParticipationsView

urlpatterns = [
    path(
        'sollicitations/<int:pk>/confirmer/',
        ConfirmerParticipationView.as_view(),
        name='confirmer-participation',
    ),
    path('participations/', MesParticipationsView.as_view(), name='mes-participations'),
    path('structure/participations/', StructureParticipationsView.as_view(), name='structure-participations'),
]