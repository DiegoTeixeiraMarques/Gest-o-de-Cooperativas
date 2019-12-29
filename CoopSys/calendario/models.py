from django.db import models

class Calendario(models.Model):
    data = models.DateField(verbose_name='Data', blank=False, null=False)
    dia = models.CharField(max_length=20, verbose_name='Dia da semana', blank=False, null=False)
    diaUtil = models.BooleanField(verbose_name='Dia útil', blank=False, null=False)
    observacao = models.CharField(max_length=255, verbose_name='Observações', blank=True, null=True)

    def __str__(self):
        return str(self.data)

    class Meta:
        verbose_name = "Calendário"
        verbose_name_plural = "Calendários"
        ordering = ['data']
