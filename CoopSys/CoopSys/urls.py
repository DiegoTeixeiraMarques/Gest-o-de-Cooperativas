from django.contrib import admin
from django.urls import path, include
from producao.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('salvarProducao/', index, name="salvarProducao"),
    path('', include('django.contrib.auth.urls')),
    #path('', include('producao.urls')),
]
