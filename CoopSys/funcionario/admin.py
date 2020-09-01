from django.contrib import admin
from .models import Funcionario

class FuncionarioAdmin(admin.ModelAdmin):
    fields = ['cooperativa', 'matricula', 'codigo', 'nome', 'apelido', 'cpf', 'setor', 'meta', 'supervisor', 'funcao', 'salario']
    list_display = ['nome', 'matricula', 'codigo', 'cooperativa', 'apelido', 'cpf', 'setor', 'meta', 'supervisor', 'funcao']  # Campos que aparecem na listagem dos objetos no admin
    #search_fields = ['nome', 'cooperativa', 'matricula']  # Campos pesquisáveis no admin
    list_filter = ['cooperativa__nome', 'supervisor', 'meta', 'funcao']
    list_editable = ['meta', 'supervisor']
admin.site.register(Funcionario, FuncionarioAdmin)
