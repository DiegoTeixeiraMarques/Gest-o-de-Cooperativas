from django.db import models
from cooperativa.models import Cooperativa

class Funcionario(models.Model):
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE, related_name='cooperativa', verbose_name="Cooperativa", null=False, blank=False)
    matricula = models.CharField(max_length=6, verbose_name="Matrícula", unique=True, blank=False)
    codigo = models.CharField(max_length=8, verbose_name="Código", unique=True, blank=False)
    nome = models.CharField(max_length=50, verbose_name="Nome", null=False, blank=False)
    apelido = models.CharField(max_length=20, verbose_name="Apelido", blank=True, null=True)
    cpf = models.CharField(max_length=11, verbose_name="CPF", help_text="Digite somente números", null=True, blank=True)
    setor = models.CharField(max_length=30, verbose_name="Setor", null=True, blank=True)
    meta = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Meta", null=True, blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, related_name='funcionario', verbose_name="Supervisor", null=True, blank=True)

    created_at = models.DateTimeField(' Criado em ', auto_now_add=True)         # Grava data de criação
    updated_at = models.DateTimeField(' Atualizado em ', auto_now=True)          # Grava data de atualização

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
