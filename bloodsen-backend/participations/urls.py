from django.urls import path
from .views import ConfirmerParticipationView

urlpatterns = [
    path(
        'sollicitations/<int:pk>/confirmer/',
        ConfirmerParticipationView.as_view(),
        name='confirmer-participation',
    ),
]