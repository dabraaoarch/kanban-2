from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Gravitacional, Peca, Aplicacao
from ..views import EtiquetasListView
from .cria_objetos import *

class GeraEtiquetaTests(TestCase):
    def setUp(self):
        if not User.objects.exists():
            user = cria_usuario()
            self.user = self.client.force_login(
                user = user
            )
        
    def load_page(self, gravitacional_id=None):
        '''
        Load page with the id informed and return the result
        '''
        if gravitacional_id != None:
            url = reverse(
                'pecas:imprimir_etiquetas',
                kwargs={
                    'gravitacional_id' : gravitacional_id
                }
            )
            return self.client.get(url)
        return None

    def test_gera_etiqueta_status_code(self):
        '''
        Test if the page return code for a valid gravitacional
        is equal to 200
        '''
        aplicacao = cria_aplicacao()
        gravitacional_id = aplicacao.gravitacional_aplicacao.id
        response = self.load_page(
            gravitacional_id = gravitacional_id
        )
        self.assertEquals(response.status_code, 200)

    def test_gera_etiqueta_context(self):
        '''
        Validates the context received
        '''
        aplicacao = cria_aplicacao()
        gravitacional_id = aplicacao.gravitacional_aplicacao.id
        response = self.load_page(
            gravitacional_id = gravitacional_id
        )
        self.assertQuerysetEqual(
            response.context['aplicacoes'],
            [aplicacao]
        )
        
        
    def test_gera_etiqueta_content(self):
        '''
        If the gravitacinal has one aplicacao, the page rendered must
        contain two tables, two barcodes and no links
        '''
        aplicacao = cria_aplicacao()
        gravitacional_id = aplicacao.gravitacional_aplicacao.id
        response = self.load_page(
            gravitacional_id = gravitacional_id
        )
        codigo_barras = "*" + aplicacao.gravitacional_aplicacao.codigo \
            + "*" + aplicacao.peca_aplicacao.codigo_peca + "*" + \
            str(aplicacao.id) + "*"
        codigo_peca = aplicacao.peca_aplicacao.codigo_peca
        nome_peca  = aplicacao.peca_aplicacao.nome_peca
        self.assertContains(response, "<a", 0)
        self.assertContains(response, "<table", 2)
        self.assertContains(response, "class='codigo-barras", 2)
        self.assertContains(response, codigo_barras, 2)
        self.assertContains(response, "<td>"+codigo_peca+"</td>", 2)
        self.assertContains(response, nome_peca, 2)

    def test_gera_etiqueta_invalid_gravitacional(self):
        '''
        If an ivalid gravitacional ID is informed, it must return
        a 404.
        '''        
        response=self.load_page(gravitacional_id=99)
        self.assertEquals(response.status_code, 404)

    def test_gera_etiqueta_content_without_aplicacao(self):
        '''
        If a valid gravitacional ID is passed but it contains no
        aplicacao, the page should not contains any tables or
        barcodes.
        '''
        gravitacional = cria_gravitacional()
        response = self.load_page(
            gravitacional_id = gravitacional.id
        )
        self.assertContains(response, "<a", 0)
        self.assertContains(response, "<table", 0)
        self.assertContains(response, "class='codigo-barras", 0)

    def test_gera_etiqueta_renders_view(self):
        '''
        The application should render the view correctly
        '''
        aplicacao = cria_aplicacao()
        gravitacional_id = aplicacao.gravitacional_aplicacao.id
        view = resolve(
            '/pecas/imprimir_etiquetas/{0}'.format(
                gravitacional_id
            )
        )
        self.assertEquals(view.func.view_class, EtiquetasListView)
