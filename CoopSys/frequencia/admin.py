from django.contrib import admin
from .models import Frequencia

class FrequenciaAdmin(admin.ModelAdmin):
    fields = ['dia', 'funcionario', 'presenca', 'motivo']
    list_display = ['dia', 'funcionario', 'presenca', 'motivo']  # Campos que aparecem na listagem dos objetos no admin
    search_fields = ['dia', 'funcionario', 'presenca', 'motivo']  # Campos pesquisáveis no admin

admin.site.register(Frequencia, FrequenciaAdmin)