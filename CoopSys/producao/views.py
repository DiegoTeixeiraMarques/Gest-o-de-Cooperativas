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
from django.db import connection

def index(request):

    codigo = request.POST.get('codigo')
    dataBase = request.POST.get('dataBase')
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
        data = Calendario.objects.get(data=dataBase)
    except:
        data = date.today()
        dataBase = data
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
        producao = ProducaoDiaria.objects.all().filter(usuario=user, dia__data = dataBase).order_by('-created_at')[:5]
    except:
        producao = ProducaoDiaria.objects.all().filter(usuario=user, dia__data = dataBase).order_by('-created_at')
        #print("exceção")
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
    #print("Qtd de consultas: ", len(connection.queries))
    return render(request, template_name, context)
    
def relatorio(request):

    template_name = 'relatorios.html'
    data_atual = date.today()
    context = {
        'data_atual': data_atual
    }

    return render(request, template_name, context)

def pegarPeso():

    listaPortas = ['com4', 'com3', 'com2', 'com1', 'com5']
    porta = 0
    new_weight = ""
    while new_weight == "":

        try:
            __message = str(chr(5))
            _serial = serial.Serial(
                listaPortas[porta],
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
                #new_weight = 0
                
            else:
                #print("fechado")
                new_weight = 0
        except:
            #print("exceção na pesagem")
            new_weight = 0
        porta = porta + 1
        #print(listaPortas[porta])
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

### Relatório Otimizado

def exportar_producao_semanal(request):

    try:
    ##### Capturando dados da página HTML

        data1 = request.POST.get('data1')
        data2 = request.POST.get('data2')
        vrPago = float(request.POST.get('vrPago')) # Pegando valor da pagina HTML
        fechamento = request.POST.get('fechamento') # "ok" indica que os dados serão salvos na tabela de fechamento
        dataInicial = datetime.strptime(data1, '%Y-%m-%d').date()  # Transformando string em datetime
        dataFinal = datetime.strptime(data2, '%Y-%m-%d').date()  # Transformando string em datetime

    ##### Carregando os dados do banco

        producoes = list(ProducaoDiaria.objects.filter(dia__data__gte = dataInicial, dia__data__lte = dataFinal).values('funcionario__nome', 'funcionario__matricula', 'funcionario__codigo','funcionario__supervisor__codigo', 'funcionario__supervisor__nome', 'producao', 'dia__data'))
        supervisores = list(Funcionario.objects.filter(funcao='F', ativo=True).values('matricula', 'codigo', 'nome', 'salario', 'cooperativa__nome', 'funcao', 'meta'))
        faltas = list(Frequencia.objects.filter(dia__data__gte = dataInicial, dia__data__lte = dataFinal, presenca = 0).values('dia__data', 'funcionario__codigo', 'justificada'))
        datas = list(Calendario.objects.filter(data__gte = dataInicial, data__lte = dataFinal).values('data', 'diaUtil'))
        remuneracoes = list(Remuneracao.objects.filter().values('faixaInicial', 'faixaFinal', 'percentualFiscal', 'percentualEncarregada'))
        encarregadas = list(Funcionario.objects.filter(funcao='E').values('matricula', 'codigo', 'nome', 'salario', 'funcao', 'meta'))

    ##### Criando planilha e informando os parâmetros do relatório

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Relatorio de Premiacao.xls"'
        wb = xlwt.Workbook(encoding='utf-8')

        # Escolhendo a fonte e deixando negrito a primeira linha (cabeçalho)
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        # Nomeando Plan
        ws = wb.add_sheet("Parametros")

        # Listando parâmetros
        ws.write(0, 0, "Parametros utilizados", font_style)
        ws.write(2, 0, "Emissão: ", font_style)
        ws.write(3, 0, "Data Inicial: ", font_style)
        ws.write(4, 0, "Data Final: ", font_style)
        ws.write(5, 0, "Valor Pago (R$/Kg): ", font_style)
        ws.write(6, 0, "Executou Fechamento? ", font_style)

        ws.write(2, 1, str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day) , font_style)
        ws.write(3, 1, data1, font_style)
        ws.write(4, 1, data2, font_style)
        ws.write(5, 1, str(vrPago), font_style)
        ws.write(6, 1, "Sim" if fechamento == "ok" else "Não", font_style)

    #### Pegando variáveis globais

        colunas = ['Funcionario', 'Matricula']
        cabecalho = []  # Contem o intervalo de datas semanal
        qtdDias = (dataFinal - dataInicial).days + 1 
        qtdSemanas = 0
        diasRestantes = 0
        datasSeparadas = []

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
            colunas.append('Premio R$')
            colunas.append('Dias MEF')
            colunas.append('Dias MGE')

        # Separando datas
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

        # Criando cabeçalhos do intervalo de dias incluindo os dias restantes
        for i in datasSeparadas:
            cabecalho.append('  Dia ' + str(i[0]['data'].day) + ' à ' + str(i[-1]['data'].day) + '  ')
        cabecalho.append('  Total: Dia ' + str(datasSeparadas[0][0]['data'].day) + ' à ' + str(datasSeparadas[-1][-1]['data'].day) + '  ')

        # Quantidade de dias Úteis
        diasUteis = 0
        for data in datas:
            if (data['diaUtil'] == True):
                diasUteis = diasUteis + 1

        # DatasSeparadas para String
        dias = []
        datasSeparadasStr = []
        for i in datasSeparadas:
            for j in i:
                dias.append(str(j['data']))
            datasSeparadasStr.append(dias)
            dias = []
        
    ##### Construindo planilhas

        
        totalGeralEncarregada = 0.00 # Para premiação da Encarregada
        premiacaoTotalEncarregada = 0.00

        for supervisor in supervisores:
            # Definindo fonte
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            # Nomeando Plan
            ws = wb.add_sheet(supervisor['nome'])

            # Listando primeiras informações
            ws.write(0, 0, supervisor['cooperativa__nome'], font_style)
            ws.write(1, 0, "Fiscal: " + supervisor['nome'], font_style)
            ws.write(1, 1, supervisor['matricula'], font_style)

            # Listando cabeçalhos de datas
            num_lin = 4
            salto_coluna = 2
            for num_col in range(len(cabecalho)):
                ws.write(num_lin, salto_coluna, cabecalho[num_col], font_style)
                salto_coluna = salto_coluna + 1
                ws.write(num_lin, salto_coluna, cabecalho[num_col], font_style)
                salto_coluna = salto_coluna + 1
                ws.write(num_lin, salto_coluna, cabecalho[num_col], font_style)
                salto_coluna = salto_coluna + 1
                
            # Listando colunas
            num_lin = 5
            for num_col in range(len(colunas)):
                ws.write(num_lin, num_col, colunas[num_col], font_style)

            # Capturando produções da equipe do Fiscal
            producoesFiscal = []
            for prod in producoes:
                if (prod['funcionario__supervisor__codigo'] == supervisor['codigo']):
                    producoesFiscal.append(prod)

            # Buscando funcionários do Fiscal
            funcionarios = list(Funcionario.objects.filter(supervisor__codigo=supervisor['codigo'], ativo=True).values('nome', 'matricula', 'codigo', 'salario', 'meta', 'funcao'))

            # Listando Funcionários, Matrículas e Produção
            num_lin = 6
            num_col = 2

            totalEquipeFiscal = 0.00 # Para premiação da Fiscal

            for funcionario in funcionarios:

                ws.write(num_lin, 0, funcionario['nome'], font_style)
                ws.write(num_lin, 1, funcionario['matricula'], font_style)

                # Totais Mês
                faltasMes = 0
                justificadasMes = 0   
                totalMes = 0.00

                for datasSemana in datasSeparadasStr:
                    # Totais Semana
                    totalSemana = 0.00
                    faltasSemana = 0
                    justificadasSemana = 0
                    diasUteisSemana = 0
                    # Pega produções
                    for producao in producoesFiscal:
                        if(producao['funcionario__codigo'] == funcionario['codigo'] and str(producao['dia__data']) in datasSemana):
                            totalSemana = totalSemana + float(producao['producao'])
                    # Pega faltas
                    for falta in faltas:
                        if(falta['funcionario__codigo'] == funcionario['codigo'] and str(falta['dia__data']) in datasSemana):
                            faltasSemana = faltasSemana + 1
                            if falta['justificada'] == True:
                                justificadasSemana = justificadasSemana + 1
                    # Pega dias úteis
                    for data in datasSemana:
                        for data2 in datas:
                            if (data == str(data2['data']) and data2['diaUtil'] == True):
                                diasUteisSemana = diasUteisSemana + 1


                    diasMEFSemana =  diasUteisSemana - faltasSemana
                    diasMGESemana = diasUteisSemana - (faltasSemana - justificadasSemana)

                    try:
                        MEFSemana = round(totalSemana / diasMEFSemana, 2)
                    except:
                        MEFSemana = 0.00
                    try:
                        MGESemana = round(totalSemana / diasMEFSemana, 2)
                    except:
                        MGESemana = 0.00

                    ws.write(num_lin, num_col, totalSemana, font_style)
                    ws.write(num_lin, num_col+1, MEFSemana, font_style)
                    ws.write(num_lin, num_col+2, MGESemana, font_style)

                    justificadasMes = justificadasMes + justificadasSemana
                    faltasMes = faltasMes + faltasSemana
                    totalMes = totalMes + totalSemana

                    num_col = num_col + 3

                diasEfetivosMes = diasUteis - faltasMes
                diasMediaGeralMes = diasUteis - (faltasMes - justificadasMes)
                MEFMes = round(totalMes / diasEfetivosMes, 2)
                MGEMes = round(totalMes / diasMediaGeralMes, 2)
                premio = (MGEMes - float(funcionario['meta'])) * diasMediaGeralMes * vrPago # Calculo do premio

                if (premio < 0.00):
                    premio = 0.00

                ws.write(num_lin, len(colunas) - 6, totalMes, font_style)
                ws.write(num_lin, len(colunas) - 5, MEFMes, font_style)
                ws.write(num_lin, len(colunas) - 4, MGEMes, font_style)
                ws.write(num_lin, len(colunas) - 3, premio, font_style)
                ws.write(num_lin, len(colunas) - 2, diasEfetivosMes, font_style)
                ws.write(num_lin, len(colunas) - 1, diasMediaGeralMes, font_style)

                #ws.write(num_lin, len(colunas) + 1, diasUteis, font_style)  # Auditoria de dias úteis
                #ws.write(num_lin, len(colunas) + 2, faltasMes, font_style)  # Auditoria de faltas

                num_lin = num_lin + 1
                num_col = 2

                totalEquipeFiscal = totalEquipeFiscal + totalMes

                if fechamento == 'ok': # Verifica se a rotina de fechamento foi acionada para salvar os dados na tabela de fechamento
                    matricula = funcionario['matricula']
                    nome = funcionario['nome']
                    funcao = funcionario['funcao']
                    meta = funcionario['meta']
                    salario = funcionario['salario']
                    producaoTotal = totalMes
                    vrPagoKG = vrPago
                    premio = premio
                    referencia = datas[-1]['data']

                    registro = Fechamento(matricula=matricula, nome=nome, funcao=funcao, meta=meta, salario=salario, producaoTotal=producaoTotal, vrPagoKG=vrPagoKG, premio=premio, referencia=referencia)
                    registro.save()

            totalGeralEncarregada = totalGeralEncarregada + totalEquipeFiscal

            # Contabilização final do prêmio da fiscal e encarregada
            if len(funcionarios) == 0:
                mediaEquipeFiscal = 0
                mediaFinalFiscal = 0
            else:
                mediaEquipeFiscal = round(totalEquipeFiscal / len(funcionarios), 2)
                mediaFinalFiscal = round(mediaEquipeFiscal / diasUteis, 2)

            # Pegando percentual de premiação
            if mediaFinalFiscal > 0:
                for remuneracao in remuneracoes:

                    if mediaFinalFiscal <= float(remuneracao['faixaFinal']) and mediaFinalFiscal >= float(remuneracao['faixaInicial']):
                        
                        percentualFiscal = float(remuneracao['percentualFiscal'])
                        percentualEncarregada = float(remuneracao['percentualEncarregada'])
                        break

                    else:
                      
                        percentualFiscal = 0
                        percentualEncarregada = 0
            else:
                percentualFiscal = 0
                percentualEncarregada = 0

            premiacaoFiscal = round(float(supervisor['salario']) * (percentualFiscal/100), 2)
            premiacaoEncarregada = round(float(encarregadas[0]['salario']) * (percentualEncarregada/100), 2)

            if (premiacaoFiscal < 0.00):
                premiacaoFiscal = 0.00

            if (premiacaoEncarregada < 0.00):
                premiacaoEncarregada = 0.00

            premiacaoTotalEncarregada = premiacaoTotalEncarregada + premiacaoEncarregada

            ws.write(2, 0, 'Prêmio Fiscal R$: ', font_style)
            ws.write(2, 1, premiacaoFiscal, font_style)
            ws.write(3, 0, 'Prêmio Encar. R$: ', font_style)
            ws.write(3, 1, premiacaoEncarregada, font_style)

            if fechamento == 'ok': # Verifica se a rotina de fechamento foi acionada para salvar os dados na tabela de fechamento
                matricula = supervisor['matricula']
                nome = supervisor['nome']
                funcao = supervisor['funcao']
                meta = supervisor['meta']
                salario = supervisor['salario']
                producaoTotal = totalEquipeFiscal
                vrPagoKG = vrPago
                premio = premiacaoFiscal
                referencia = datas[-1]['data']

                registro = Fechamento(matricula=matricula, nome=nome, funcao=funcao, meta=meta, salario=salario, producaoTotal=producaoTotal, vrPagoKG=vrPagoKG, premio=premio, referencia=referencia)
                registro.save()

        if fechamento == 'ok': # Verifica se a rotina de fechamento foi acionada para salvar os dados na tabela de fechamento
            matricula = encarregadas[0]['matricula']
            nome = encarregadas[0]['nome']
            funcao = encarregadas[0]['funcao']
            meta = encarregadas[0]['meta']
            salario = encarregadas[0]['salario']
            producaoTotal = totalGeralEncarregada
            vrPagoKG = vrPago
            premio = premiacaoTotalEncarregada
            referencia = datas[-1]['data']

            registro = Fechamento(matricula=matricula, nome=nome, funcao=funcao, meta=meta, salario=salario, producaoTotal=producaoTotal, vrPagoKG=vrPagoKG, premio=premio, referencia=referencia)
            registro.save()

        # Plan dados gerais de produção do mês
        ws = wb.add_sheet('Produções registradas')
        # Colunas
        ws.write(0, 0, 'Funcionário', font_style)
        ws.write(0, 1, 'Matrícula', font_style)
        ws.write(0, 2, 'Código', font_style)
        ws.write(0, 3, 'Cod. Fiscal', font_style)
        ws.write(0, 4, 'Fiscal', font_style)
        ws.write(0, 5, 'Produção', font_style)
        ws.write(0, 6, 'Dia', font_style)
        # Linhas
        linha = 1
        for producao in producoes:

            ws.write(linha, 0, producao['funcionario__nome'], font_style)
            ws.write(linha, 1, producao['funcionario__matricula'], font_style)
            ws.write(linha, 2, producao['funcionario__codigo'], font_style)
            ws.write(linha, 3, producao['funcionario__supervisor__codigo'], font_style)
            ws.write(linha, 4, producao['funcionario__supervisor__nome'], font_style)
            ws.write(linha, 5, producao['producao'], font_style)
            ws.write(linha, 6, producao['dia__data'].strftime('%d/%m/%Y'), font_style)

            linha = linha + 1
            
            
        wb.save(response)
        #print("Qtd de consultas relatorio", len(connection.queries))
        return response

    except:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Incosistências nos dados.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Erro')
        # Definindo fonte
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        # Listando primeiras informações
        ws.write(0, 0, "1 - Verifique o intervalo de datas e se informou o valor a ser pago por KG. Ex.: 0,90", font_style)
        ws.write(1, 0, "2 - Verifique se todos os salários estão inseridos", font_style)
        ws.write(2, 0, "3 - Verifique se todas as datas no sitema estão corretas", font_style)
        ws.write(3, 0, "4 - Verifique se todos funcionrios possuem função cadastrada e se há somente um(a) encarregado(a)", font_style)
        ws.write(4, 0, "5 - Contacte o administrador", font_style)
        wb.save(response)
        return response
