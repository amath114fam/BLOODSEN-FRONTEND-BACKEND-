from django.contrib import admin
from .models import Participation


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sollicitation', 'statut', 'date_confirmation')
    list_filter = ('statut',)