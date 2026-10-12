from django.contrib import admin
from .models import Document, DocumentChunk


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Admin pour les documents RAG uploadés par le superuser.
    """
    list_display = ('titre', 'ajoute_par', 'date_ajout', 'actif')
    list_filter = ('actif', 'date_ajout')
    search_fields = ('titre', 'description')
    readonly_fields = ('date_ajout',)


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    """
    Admin pour les chunks (morceaux) des documents.
    Lecture seule : les chunks sont générés automatiquement.
    """
    list_display = ('document', 'ordre', 'date_creation')
    list_filter = ('document',)
    search_fields = ('contenu',)
    readonly_fields = ('document', 'contenu', 'ordre', 'embedding', 'date_creation')

    def has_add_permission(self, request):
        # On ne peut pas créer un chunk manuellement
        return False

    def has_change_permission(self, request, obj=None):
        # On ne peut pas modifier un chunk (embedding figé)
        return False