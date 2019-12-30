from django import forms
from .models import ProducaoDiaria

class ProducaoDiariaForm(forms.ModelForm):

    matricula = forms.CharField(label='Matricula', max_length=100)

    #class Meta:
     #   model = ProducaoDiaria
      #  fields = ['dia', 'funcionario', 'producao', 'usuario']