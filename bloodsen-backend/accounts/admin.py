from django.contrib import admin
from .models import Utilisateur, ProfilDonneur, ProfilStructureSante, InscriptionEnAttente


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'date_creation', 'is_active')
    list_filter = ('role',)
    search_fields = ('email',)

# admin.site.register() : version simple, sans personnalisation d'affichage
admin.site.register(ProfilDonneur)
admin.site.register(ProfilStructureSante)

# Utile en développement pour voir les inscriptions en attente de vérification
admin.site.register(InscriptionEnAttente)