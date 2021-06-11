from django.test import TestCase
from ..models import Abastecimento
from .cria_objetos import *
from ..forms import NovoAbastecimentoForm
from ..views import PedidosListView
from django.urls import reverse, resolve

class AbastecimentosTransporteTests(TestCase):
    def setUp(self):
        if not User.objects.exists():
            user = cria_usuario()
            self.user = self.client.force_login(
                user = user
            )
        self.response = self.load_page()
          
    def load_page(self):
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'transporte'
            }
        )
        return self.client.get(url)
        
        
    def test_abastecimento_transporte_status_code(self):
        '''
        If the correct url is given the response status code
        must be 200
        '''
        self.assertEquals(
            self.response.status_code,
            200
        )
        self.assertIsInstance(
            self.response.context['form'],
            NovoAbastecimentoForm
        )

    def test_abastecimento_transporte_render_view(self):
        '''
        Checks if the page is rendered according to the view
        '''
        view = resolve('/pecas/abastecimento/transporte/')
        self.assertEquals(view.func.view_class, PedidosListView)

    def test_abastecimento_transporte_without_itens(self):
        '''
        If no itens where found in the database it should not
        have any table and have a message 'Sem abastecimentos 
        em transporte'
        '''
        self.assertContains(
            self.response,
            'Sem abastecimentos',
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

    def test_abastecimento_transporte_with_itens(self):
        '''
        If there were itens in the database it should display
        a table with a link to remove the item
        '''
        abastecimento = cria_abastecimento(situacao='transporte')
        abastecimento.save()
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

    def test_abastecimento_transporte_with_itens_in_other_status(self):
        '''
        If there were itens in the database but with other
        status it should not display
        a table with a link to remove the item
        '''
        abastecimento = cria_abastecimento()
        response = self.load_page()
        self.assertContains(
            response,
            'Sem abastecimentos',
            1
        )
        self.assertContains(
            response,
            '<table',
            0
        )
    
    def test_abastecimento_transporte_context(self):
        '''
        If there were itens in the database it should display
        a table with a link to remove the item
        '''
        abastecimento = cria_abastecimento(situacao='transporte')
        response = self.load_page()
        self.assertQuerysetEqual(
            response.context['pedidos'],
            [abastecimento]
        )

    def test_abastecimento_transporte_links(self):
        '''
        The page must contains 3 links, one to this page, one to
        abastecimentos em transporte and one the abastecimentos 
        conlcuidos.
        '''
        response = self.load_page()
        self.assertContains(
            response,
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
            response,
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
            response,
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
        
    def test_abastecimentos_tranporte_move_pedido(self):
        '''
        For a valid item code it should change its status
        and redirect to the same page
        '''
        abastecimento = cria_abastecimento()
        codigo = abastecimento.codigo
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'transporte'
            }
        )
        response = self.client.post(
            url,
            {
                'codigo' : codigo,
                'tipo_pedido' : 'transporte'
            }
        )
        self.assertRedirects(
            response,
            url
        )
        self.assertTrue(
            Abastecimento.objects.filter(
                situacao='transporte'
            ).exists()
        )

    def test_abastecimentos_tranporte_move_pedido_wrong_status(self):
        '''
        If a valid item code is given but it is in another
        status, it should just redirect
        '''
        abastecimento = cria_abastecimento(situacao='concluido')
        codigo = abastecimento.codigo
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'transporte'
            }
        )
        response = self.client.post(
            url,
            {
                'codigo' : codigo,
                'tipo_pedido' : 'transporte'
            }
        )
        self.assertEquals(response.status_code, 404)
        self.assertFalse(
            Abastecimento.objects.filter(
                situacao = 'transporte'
            ).exists()
        )
        self.assertTrue(
            Abastecimento.objects.filter(
                situacao = 'concluido'
            ).exists()
        )

    def test_abastecimentos_tranporte_move_pedido_invalid_data(self):
        '''
        If it receives an invalid item code it should return a
        404 error
        '''
        codigo ='*10*10*1*'
        url = reverse(
            'pecas:pedidos',
            kwargs = {
                'tipo_pedido' : 'transporte'
            }
        )
        response = self.client.post(
            url,
            {
                'codigo' : codigo,
                'tipo_pedido' : 'transporte'
            }
        )
        self.assertEquals(response.status_code, 404)
