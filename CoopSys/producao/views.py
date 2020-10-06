from django.shortcuts import render, HttpResponse
from .models import ProducaoDiaria
from funcionario.models import Funcionario
from calendario.models import Calendario
from django.contrib.auth.models import User
from cooperativa.models import Cooperativa
from frequencia.models import Frequencia
from remuneracao.models import Remuneracao
from fechamento.models import Fechamento
from datetime import date, datetime
import serial
import pdb
import xlwt
import locale
import math

def index(request):

    codigo = request.POST.get('codigo')
    dataBase = request.POST.get('dataBase')
    data = dataBase
    hoje = date.today()

    try:
        user = request.user.id
        funcionario = Funcionario.objects.get(codigo=codigo)
        usuario = User.objects.get(id=user)
    except:
        msg = 'Código não localizado!'
    try:
        peso = pegarPeso()
    except:
        msg = 'Problema ao pegar o peso da balança!'
    try:
        data = Calendario.objects.get(data=data)
    except:
        msg = 'Data não informada ou não cadastrada!'
    try:
        producaoNova = ProducaoDiaria(dia=data, funcionario=funcionario, producao=peso, usuario=usuario)
        producaoNova.save()
        msg = 'Salvo com Sucesso!'
    except:
        if codigo == None:
            msg = '...'
        else:
            pass
    try:
        tam = len(ProducaoDiaria.objects.all().filter(usuario=user, dia__data = dataBase)) - 5
        producao = ProducaoDiaria.objects.all().filter(usuario=user, dia__data = dataBase)[tam:]
    except:
        producao = ProducaoDiaria.objects.all().filter(usuario=user, dia__data = dataBase)
    try:
        template_name = 'index.html'
        context = {
            'producao': producao,
            'msg': msg,
            'data_base': data,
            'hoje': hoje
        }
    except:
        template_name = 'index.html'
        msg = 'Erro'
        data_atual = date.today()
        context = {
            'producao': producao,
            'msg': msg,
            'data_base': data,
            'hoje': hoje
        }
    return render(request, template_name, context)
    

def relatorio(request):

    template_name = 'relatorios.html'
    data_atual = date.today()
    context = {
        'data_atual': data_atual
    }

    return render(request, template_name, context)

def relatoriodiadia(request):

    template_name = 'relatorioSupervisor.html'
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
            #print("aberto")
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
            new_weight = 0
    except:
        #print("exceção")
        new_weight = 35
    

    return (new_weight)


def exportar_producao_dia(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Producao_do_dia.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lançamentos')
    try:
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Dia', 'Matricula', 'Funcionario', 'Producao', 'Usuario', 'Unidade']
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
            B = Funcionario.objects.get(id=rows[i][1]).matricula
            C = Funcionario.objects.get(id=rows[i][1]).nome
            D = rows[i][2]
            E = User.objects.get(id=rows[i][3]).username
            F = Funcionario.objects.get(id=rows[i][1]).cooperativa.nome
            rows2.append([A, B, C, D, E, F])
        for row in rows2:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)          
        wb.save(response)
        return response
    except:    
        #print('Exceção!')
        wb.save(response)
        return response

def pegarSupervisores():
    s = Funcionario.objects.filter(supervisor__isnull = False) # Pegando todos os funcionarios que tem supervisor informado no cadastro
    # Loop para filtrar apenas os supervisores únicos dentro de todos os funcionários encontrados no banco
    supervisores = []
    for i in s:
        id = i.supervisor
        if id not in supervisores:
            supervisores.append(id) 
    return supervisores

def pegarProducoes(dataInicial, dataFinal):
    # Pegando os dados de producao no intervalo de datas informadas
    return ProducaoDiaria.objects.filter(dia__data__gte = dataInicial, dia__data__lte = dataFinal).select_related('funcionario', 'dia')

