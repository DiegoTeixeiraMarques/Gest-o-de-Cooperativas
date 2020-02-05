from django.test import TestCase
#from producao.models import ProducaoDiaria
#from funcionario.models import Funcionario
#from calendario.models import Calendario
import xlwt
from datetime import date
#from calendario.models import Calendario
from .models import ProducaoDiaria

# Create your tests here.
def exportar_producao():

    #response = HttpResponse(content_type='application/ms-excel')
    #response['Content-Disposition'] = 'attachment; filename="Producao_do_dia.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lançamentos')

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
    #data = Calendario.objects.get(data=data_atual)
    rows = ProducaoDiaria.objects.all().values_list('dia', 'funcionario', 'producao', 'usuario')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

            print(type(row))
            print('linha: ', row)

    #wb.save(response)
    return ws
exportar_producao()