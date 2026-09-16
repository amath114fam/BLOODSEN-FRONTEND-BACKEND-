from django.contrib import admin
from .models import Demande, Sollicitation


@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'groupe_sanguin', 'quantite', 'urgence', 'statut', 'structure', 'date_creation')
    list_filter = ('statut', 'urgence', 'groupe_sanguin')
    search_fields = ('structure__nom_structure', 'message')


@admin.register(Sollicitation)
class SollicitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'demande', 'donneur', 'statut', 'date_creation', 'date_reponse')
    list_filter = ('statut',)
    search_fields = ('donneur__nom', 'donneur__prenom')