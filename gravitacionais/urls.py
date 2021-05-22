from django.urls import path
from . import views

app_name="gravitacionais"

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'novo_gravitacional',
        views.novo_gravitacional,
        name='novo_gravitacional'
    ),
    path(
        'gerir_gravitacional/<int:gravitacional_id>',
        views.gerir_gravitacional,
        name='gerir_gravitacional'
    ),
    path(
        'remover_aplicacao/<int:aplicacao_id>',
        views.remover_aplicacao,
        name='remover_aplicacao'
    ),
    path(
        'imprimir_etiquetas/<int:gravitacional_id>',
        views.imprimir_etiquetas,
        name='imprimir_etiquetas'
    )
    ]
