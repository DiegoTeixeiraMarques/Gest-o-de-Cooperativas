from django.contrib import admin
from .models import Frequencia

class FrequenciaAdmin(admin.ModelAdmin):
    fields = ['dia', 'funcionario', 'presenca', 'motivo', 'justificada']
    list_display = ['dia', 'funcionario', 'presenca', 'motivo', 'justificada']  # Campos que aparecem na listagem dos objetos no admin
    #search_fields = ['funcionario']  # Campos pesquisáveis no admin
    list_filter = ['funcionario']

admin.site.register(Frequencia, FrequenciaAdmin)