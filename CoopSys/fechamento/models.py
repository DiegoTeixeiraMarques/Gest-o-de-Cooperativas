from django.db import models

from django.db import models

class Fechamento(models.Model):
    matricula = models.CharField(max_length=6, verbose_name="Matrícula", null=True, blank=True)
    nome = models.CharField(max_length=50, verbose_name="Nome", null=True, blank=True)
    funcao = models.CharField(max_length=20, verbose_name="Função", null=True, blank=True)
    meta = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Meta", null=True, blank=True)
    salario = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Salário", null=True, blank=True)
    producaoTotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Produção Total", null=True, blank=True)
    vrPagoKG = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Vr KG", null=True, blank=True)
    premio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prêmio", null=True, blank=True)
    referencia = models.DateField(verbose_name="Referência", null=True, blank=True)

    created_at = models.DateTimeField(' Criado em ', auto_now_add=True)         # Grava data de criação
    updated_at = models.DateTimeField(' Atualizado em ', auto_now=True)          # Grava data de atualização

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Fechamento'
        verbose_name_plural = 'Fechamentos'
