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
        codigo = request.POST.get('codigo')
        user = request.user.id
        data_atual = date.today()

        funcionario = Funcionario.objects.get(codigo=codigo)
        usuario = User.objects.get(id=user)
    except:
        msg = 'Código não localizado!'
        data_atual = date.today()

    try:
        peso = pegarPeso()
    except:
        msg = 'Problema ao pegar o peso da balança!'

    try:
        data = Calendario.objects.get(data=data_atual)
    except:
        msg = 'Cadastre a data de hoje no banco de dados!'
        data_atual = date.today()

    try:
        producaoNova = ProducaoDiaria(dia=data, funcionario=funcionario, producao=peso, usuario=usuario)
        producaoNova.save()
        msg = 'Salvo com Sucesso!'
    except:
        if codigo == None:
            msg = '...'
        else:
            print('Erro ao salvar registro.')
  
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
    response['Content-Disposition'] = 'attachment; filename="Funcionarios.xls"'

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

def exportar_producao2(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Producao_do_dia.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lançamentos')

    try:

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Dia', 'Funcionario', 'Producao', 'Usuario']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        data_atual = date.today()
        data = Calendario.objects.get(data=data_atual)
        rows = ProducaoDiaria.objects.all().filter(dia=data).values_list('dia', 'funcionario', 'producao', 'usuario')        
        rows2 = []

        for i in range(len(rows)):
            A = format(Calendario.objects.get(id=rows[i][0]).data, "%d/%m/%Y")
            B = Funcionario.objects.get(id=rows[i][1]).nome
            C = rows[i][2]
            D = User.objects.get(id=rows[i][3]).username
            rows2.append([A, B, C, D])

        for row in rows2:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)          
        
        wb.save(response)
        return response
    except:    
        print('Exceção!')
        wb.save(response)
        return response

def exportar_producao(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Producao_do_mes.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Fechamento_mes')

    try:

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Supervisor']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        funcionarios = Funcionario.objects.all().filter(supervisor!=None).values_list('nome', 'supervisor')        
        supervisores = []

        for i in range(len(funcionarios)):
            if funcionarios[i][1] != None:
                supervisores.append(funcionarios[i][1])


        for row in funcionarios:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)          
        
        wb.save(response)
        return response
    except:    
        print('Exceção!')
        wb.save(response)
        return response
        