from django.test import TestCase
from .models import Calendario, Frequencia, Funcionario

def validacaoApontamentoFalta(obj):

    faltasFuncionario = Frequencia.objects.all().filter(funcionario=obj.funcionario)

    print('Faltas Funcionario: ', faltasFuncionario.dia)
    print('Obj dia: ', obj.dia)

    #print('faltas funcionario: ',faltasFuncionario)
    #print('Obj.data: ', obj.dia)
    #print('Funcionario.data: ', faltasFuncionario.dia)

    if faltasFuncionario == []:
        return True
    else:
        for i in faltasFuncionario:
            if obj.dia ==  faltasFuncionario.dia:
                return False
    return True