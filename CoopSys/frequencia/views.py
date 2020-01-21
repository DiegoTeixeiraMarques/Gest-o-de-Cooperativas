from django.shortcuts import render
from .models import Funcionario
from calendario.models import Calendario
from .models import Frequencia
from datetime import date

def apontarFalta(request):

    try:
        matricula = request.POST.get('matricula')
        motivo = request.POST.get('motivo')
        data_atual = date.today()

        funcionario = Funcionario.objects.get(matricula=matricula)
        data = Calendario.objects.get(data=data_atual)
        falta = Frequencia(dia=data, funcionario=funcionario, presenca=1, motivo=motivo)

        if(validacaoApontamentoFalta(falta)):
            falta.save()
            msg = 'Salvo com Sucesso!'
        else:
            msg = 'Falta já informada para este funcionário!'

    except:
        #print("Matrícula não localizada ou não informada!")
        msg = 'Matrícula não localizada ou não informada!'
        data_atual = date.today()

    try:
        tam = len(Frequencia.objects.all()) - 5
        frequencia = Frequencia.objects.all()[tam:]
    except:
        frequencia = Frequencia.objects.all()
        #msg = 'Matrícula não localizada ou não informada!'

    #print(frequencia)

    template_name = 'ponto.html'
    context = {
        'frequencia': frequencia,
        'msg': msg,
        'data_atual': data_atual
    }

    return render(request, template_name, context)

def validacaoApontamentoFalta(obj):

    """ Verifica se o funcionário já tem falta apontada no mesmo dia """

    faltasFuncionario = Frequencia.objects.all().filter(funcionario=obj.funcionario.id)

    if faltasFuncionario == []:
        return True
    else:
        indice = 0
        for i in faltasFuncionario:
            if obj.dia == faltasFuncionario[indice].dia:
                return False
            indice = indice + 1
    return True