def pegarDatasSemanal(dataInicial, dataFinal):
    # Criando variáveis necessárias
    datas = []
    colunas = []
    qtdDias = (dataFinal - dataInicial).days + 1 
    data = Calendario.objects.get(data=dataInicial)
    qtdSemanas = 0
    diasRestantes = 0

    # Ex.: [ ['Nome'],['Matricula'],['data1'],['data2'], ..., ['Dias Uteis'], ['Dias Efetivos'], ['Média'], ['Efetiva'], ['Soma'] ]
    colunas.insert(0, 'Matricula')
    colunas.insert(0, 'Funcionario')

    # Verificando se existe qtd de dias para rodar o loop
    if qtdDias == 0:
         qtdDias = 1

    # Verificando se intervalo de datas ultrapassa uma semana
    if qtdDias > 7:
        qtdSemanas = qtdDias // 7 # Quantidade de semanas
        diasRestantes = qtdDias % 7 # Dias que sobram
        # Montando a lista dos cabeçalhos da planilha
        for i in range(qtdSemanas):
            colunas.append('KG')
            colunas.append('MEF')
            colunas.append('MGE')
        if diasRestantes > 0:
            colunas.append('KG')
            colunas.append('MEF')
            colunas.append('MGE')
        # Totais
        colunas.append('KG')
        colunas.append('M.EF.')
        colunas.append('M.GE.')
        colunas.append('PREMIO R$')
        colunas.append('DIAS MEF')
        colunas.append('DIAS MGE')

    # Colocando datas numa lista
    for i in range(qtdDias):
        datas.append(date.fromordinal(data.data.toordinal()+i))
    return colunas, datas, qtdSemanas, diasRestantes

def countDiasUteis(datas):

    """ Retorna quantidade de dias uteis informadas no banco baseado numa listas de datas enviadas por parâmetro """
    try:
        totalDiasUteis = 0
        for i in datas:
            if Calendario.objects.get(data=i).diaUtil == 1:
                totalDiasUteis += 1
        return totalDiasUteis
    except:
        return 'Erro'

def countFaltasSemanal(datas, funcionario):

    """ Retorna quantidade de faltas de um funcionario recebido por parametro junto com o periodo """
    try:
        faltas = 0
        for i in datas:
            dia = Calendario.objects.get(data=i)
            query = Frequencia.objects.all().filter(dia=dia, funcionario=funcionario[0]).values_list('presenca', 'justificada')
        
            if query.count() > 0:
                if query[0][0] == False and query[0][1] == False: # Faltas não justificadas
                    faltas += 1
        
        return faltas
    except:
        return 'Erro'

def countTodasFaltas(datas, funcionario):

    """ Retorna quantidade de faltas de um funcionario recebido por parametro junto com o periodo """
    try:
        faltas = 0
        for i in datas:
            dia = Calendario.objects.get(data=i)
            query = Frequencia.objects.all().filter(dia=dia, funcionario=funcionario[0]).values_list('presenca', 'justificada')
        
            if query.count() > 0:
                if query[0][0] == False: #and query[0][1] == True
                    faltas += 1
        
        return faltas
    except:
        return 'Erro'

def countFaltas(datas, funcionario):
    faltas = 0

    for i in datas:
        dia = Calendario.objects.get(data=i)
        query = Frequencia.objects.all().filter(dia=dia, funcionario=funcionario).values_list('presenca', 'justificada')
       
        if query.count() > 0:
            if query[0][0] == False and query[0][1] == False:
                faltas += 1
    return faltas

