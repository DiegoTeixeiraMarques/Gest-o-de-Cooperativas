from django.contrib import admin
from .models import Calendario

class CalendarioAdmin(admin.ModelAdmin):
    fields = ['data', 'dia', 'diaUtil', 'observacao']
    list_display = ['data', 'dia', 'diaUtil', 'observacao']  # Campos que aparecem na listagem dos objetos no admin
    #search_fields = ['data']  # Campos pesquisáveis no admin
    list_editable = ['dia', 'diaUtil', 'observacao']
    list_filter = ['data', 'dia', 'observacao']

admin.site.register(Calendario, CalendarioAdmin)