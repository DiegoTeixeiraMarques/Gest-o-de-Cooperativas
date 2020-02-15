from django.shortcuts import render, HttpResponse
from .models import ProducaoDiaria
from funcionario.models import Funcionario
from calendario.models import Calendario
from django.contrib.auth.models import User
from cooperativa.models import Cooperativa
from frequencia.models import Frequencia
from datetime import date, datetime
import serial
import pdb
import xlwt
import locale

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

def relatorio(request):

    template_name = 'relatorios.html'
    data_atual = date.today()
    context = {
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
    response['Content-Disposition'] = 'attachment; filename="Relatorio de Producao.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Produtividade')

    try:

        # Sheet header, first row
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        data1 = request.POST.get('data1') # Pegando data1 da pagina HTML (string)
        data2 = request.POST.get('data2') # Pegando data2 da pagina HTML (string)
        dataInicial = datetime.strptime(data1, '%Y-%m-%d').date() # Transformando string em datetime
        dataFinal = datetime.strptime(data2, '%Y-%m-%d').date() # Transformando string em datetime

        row_num = 0
        columns = []
        datas = []
        qtdDias = (dataFinal - dataInicial).days
        data = Calendario.objects.get(data=dataInicial)
        vrPago = float(request.POST.get('vrPago')) # Pegando valor da pagina HTML

        # Acrescentando as duas primeiras colunas
        columns.append('Código')
        columns.append('Funcionário')
        columns.append('Supervisor')
        columns.append('Empresa')
        columns.append('Meta')
        columns.append('Produção Total')
        columns.append('Vr Considerado')
        columns.append('Prêmio')
        columns.append('Dias Considerados')
        columns.append('Dias Úteis')
        columns.append('Média')
        columns.append('Efetiva')
        

        # Colocando datas numa lista
        for i in range(qtdDias):
            datas.append(date.fromordinal(data.data.toordinal()+i))
            if datas[i].weekday() == 5:
                columns.append('Sábado')
            elif datas[i].weekday() == 6:
                columns.append('Domingo')
            else:
                columns.append(format(datas[i], "%d/%m/%Y"))

        # Colocando as datas como colunas da planilha
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle() 

        funcionarios = buscarFuncionarios()
        funcionarios = buscarSupervisores_Empresa(funcionarios)
        funcionarios = buscarProducoes(funcionarios, datas, vrPago)

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

    
def buscarFuncionarios():

    """ Retornar todos os funcionarios que tem supervisor """
    query = Funcionario.objects.all().filter().values_list('codigo', 'nome', 'supervisor', 'cooperativa', 'meta')
    funcionarios = []
    for i in query:
        if i[2] != None:
            funcionarios.append([i[0], i[1], i[2], i[3], i[4]]) # codigo, nome, supervisor, empresa, meta
    return funcionarios


def buscarSupervisores_Empresa(funcionarios):

    """ Substitue os id de supervidor e empresa pelos nomes de cada um """
    for i in funcionarios:
        supervisor = Funcionario.objects.get(id=i[2])
        empresa = Cooperativa.objects.get(id=i[3])
        i[2] = supervisor.nome
        i[3] = empresa.nome
    return funcionarios

def countDiasUteis(datas):

    """ Retorna quantidade de dias uteis informadas no banco baseado numa listas de datas enviadas por parâmetro """
    totalDiasUteis = 0
    for i in datas:
        if Calendario.objects.get(data=i).diaUtil == 1:
            totalDiasUteis += 1
    return totalDiasUteis

def countFaltas(datas, funcionario):
    faltas = 0

    for i in datas:
        dia = Calendario.objects.get(data=i)
        query = Frequencia.objects.all().filter(dia=dia, funcionario=funcionario).values_list('presenca', 'justificada')
       
        if query.count() > 0:
            if query[0][0] == False and query[0][1] == False:
                faltas += 1
    return faltas


def buscarProducoes(funcionarios, datas, vrPago):

    import locale

    locale.setlocale(locale.LC_ALL, 'pt_BR') 
    # Aqui definimos que nosso local é Brasil 
    # e isso implica a utilização do R$ para o currency
    # além do uso do ponto para separar as casas de centenas, milhares etc
    # e a vírgula para separar os centavos

    faltas = 0
    diasUteis = countDiasUteis(datas)
    media = 0.00
    mediaEfetiva = 0.00
    producaoTotal = 0.00
    premio = 0.00

    for j in range(len(funcionarios)):

        funcionario = Funcionario.objects.get(codigo=funcionarios[j][0])
        funcionarios[j].append(producaoTotal) # Adiciona produção total do período
        funcionarios[j].append(vrPago) # Adiciona vr que será pago por kg
        funcionarios[j].append(premio) # Adiciona premio a ser pago
        funcionarios[j].append(diasUteis - countFaltas(datas, funcionario)) # Adiciona dias totais trabalhados
        funcionarios[j].append(diasUteis) # Adiciona dias úteis do período
        funcionarios[j].append(media) # Adiciona média de produção do período
        funcionarios[j].append(mediaEfetiva) # Adiciona média efetiva de produção do perído
        for i in datas:
            dia = Calendario.objects.get(data=i)
            query = ProducaoDiaria.objects.all().filter(dia=dia, funcionario=funcionario).values_list('producao')

            total = 0.00    # Acumulador de produção diária
            if query.count() != 0:
                for m in query:
                    total += float(m[0])     
                funcionarios[j].append(total)
            else:
                funcionarios[j].append(0.00)

    # Calculando as médias
    for i in funcionarios:
        coluna = 12
        for j in range(len(i) - 12): # Subtrai as primeiras colunas
            producaoTotal += i[coluna]
            coluna += 1
        i[5] = producaoTotal
        i[10] = round(producaoTotal / i[9], 2) # Média de produção
        i[11] =  round(producaoTotal / i[8], 2) # Média efetiva de produção

        i[7] = locale.currency((i[10]-float(i[4]))*i[9]*i[6], grouping=True) # Cálculo da premiação

        producaoTotal = 0
        
    return funcionarios