def converterLinhasSemanal(producoes, datas, supervisor, qtdSemanas, diasRestantes, vrPago, remuneracoes, fechamento):

    """ Prepara a lista para ser inserida como linhas na planilha do relatório """

    funcionarios = []
    # Ex.: [ ['Nome'], ['Matricula'], ['KG'], ['MEF'], ['MGE'], ..., ['ACUMULADO KG'], ['ACUMULADO MEF'], ['ACUMULADO MGE'], ['PREMIO'], ['DIAS UTEIS'], ['DIAS EFETIVOS'] ]
    linhas = []
    datasSeparadas = datas
    diasUteisGeral = countDiasUteis(datas)

    # Para calculo do prêmio da Fiscal
    totalEquipe = 0
    mediaEquipe = 0
    salarioFiscal = float(supervisor.salario)
    salarioEncarregada = float(Funcionario.objects.get(funcao = 'E').salario)
    qtdFuncionarios = 0

    # linhas = [[func1], [func2], [func3], ...]
    for i in producoes:
        if (i.funcionario not in funcionarios) and (i.funcionario.supervisor == supervisor):
            funcionarios.append(i.funcionario)
            linhas.append([i.funcionario, i.funcionario.matricula])

    if (qtdSemanas == 1 and diasRestantes > 0) or (qtdSemanas > 1) :
        datasSeparadas = [] # [[data1, ..., data7], [data1, ..., data7], [data1, data2, data3, ...]]

        # Separando as datas em semanas
        for semana in range(qtdSemanas):
            posicao1 = semana * 7 # Pega a primeira data da semana do loop
            posicao2 = posicao1 + 7 # Pega a última data da semana do loop
            dias = datas[posicao1:posicao2]
            datasSeparadas.append(dias)
        if diasRestantes > 0:
            dias = datas[-diasRestantes:]
            if type(dias) == list:
                datasSeparadas.append(dias)
            else:
                datasSeparadas.append([dias])
    
        # Criando linhas
        for i in linhas:
            diasEfetivosGeral = diasUteisGeral - countTodasFaltas(datas, i) # F - Para calculo da media efetiva
            diasMediaGeral = diasUteisGeral - countFaltasSemanal(datas, i) # E - Para calculo da media geral, faltas não justificadas
            totalGeral = 0
            for datasSep in datasSeparadas:
                diasUteis = countDiasUteis(datasSep)
                diasEfetivos = int(diasUteis) - int(countTodasFaltas(datasSep, i)) # F, Todas as faltas, para calculo da media efetiva
                diasMedia = int(diasUteis) - int(countFaltasSemanal(datasSep, i)) # E - Para calculo da media geral, faltas não justificadas
                totalSemana = 0
                for d in datasSep:
                    for j in producoes:
                        if j.funcionario == i[0] and j.dia.data == d:
                            totalSemana = totalSemana + float(j.producao) # Produção total do funcionário da semana no loop
                            totalGeral = totalGeral + float(j.producao) # Produção total do período
                
                i.append(totalSemana) # Kg total da semana
                if diasEfetivos > 0:
                    i.append(round(totalSemana / diasEfetivos, 2)) # Efetiva Semana
                else:
                    i.append(0)
                if diasMedia > 0:
                    i.append(round(totalSemana / diasMedia, 2)) # Media Semana
                else:
                    i.append(0)
            i.append(totalGeral) # Kg total da semana
            if diasEfetivosGeral > 0:
                i.append(round(totalGeral / diasEfetivosGeral, 2)) # Efetiva Mes
            else:
                i.append(0)
            if diasMediaGeral > 0:
                i.append(round(totalGeral / diasMediaGeral, 2)) # Media Mes
            else:
                i.append(0)
            mediaGeral = round(totalGeral / diasMediaGeral, 2)
            premio = (float(mediaGeral) - float(i[0].meta)) * diasMediaGeral * vrPago # Calculo do premio
            if premio < 0:
                i.append(0.00)
            else:
                i.append(premio) # Prêmio
            i.append(diasEfetivosGeral) # Para media efetiva, dias uteis menos todas as faltas
            i.append(diasMediaGeral) # Para media geral, dias uteis menos faltas nao justificadas

            # Cálculo da premiação fiscal
            totalEquipe = totalEquipe + totalGeral
            qtdFuncionarios = qtdFuncionarios + 1

            if fechamento == 'ok': # Verifica se a rotina de fechamento foi acionada para salvar os dados na tabela de fechamento
                matricula = i[0].matricula
                nome = i[0].nome
                funcao = i[0].funcao
                meta = i[0].meta
                salario = i[0].salario
                producaoTotal = totalGeral
                vrPagoKG = vrPago
                premio = premio
                referencia = datas[-1]

                registro = Fechamento(matricula=matricula, nome=nome, funcao=funcao, meta=meta, salario=salario, producaoTotal=producaoTotal, vrPagoKG=vrPagoKG, premio=premio, referencia=referencia)
                registro.save()

        # Contabilização final do prêmio da fiscal
        if qtdFuncionarios == 0:
            mediaEquipe = 0
            mediaFinal = 0
        else:
            mediaEquipe = round(totalEquipe / qtdFuncionarios,2)
            mediaFinal = round(mediaEquipe / diasUteisGeral,2)

        # Pegando percentual de premiação
        if mediaFinal > 0:
            for i in remuneracoes:
                if mediaFinal <= i.faixaFinal and mediaFinal >= i.faixaInicial:
                    percentualFiscal = float(i.percentualFiscal)
                    percentualEncarregada = float(i.percentualEncarregada)
        else:
            percentualFiscal = 0
            percentualEncarregada = 0

        premiacaoFiscal = round(salarioFiscal * (percentualFiscal/100), 2)
        premiacaoEncarregada = round(salarioEncarregada * (percentualEncarregada/100), 2)
    else:
        for i in linhas:
            producaoDia = 0.00
            total = 0
            diasUteis = countDiasUteis(datas)
            diasEfetivos = int(diasUteis) - int(countTodasFaltas(datas, i)) # F, Todas as faltas, para calculo da media efetiva
            diasMedia = int(diasUteis) - int(countFaltasSemanal(datas, i)) # E - Para calculo da media geral, faltas não justificadas
            for d in datas:
                for j in producoes:
                    if j.funcionario == i[0] and j.dia.data == d:
                        producaoDia = producaoDia + float(j.producao) # Produção total do funcionário em cada dia
                        total = total + float(j.producao) # Produção total do funcionario no período
                i.append(producaoDia)
                producaoDia = 0.00
            i.append(diasUteis) # Dias Uteis
            i.append(diasEfetivos) # Faltas
            if diasMedia > 0:
                i.append(round(total / diasMedia, 2)) # Media Geral
            else:
                i.append(0)
            if diasEfetivos > 0:
                i.append(round(total / diasEfetivos, 2)) # Efetiva
            else:
                i.append(0)
            i.append(round(total, 2)) # Soma Total

            totalEquipe = totalEquipe + total
            qtdFuncionarios = qtdFuncionarios + 1

            # Contabilização final do prêmio da fiscal
        if qtdFuncionarios == 0:
            mediaEquipe = 0
            mediaFinal = 0
        else:
            mediaEquipe = round(totalEquipe / qtdFuncionarios,2)
            mediaFinal = round(mediaEquipe / diasUteisGeral,2)

        # Pegando percentual de premiação
        if mediaFinal > 0:
            for i in remuneracoes:
                if mediaFinal <= i.faixaFinal and mediaFinal >= i.faixaInicial:
                    percentualFiscal = float(i.percentualFiscal)
                    percentualEncarregada = float(i.percentualEncarregada)
        else:
            percentualFiscal = 0
            percentualEncarregada = 0

        premiacaoFiscal = round(salarioFiscal * (percentualFiscal/100), 2)
        premiacaoEncarregada = round(salarioEncarregada * (percentualEncarregada/100), 2)

    return linhas, datasSeparadas, premiacaoFiscal, premiacaoEncarregada

