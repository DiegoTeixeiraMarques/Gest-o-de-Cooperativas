from django.contrib import admin
from .models import ProducaoDiaria

class ProducaoDiariaAdmin(admin.ModelAdmin):
    fields = ['funcionario', 'dia', 'producao', 'usuario']
    list_display = ['funcionario', 'matricula', 'dia', 'producao', 'usuario']  # Campos que aparecem na listagem dos objetos no admin
    #search_fields = ['search_funcionario'] # Campos pesquisáveis no admin
    list_filter = ['funcionario', 'dia', 'dia__data', 'producao', 'usuario']

    #class Media:
     #   js = ('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
      #        '/static/admin_extra.js',)

    def matricula(self, obj):
        return obj.funcionario.matricula

admin.site.register(ProducaoDiaria, ProducaoDiariaAdmin)
