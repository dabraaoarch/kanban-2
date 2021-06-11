from django.urls import path

from . import views

app_name="pecas"

urlpatterns = [
    path(
        '',
        views.PecasListView.as_view(),
        name='index'
    ),
    path(
        '<int:peca_id>/',
        views.AplicacaoListView.as_view(),
        name='aplicacoes'
    ),
    path(
        'nova_peca/',
        views.NovaPecaView.as_view(),
        name='nova_peca'
    ),
    path(
        'remover_peca/<int:peca_id>',
        views.remover_peca,
        name='remover_peca'),
    path(
        'remover_aplicacao/<int:aplicacao_id>',
        views.remover_aplicacao,
        name='remover_aplicacao'
    ),
    path(
        'gravitacionais/',
        views.GravitacionalListView.as_view(),
        name='gravitacionais'
    ),
    path(
        'novo_gravitacional/',
        views.NovoGravitacionalView.as_view(),
        name='novo_gravitacional'
    ),
    path(
        'gerir_gravitacional/<int:gravitacional_id>',
        views.GerirGravitacionalView.as_view(),
        name='gerir_gravitacional'
    ),
    path(
        'remover_gravitacional/<int:gravitacional_id>',
        views.remover_gravitacional,
        name='remover_gravitacional'
    ),
    path(
        'imprimir_etiquetas/<int:gravitacional_id>',
        views.EtiquetasListView.as_view(),
        name='imprimir_etiquetas'
    ),
    path(
        'abastecimento/<tipo_pedido>/',
        views.PedidosListView.as_view(),
        name='pedidos'
    ),
    path(
        'apagar_abastecimento/<int:abastecimento_id>',
        views.apagar_abastecimento,
        name='apagar_abastecimento'
    ),
    
]