def criarPlanilhaSupervisorSemanal(wb, supervisor, colunas, linhas, datasSeparadas, premiacaoFiscal, premiacaoEncarregada):
    
    #Criando variavéis necessárias
    ws = wb.add_sheet(supervisor.nome)
    row_num = 0
    
    # Escolhendo a fonte e deixando negrito a primeira linha (cabeçalho)
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # Add nome da cooperativa na celula (A1, B1) e pula duas linhas para baixo
    ws.write(row_num, 0, supervisor.cooperativa.nome, font_style)
    ws.write(row_num+1, 0, supervisor.nome, font_style)
    ws.write(row_num+1, 1, "Prêmio Fiscal", font_style)
    ws.write(row_num+1, 2, premiacaoFiscal, font_style)
    ws.write(row_num+1, 3, "Prêmio Encarregada", font_style)
    ws.write(row_num+1, 4, premiacaoEncarregada, font_style)
    row_num += 2

    # Colocando intervalo de datas nas colunas da planilha [[01/01 a 07/01], [08/01 as 14/01]]
    posicaoColuna = 2
    for i in range(len(datasSeparadas)):
        intervaloDatas = datasSeparadas[i][0].strftime('%d/%m') + ' a ' + datasSeparadas[i][-1].strftime('%d/%m')
        ws.write(row_num, posicaoColuna, intervaloDatas, font_style)
        posicaoColuna = posicaoColuna + 3
    
    # Add intervalo de datas geral nos totalizadores
    intervaloDatas = datasSeparadas[0][0].strftime('%d/%m') + ' a ' + datasSeparadas[-1][-1].strftime('%d/%m')
    ws.write(row_num, posicaoColuna, intervaloDatas, font_style)

    row_num += 1

    # Colocando as colunas na planilha
    for col_num in range(len(colunas)):
        ws.write(row_num, col_num, colunas[col_num], font_style)
    
    # Mudando o estilo da fonte para inserção das linhas na planilha
    font_style = xlwt.XFStyle()

    for row in linhas:
        row_num += 1
        for col_num in range(len(row)):
            # Ex.: [ ['Nome'],['xxxxxx'],['xxxxxx'],['xxxxxx'], ... ]
            if col_num == 0:
                ws.write(row_num, col_num, row[col_num].nome, font_style)
            # [ ['xxxxx'],['Matricula'],['xxxxxx'],['xxxxxx'], ... ]
            elif col_num == 1:
                ws.write(row_num, col_num, row[col_num], font_style)
            # [ ['xxxxx'],['xxxxxx'],['data1'],['data2'], ... ]
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    return True

