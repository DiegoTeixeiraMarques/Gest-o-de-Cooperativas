from django.contrib import admin
from .models import Funcionario

class FuncionarioAdmin(admin.ModelAdmin):
    fields = ['cooperativa', 'matricula', 'codigo', 'nome', 'apelido', 'cpf', 'setor', 'meta', 'supervisor', 'funcao', 'salario', 'ativo']
    list_display = ['nome', 'matricula', 'codigo', 'cooperativa', 'apelido', 'cpf', 'setor', 'meta', 'supervisor', 'funcao', 'ativo']  # Campos que aparecem na listagem dos objetos no admin
    #search_fields = ['nome', 'cooperativa', 'matricula']  # Campos pesquisáveis no admin
    list_filter = ['cooperativa__nome', 'supervisor', 'meta', 'funcao', 'ativo']
    #list_editable = ['meta', 'supervisor']
admin.site.register(Funcionario, FuncionarioAdmin)
