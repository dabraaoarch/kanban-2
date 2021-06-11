from django.test import TestCase
from django.urls import reverse, resolve, reverse_lazy
from ..views import  PecasListView
from ..models import Peca, Aplicacao, Gravitacional
from .cria_objetos import *

class PecasTests(TestCase):
    def setUp(self):
        if not User.objects.exists():
            user = cria_usuario()
            self.user = self.client.force_login(
                user = user
            )
    
    def load_page(self):
        '''
        Get the page to run the tests
        '''
        url = reverse('pecas:index')
        return self.client.get(url)
        
    def test_pecas_list_view_status_code(self):
        '''
        For a correct url the return status code must be 200
        '''
        response = self.load_page()
        self.assertEquals(response.status_code,200)

    def test_pecas_list_view_no_pecas_found(self):
        '''
        If no items were found in the database, the page
        must show a 'No items found' message
        '''
        response = self.load_page()
        self.assertContains(response, 'Sem peças para listagem', 1)

    def test_resolve_peca_list_view(self):
        '''
        The correct url should display the content discribed in
        the view
        '''
        view = resolve('/pecas/')
        self.assertEquals(view.func.view_class, PecasListView)

    def test_peca_list_view_with_peca(self):
        '''
        If some item is already registered, the table should
        display the five collumns related do the item
        '''
        peca = cria_pecas()
        response = self.load_page()
        self.assertContains(response, '<td', 5)
        self.assertQuerysetEqual(response.context['pecas'], [peca])
        
    def test_peca_list_view_without_peca(self):
        '''
        If there is no item in db, the table should not
        display any line
        '''
        response = self.load_page()
        self.assertContains(response, '<td', 0)
        self.assertQuerysetEqual(response.context['pecas'], [])

    def test_peca_contains_aplicacao(self):
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
            "<a href='{0}'>{1}".format(
                reverse('pecas:aplicacoes',
                        kwargs= { 'peca_id' : peca.id}
                ),
                Aplicacao.objects.filter(
                    peca_aplicacao=peca,
                    ativo=True
                ).count()                
            ),
            1
        )
        
    def test_peca_contains_links(self):
        '''
        The pecas:index must contain a link to a new peca, to
        gravitacionais:index and abastecimento:index
        '''
        response = self.load_page()
        self.assertContains(
            response,
            " href='{0}'".format(reverse('pecas:nova_peca')),
            1
        )
        self.assertContains(
            response,
            ' href="{0}"'.format(reverse('pecas:gravitacionais')),
            1
        )
        self.assertContains(
            response,
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
            
    def test_remover_peca_link(self):
        '''
        The pecas:index list must contains 
        one remove link to each peca
        '''
        peca = cria_pecas()
        response = self.load_page()
        self.assertContains(
            response,
            "<a href='{0}'".format(
                reverse(
                    'pecas:remover_peca',
                    kwargs={
                        'peca_id' : peca.id
                    }
                ),
                1
            )
        )

    def test_remover_peca_invalid_peca_id(self):
        '''
        If an invalid ID if given for the remover_peca 
        view it must return a 404 error.
        '''
        url = reverse(
            'pecas:remover_peca',
            kwargs = {
                'peca_id' : 99
            }
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_remover_peca_redirects_to_index(self):
        '''
        After removing a peca the pecas:remover_peca 
        view must redirect the user to the pecas:index
        '''
        peca = cria_pecas()
        url = reverse(
            'pecas:remover_peca',
            kwargs = {
                'peca_id' : peca.id
            }
        )
        response = self.client.get(url)
        self.assertRedirects(response,reverse('pecas:index'))

    def test_remover_peca_removed(self):
        '''
        Check if the peca is removed from the database
        '''
        peca = cria_pecas()
        url = reverse(
            'pecas:remover_peca',
            kwargs = {
                'peca_id' : peca.id
            }
        )
        response = self.client.get(url)
        self.assertFalse(Peca.objects.exists())
