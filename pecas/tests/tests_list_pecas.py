from django.test import TestCase
from django.urls import reverse, resolve
from ..views import index
from ..models import Peca, Aplicacao
from gravitacionais.models import Gravitacional
from .cria_objetos import *

class PecasTests(TestCase):
    
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
        self.assertEquals(view.func, index)

    def test_peca_list_view_with_peca(self):
        '''
        If some item is already registered, the table should
        display the four collumns related do the item
        '''
        peca = cria_pecas()
        response = self.load_page()
        self.assertContains(response, '<td', 4)
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
        
    def test_peca_contains_link_to_nova_peca(self):
        response = self.load_page()
        self.assertContains(
            response,
            "<a href='{0}'".format(reverse('pecas:nova_peca')),
            1
        )
            
        
        
