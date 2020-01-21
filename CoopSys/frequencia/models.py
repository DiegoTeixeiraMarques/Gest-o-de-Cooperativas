from django.db import models
from funcionario.models import Funcionario
from calendario.models import Calendario

class Frequencia(models.Model):
    dia = models.ForeignKey(Calendario, related_name="Calendario", verbose_name='Dia', on_delete=models.CASCADE, blank=False, null=False)
    funcionario = models.ForeignKey(Funcionario, related_name='Funcionario', verbose_name='Funcionario', on_delete=models.CASCADE, blank=False, null=False)
    presenca = models.BooleanField(blank=False, default=True)
    motivo = models.CharField(max_length=255, blank=True, null=True, verbose_name='Motivo')
    justificada = models.BooleanField(blank=False, default=False)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Criado em', auto_now=True)

    def __str__(self):
        return str(self.funcionario)

    class Meta:
        verbose_name = "Batida de ponto"
        verbose_name_plural = "Batida de pontos"
        ordering = ['dia']