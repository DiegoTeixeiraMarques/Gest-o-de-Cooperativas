from django.contrib import admin
from django.urls import path, include
from producao.views import index, exportar_producao, relatorio, exportar_producao_dia
from frequencia.views import apontarFalta

urlpatterns = [
    path('', admin.site.urls),
    path('jet/', include(('jet.urls', 'jet'))),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('salvarProducao/', index, name="salvarProducao"),
    path('account/', include('django.contrib.auth.urls')),
    path('account/', apontarFalta, name="apontarFalta"),
    path('exportar_producao/', exportar_producao, name='exportar_producao'),
    path('exportar_producao_dia', exportar_producao_dia, name='exportar_producao_dia'),
    path('relatorios/', relatorio, name="relatorio"),
    #path('', include('producao.urls')),
]
