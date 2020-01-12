from django.shortcuts import render
from funcionario.models import Funcionario
from calendario.models import Calendario
from .models import Frequencia
from datetime import date

def apontarFalta(request):

    try:
        matricula = request.POST.get('matricula')
        motivo = request.POST.get('motivo')
        data_atual = date.today()

        msg = 'Salvo com Sucesso!'

        funcionario = Funcionario.objects.get(matricula=matricula)
        data = Calendario.objects.get(data=data_atual)

        falta = Frequencia(dia=data, funcionario=funcionario, presenca=1, motivo=motivo)
        falta.save()


    except:
        print("Matrícula não localizada ou não informada!")
        msg = 'Matrícula não localizada ou não informada!'
        data_atual = date.today()

    try:
        tam = len(Frequencia.objects.all()) - 5
        frequencia = Frequencia.objects.all()[tam:]
    except:
        frequencia = Frequencia.objects.all()

    print(frequencia)

    template_name = 'ponto.html'
    context = {
        'frequencia': frequencia,
        'msg': msg,
        'data_atual': data_atual
    }

    return render(request, template_name, context)
