from django.urls import path
from .views import index

app_name = 'salvarProducao'
urlpatterns = [
    path('', index, name="salvarProducao"),
]
