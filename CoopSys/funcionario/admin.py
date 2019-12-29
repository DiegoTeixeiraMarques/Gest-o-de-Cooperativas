from django.contrib import admin
from .models import Funcionario

class FuncionarioAdmin(admin.ModelAdmin):
    fields = ['cooperativa', 'matricula', 'codigo', 'nome', 'apelido', 'cpf', 'setor', 'meta', 'supervisor']
    list_display = ['nome', 'matricula', 'codigo', 'cooperativa', 'apelido', 'cpf', 'setor', 'meta', 'supervisor']  # Campos que aparecem na listagem dos objetos no admin
    #search_fields = ['nome', 'cooperativa', 'matricula']  # Campos pesquisáveis no admin
    list_filter = ['cooperativa', 'supervisor', 'meta']
    #list_editable = ['nome', 'meta']

admin.site.register(Funcionario, FuncionarioAdmin)