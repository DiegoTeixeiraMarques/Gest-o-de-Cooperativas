from django.contrib import admin
from .models import Fechamento

class FechamentoAdmin(admin.ModelAdmin):
    fields = ['matricula', 'nome', 'funcao', 'meta', 'salario', 'producaoTotal', 'vrPagoKG', 'premio', 'referencia']
    list_display = ['matricula', 'nome', 'funcao', 'meta', 'salario', 'producaoTotal', 'vrPagoKG', 'premio', 'referencia']  # Campos que aparecem na listagem dos objetos no admin
    #search_fields = ['nome', 'cooperativa', 'matricula']  # Campos pesquisáveis no admin
    list_filter = ['matricula', 'nome', 'funcao', 'referencia']
    #list_editable = ['meta', 'supervisor']
admin.site.register(Fechamento, FechamentoAdmin)