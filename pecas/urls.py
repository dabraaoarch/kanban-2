from django.urls import path

from . import views

app_name="pecas"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:peca_id>/', views.aplicacoes, name='aplicacoes'),
    path('nova_peca/', views.nova_peca, name='nova_peca')
    ]
