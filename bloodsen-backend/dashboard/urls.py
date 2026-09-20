from django.urls import path
from .views import DashboardDonneurView, DashboardStructureView

urlpatterns = [
    path('dashboard/donneur/', DashboardDonneurView.as_view(), name='dashboard-donneur'),
    path('dashboard/structure/', DashboardStructureView.as_view(), name='dashboard-structure'),
]