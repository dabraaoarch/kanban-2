from django.test import TestCase
from django.urls import reverse, resolve
from ..views import GravitacionalListView
from ..models import Gravitacional, Peca, Aplicacao
from .cria_objetos import *

class GravitacionaisTests(TestCase):
    
    def setUp(self):
        '''
        Get the page to run the tests
        '''
        if not User.objects.exists():
            user = cria_usuario()
            self.user = self.client.force_login(
                user = user
            )
        self.response = self.load_page()

    def load_page(self):
        url = reverse('pecas:gravitacionais')
        return self.client.get(url)
        
    def test_gravitacionais_list_view_status_code(self):
        '''
        For a correct url the return status code must be 200
        '''
        self.assertEquals(
            self.response.status_code,
            200
        )

    def test_gravitacionais_list_view_no_gravitacional_found(self):
        '''
        If no gravitacionais were found in the database, the page
        must show a 'No gravitacionais found' message
        '''
        self.assertContains(
            self.response,
            'Sem gravitacionais para listagem',
            1
        )

    def test_resolve_gravitacional_list_view(self):
        '''
        The correct url should display the content discribed in
        the view
        '''
        view = resolve('/pecas/gravitacionais/')
        self.assertEquals(
            view.func.view_class,
            GravitacionalListView
        )

    def test_gravitacionais_list_view_with_gravitacional(self):
        '''
        If some gravitacional is already registered, the table should
        display the four collumns related do the gravitacional
        '''
        gravitacional = cria_gravitacional()
        response = self.load_page()
        self.assertContains(
            response,
            '<td',
            8
        )
        self.assertQuerysetEqual(
            response.context['gravitacionais'],
            [gravitacional]
        )
        
    def test_gravitacional_list_view_without_gravitacional(self):
        '''
        If there is no gravitacional in db, the table should not
        display any line
        '''
        self.assertContains(
            self.response,
            '<td',
            0
        )
        self.assertQuerysetEqual(
            self.response.context['gravitacionais'],
            []
        )

    def test_gravitacional_contains_items(self):
        '''
        If there are aplications for the item, it should be
        counted and displayed correctly on the table
        with a link to the specific applications
        '''
        peca = cria_pecas()
        gravitacional = cria_gravitacional()
        aplicacao = cria_aplicacao(
            peca=peca,
            gravitacional=gravitacional
        )
        response = self.load_page()
        self.assertContains(
            response,
            " href='{0}'>".format(
                reverse('pecas:gerir_gravitacional',
                        kwargs= {
                            'gravitacional_id' : gravitacional.id
                        }
                        )
                ),
            1
        )
        
    def test_gravitacional_contains_links(self):
        '''
        The page must contain a link to add a new gravitacional
        a link back to pecas and a link to abastecimento
        '''
        self.assertContains(
            self.response,
            "<a href='{0}'".format(
                reverse('pecas:novo_gravitacional')
            ),
            1
        )
        self.assertContains(
            self.response,
            ' href="{0}"'.format(
                reverse('pecas:index')
            ),
            1
        )
        self.assertContains(
            self.response,
            ' href="{0}"'.format(
                reverse(
                    'pecas:pedidos',
                    kwargs = {
                        'tipo_pedido' : 'pendentes'
                    }
                )
            ),
            1
        )

    def test_gravitacional_contain_link_to_remove_gravitacional(self):
        '''
        For each gravitacional must be a link to 
        gravitacionais:remover_gravitacional view
        '''
        gravitacional = cria_gravitacional()
        response = self.load_page()
        self.assertContains(
            response,
            " href='{0}'".format(
                reverse(
                    'pecas:remover_gravitacional',
                    kwargs={
                        'gravitacional_id' : gravitacional.id
                    }
                )
            ),
            1
        )
                
    def test_remover_gravitacional_redirects_index(self):
        '''
        If a valid gravitacional_id is given, the
        gravitacionais:remover_gravitacional view should return the
        user to the gravitacionais:index view and the object should
        not be found on the data_base
        '''
        gravitacional = cria_gravitacional()
        url = reverse(
            'pecas:remover_gravitacional',
            kwargs = {
                'gravitacional_id' : gravitacional.id
            }
        )
        response = self.client.get(url)
        self.assertRedirects(response, reverse('pecas:gravitacionais'))

def test_remover_gravitacional_removed(self):
        '''
        If a valid gravitacional_id is given, the
        gravitacionais:remover_gravitacional, the gravitacional
        must be remover from the database and also the aplicacao
        '''
        gravitacional = cria_gravitacional()
        aplicacao = cria_aplicacao(gravitacional=gravitacional)
        url = reverse(
            'pecas:remover_gravitacional',
            kwargs = {
                'gravitacional_id' : gravitacional.id
            }
        )
        response = self.client.get(url)
        self.assertFalse(Gravitacional.objects.exist())
        self.assertFalse(Aplicacao.objects.exist())

