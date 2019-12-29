from django.contrib import admin
from .models import Cooperativa


admin.site.site_header = 'Cooperativa'
admin.site.index_title = 'Cooperativa'
admin.site.site_title = 'Cooperativa'

class CooperativaAdmin(admin.ModelAdmin):
    fields = ['codigo', 'nome', 'cnpj']
    list_display = ['codigo', 'nome', 'cnpj']  # Campos que aparecem na listagem dos objetos no admin
    search_fields = ['codigo', 'nome', 'cnpj']  # Campos pesquisáveis no admin
    #list_filter = ['codigo', 'nome', 'cnpj']
    #list_editable = ['nome']

admin.site.register(Cooperativa, CooperativaAdmin)