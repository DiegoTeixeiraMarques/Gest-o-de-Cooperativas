from django.contrib import admin
from django.urls import path, include
from producao.views import index
from frequencia.views import apontarFalta

urlpatterns = [
    path('', admin.site.urls),
    path('jet/', include(('jet.urls', 'jet'))),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('salvarProducao/', index, name="salvarProducao"),
    path('account/', include('django.contrib.auth.urls')),
    path('apontarFalta/', apontarFalta, name="apontarFalta")
    #path('', include('producao.urls')),
]
