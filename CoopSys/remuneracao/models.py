from django.db import models

class Remuneracao(models.Model):
    obs = models.CharField(max_length=25, verbose_name="Observação", blank=False, null=False)
    faixaInicial = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Faixa Inicial", null=False, blank=False)
    faixaFinal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Faixa Final", null=False, blank=False)
    percentualFiscal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Percentual Fiscal", null=False, blank=False)
    percentualEncarregada = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Percentual Encarregada", null=False, blank=False)

    created_at = models.DateTimeField(' Criado em ', auto_now_add=True)         # Grava data de criação
    updated_at = models.DateTimeField(' Atualizado em ', auto_now=True)          # Grava data de atualização

    def __str__(self):
        return self.obs

    class Meta:
        verbose_name = 'Remuneração'
        verbose_name_plural = 'Remunerações'
