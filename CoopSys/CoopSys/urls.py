from django.contrib import admin
from django.urls import path, include
from producao.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="salvarProducao"),
    #path('', include('producao.urls')),
]
