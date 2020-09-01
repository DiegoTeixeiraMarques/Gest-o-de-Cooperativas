from django.contrib import admin
from .models import Remuneracao

class RemuneracaoAdmin(admin.ModelAdmin):
    fields = ['obs', 'faixaInicial', 'faixaFinal', 'percentualFiscal', 'percentualEncarregada']
    list_display = ['obs', 'faixaInicial', 'faixaFinal', 'percentualFiscal', 'percentualEncarregada']  # Campos que aparecem na listagem dos objetos no admin
    list_editable = ['faixaInicial', 'faixaFinal', 'percentualFiscal', 'percentualEncarregada']

admin.site.register(Remuneracao, RemuneracaoAdmin)