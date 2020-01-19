from django.shortcuts import render, HttpResponse
from .models import ProducaoDiaria
from funcionario.models import Funcionario
from calendario.models import Calendario
from django.contrib.auth.models import User
from datetime import date
import serial
import pdb
import xlwt

def index(request):

    try:
        matricula = request.POST.get('matricula')
        user = request.user.id
        peso = pegarPeso()
        data_atual = date.today()

        funcionario = Funcionario.objects.get(matricula=matricula)
        usuario = User.objects.get(id=user)
        data = Calendario.objects.get(data=data_atual)

        producaoNova = ProducaoDiaria(dia=data, funcionario=funcionario, producao=peso, usuario=usuario)
        producaoNova.save()
        msg = 'Salvo com Sucesso!'


    except:
        #print("Matrícula não localizada ou não informada!")
        msg = 'Matrícula não localizada ou não informada!'
        data_atual = date.today()

    try:
        tam = len(ProducaoDiaria.objects.all().filter(usuario=user)) - 5
        #print(tam)
        producao = ProducaoDiaria.objects.all().filter(usuario=user)[tam:]
    except:
        producao = ProducaoDiaria.objects.all().filter(usuario=user)

    template_name = 'index.html'
    context = {
        'producao': producao,
        'msg': msg,
        'data_atual': data_atual
    }

    return render(request, template_name, context)

def pegarPeso():

    try:
        __message = str(chr(5))
        _serial = serial.Serial(
            'com1',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
            writeTimeout=2
        )

        #print(_serial)

        # if True
        if _serial.isOpen():
            print("aberto")
            _serial.write(__message.encode('ascii'))
            _serial.flushInput()
            weight = _serial.read(14)
            str_weight = str(weight.decode())
            # new_weight = ["0","3",".","1","2"]
            new_weight = []
            for x in range(len(str_weight)):
                if 0 < x < 7:
                    new_weight.append(str_weight[x])

            _serial.close()

            new_weight = "".join(new_weight)
        else:
            #print("fechado")
            new_weight = 20
    except:
        #print("exceção")
        new_weight = 20
    

    return (new_weight)

def exportar_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="funcionarios.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Funcionarios')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Cooperativa', 'Matricula', 'Codigo', 'Nome', 'Apelido', 'Cpf', 'Setor', 'Meta', 'Supervisor']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()



    rows = Funcionario.objects.all().values_list('cooperativa', 'matricula', 'codigo', 'nome', 'apelido', 'cpf', 'setor', 'meta', 'supervisor')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response