from django.urls import path
from .views import index, ponto

app_name = 'salvarProducao'
urlpatterns = [
    path('', index, name="salvarProducao"),
    path('', ponto, name="informarFalta"),
]
