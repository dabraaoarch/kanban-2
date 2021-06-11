from django.test import TestCase
from ..models import Abastecimento
from .cria_objetos import *
from django.urls import reverse, resolve
from ..forms import NovoAbastecimentoForm
from ..views import PedidosListView
from django.test.client import Client

class AbastecimentosPendentesTests(TestCase):
    def setUp(self):
        if not User.objects.exists():
            user = cria_usuario()
            self.user = self.client.force_login(
                user = user
            )

        self.response =  self.load_page()
        
    def load_page(self):
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'pendentes'
            }
        )
        return self.client.get(url)
    
    def test_abastecimento_pendente_status_code(self):
        '''
        If the correct url is given the response status code
        must be 200
        '''
        self.assertEquals(
            self.response.status_code,
            200
        )

    def test_abastecimento_pendente_render_view(self):
        '''
        Checks if the page is rendered according to the view
        '''
        view = resolve(
            reverse(
                'pecas:pedidos',
                kwargs = {
                    'tipo_pedido' : 'pendentes'
                }
            )
        )
            
        self.assertEquals(view.func.view_class, PedidosListView)
        
    def test_abastecimento_pendente_form_context(self):
        '''
        Checks if the page receives the form
        '''
        self.assertEquals(
            self.response.status_code,
            200
        )
        self.assertIsInstance(
            self.response.context['form'],
            NovoAbastecimentoForm
        )

    def test_abastecimento_pendentes_without_itens(self):
        '''
        If no itens where found in the database it should not
        have any table and have a message 'Sem abastecimentos 
        pendentes'
        '''
        self.assertContains(
            self.response,
            'Sem abastecimentos pendentes!',
            1
        )
        self.assertContains(
            self.response,
            '<table',
            0
        )
        self.assertContains(
            self.response,
            '<input type="text"',
            1
        )
        self.assertContains(
            self.response,
            '<input type="hidden"',
            1
        )

    def test_abastecimento_pendentes_with_itens(self):
        '''
        If there were itens in the database it should display
        a table with a link to remove the item
        '''
        abastecimento = cria_abastecimento()
        response = self.load_page()
        self.assertContains(
            response,
            '<table',
            1
        )
        self.assertContains(
            response,
            '<td',
            6
        )
        self.assertContains(
            response,
            'codigo-barras',
            1
        )

    def test_abastecimento_pendentes_with_itens_in_other_status(self):
        '''
        If there were itens in the database but with other
        status it should not display
        a table with a link to remove the item
        '''
        abastecimento = cria_abastecimento(situacao='transporte')
        response = self.load_page()
        self.assertContains(
            response,
            'Sem abastecimentos pendentes!',
            1
        )
        self.assertContains(
            response,
            '<table',
            0
        )
    
    def test_abastecimento_pendentes_context(self):
        '''
        If there were itens in the database it should display
        a table with a link to remove the item
        '''
        abastecimento = cria_abastecimento()
        response = self.load_page()
        self.assertQuerysetEqual(
            response.context['pedidos'],
            [abastecimento]
        )

    def test_abastecimento_pendentes_links(self):
        '''
        The page must contains 3 links, one to this page, one to
        abastecimentos em transporte and one the abastecimentos 
        conlcuidos.
        '''
        self.assertContains(
            self.response,
            "<a href='{0}'".format(
                reverse(
                    'pecas:pedidos',
                    kwargs = {
                        'tipo_pedido' : 'pendentes'
                    }
                )
            ),
            1
        )
        self.assertContains(
            self.response,
            "<a href='{0}'".format(
                reverse(
                    'pecas:pedidos',
                    kwargs = {
                        'tipo_pedido' : 'concluidos'
                    }
                )
            ),
            1
        )
        self.assertContains(
            self.response,
            "<a href='{0}'".format(
                reverse(
                    'pecas:pedidos',
                    kwargs = {
                        'tipo_pedido' : 'transporte'
                    }
                )
            ),
            1
        )
        
    def test_abastecimentos_pendentes_novo_pedido_empty_data(self):
        '''
        If empty data is sent to the server it will ignore that
        and list the open requisitions
        '''
        codigo = ''
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'pendentes'
            }
        )
        response = self.client.post(
            url,
            {
                'codigo' : codigo
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Abastecimento.objects.exists())
        
    def test_abastecimentos_pendentes_novo_pedido_invalid_data(self):
        '''
        If invalid data is sent to the server it will ignore the data
        and list the open requisitions
        '''
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'pendentes'
            }
        )
        response = self.client.post(url,{})
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Abastecimento.objects.exists())


    def test_abastecimentos_pendentes_novo_pedido_invalid_subdata(self):
        '''
        If a valid data is sent, but the aplicacao and gravitacional
        are not found in the database the it must return a 404
        '''
        codigo = '*GV-101*1001*1*'
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'pendentes'
            }
            
        )
        response = self.client.post(
            url,
            {
                'codigo' : codigo,
                'tipo_pedido' : 'pendentes'
            }
        )
        self.assertEquals(response.status_code, 404)
        self.assertFalse(Abastecimento.objects.exists())

    def test_abastecimentos_pendentes_novo_pedido_valid_data(self):
        '''
        If a valid data is sent the item should be added to the
        database and be listed in the page
        '''
        aplicacao = cria_aplicacao()
        codigo = "*" + \
            aplicacao.gravitacional_aplicacao.codigo + "*" + \
            aplicacao.peca_aplicacao.codigo_peca + "*" + \
            str(aplicacao.id) + "*"
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'pendentes'
            }
        )
        response = self.client.post(
            url,
            {
                'codigo' : codigo,
                'tipo_pedido' : 'pendentes'
            }
        )
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Abastecimento.objects.exists())

