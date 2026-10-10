from django.urls import path
from .views import DashboardDonneurView, DashboardStructureView, StatsStructureView, StructureDonneursView, PredictionsStructureView

urlpatterns = [
    path('dashboard/donneur/', DashboardDonneurView.as_view(), name='dashboard-donneur'),
    path('dashboard/structure/', DashboardStructureView.as_view(), name='dashboard-structure'),
    path('dashboard/structure/stats/', StatsStructureView.as_view(), name='dashboard-structure-stats'),
    path('structure/donneurs/', StructureDonneursView.as_view(), name='structure-donneurs'),
    path(
        'dashboard/structure/predictions/',
        PredictionsStructureView.as_view(),
        name='dashboard-structure-predictions',
    ),
]