def exportar_producao_semanal(request):

    #try:
    # Pegando datas e valor informados na página HTML (string)
    data1 = request.POST.get('data1')
    data2 = request.POST.get('data2')
    vrPago = float(request.POST.get('vrPago')) # Pegando valor da pagina HTML
    fechamento = request.POST.get('fechamento') # "ok" indica que os dados serão salvos na tabela de fechamento

    # Transformando string em datetime
    dataInicial = datetime.strptime(data1, '%Y-%m-%d').date()
    dataFinal = datetime.strptime(data2, '%Y-%m-%d').date()

    # Carregando os dados necessários para construção dos relatórios
    producoes = pegarProducoes(dataInicial, dataFinal)
    supervisores = pegarSupervisores()
    colunas, datas, qtdSemanas, diasRestantes = pegarDatasSemanal(dataInicial, dataFinal)

    # Cria planilha de trabalho Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Relatorio de Producao Semanal.xls"'
    wb = xlwt.Workbook(encoding='utf-8')

    remuneracoes = Remuneracao.objects.all()

    for i in range(len(supervisores)):
        linhas, datasSeparadas, premiacaoFiscal, premiacaoEncarregada = converterLinhasSemanal(producoes, datas, supervisores[i], qtdSemanas, diasRestantes, vrPago, remuneracoes, fechamento)    
        criarPlanilhaSupervisorSemanal(wb, supervisores[i], colunas, linhas, datasSeparadas, premiacaoFiscal, premiacaoEncarregada)
    wb.save(response)
    return response
    #except:
        #response = HttpResponse(content_type='application/ms-excel')
        #response['Content-Disposition'] = 'attachment; filename="Relatorio de Producao.xls"'
        #wb = xlwt.Workbook(encoding='utf-8')
        #ws = wb.add_sheet('Produtividade')
        #wb.save(response)
        #return response
    
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


def buscarProducoes(funcionarios, datas, vrPago):
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

        faltas = countFaltas(datas, funcionario)

        funcionarios[j].append(diasUteis - faltas) # Adiciona dias totais trabalhados
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

        #Tratando divisão por zero
        if i[9] == 0:
            i[10] = 0
        else:
            i[10] = round(producaoTotal / i[9], 2) # Média de produção
        if i[8] == 0:
            i[11] = 0
        else:
            i[11] =  round(producaoTotal / i[8], 2) # Média efetiva de produção
        # Cálculo da premiação
        x = i[10]-float(i[4])
        if ( x*i[9]*i[6] ) > 0:
            i[7] = locale.currency((i[10]-float(i[4]))*i[9]*i[6], grouping=True)
        else:
            i[7] = locale.currency(0.00, grouping=True)
        producaoTotal = 0

    return funcionarios


### Produção dia a dia

def exportar_producao_diadia(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Prod dia a dia.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Produtividade')

    try:

        # Sheet header, first row
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        data1 = request.POST.get('data3') # Pegando data1 da pagina HTML (string)
        data2 = request.POST.get('data4') # Pegando data2 da pagina HTML (string)

        dataInicial = datetime.strptime(data1, '%Y-%m-%d').date() # Transformando string em datetime
        dataFinal = datetime.strptime(data2, '%Y-%m-%d').date() # Transformando string em datetime

        row_num = 0
        columns = []
        datas = []
        qtdDias = (dataFinal - dataInicial).days

        # Quando o relátorio é data inicial e final do mesmo dia
        if qtdDias == 0:
            qtdDias = 1
            
        data = Calendario.objects.get(data=dataInicial)
        vrPago = float(request.POST.get('vrPago1')) # Pegando valor da pagina HTML

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
        print('Exceção 01!')
        wb.save(response)
        return response