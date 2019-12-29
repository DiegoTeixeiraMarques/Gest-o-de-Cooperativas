from django.db import models
from funcionario.models import Funcionario
from calendario.models import Calendario
from django.contrib.auth.models import User

class ProducaoDiaria(models.Model):
    dia = models.ForeignKey(Calendario, verbose_name='Dia', on_delete=models.CASCADE, blank=False, null=False)
    funcionario = models.ForeignKey(Funcionario, verbose_name='Funcionário', on_delete=models.CASCADE, blank=False, null=False)
    producao = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Produção do dia", blank=False,
                                   null=False)
    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, blank=False,
                                    null=False)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Criado em', auto_now=True)

    def __str__(self):
        return str(self.funcionario)

    class Meta:
        verbose_name = 'Produção'
        verbose_name_plural = 'Produções'
