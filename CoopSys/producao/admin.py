from django.contrib import admin
from .models import ProducaoDiaria

class ProducaoDiariaAdmin(admin.ModelAdmin):
    fields = ['funcionario', 'dia', 'producao', 'usuario']
    list_display = ['funcionario', 'dia', 'producao', 'usuario']  # Campos que aparecem na listagem dos objetos no admin
    #search_fields = ['funcionario', 'dia', 'producao']  # Campos pesquisáveis no admin
    list_filter = ['funcionario', 'dia', 'producao', 'usuario']

    #class Media:
     #   js = ('//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
      #        '/static/admin_extra.js',)

admin.site.register(ProducaoDiaria, ProducaoDiariaAdmin)
