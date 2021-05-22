from django.test import TestCase
from django.urls import reverse, resolve
from ..views import index
from pecas.models import Peca, Aplicacao
from ..models import Gravitacional
from .cria_objetos import *

class GravitacionaisTests(TestCase):
    
    def load_page(self):
        '''
        Get the page to run the tests
        '''
        url = reverse('gravitacionais:index')
        return self.client.get(url)
        
    def test_gravitacionais_list_view_status_code(self):
        '''
        For a correct url the return status code must be 200
        '''
        response = self.load_page()
        self.assertEquals(response.status_code,200)

    def test_gravitacionais_list_view_no_gravitacional_found(self):
        '''
        If no gravitacionais were found in the database, the page
        must show a 'No gravitacionais found' message
        '''
        response = self.load_page()
        self.assertContains(
            response,
            'Sem gravitacionais para listagem',
            1
        )

    def test_resolve_gravitacional_list_view(self):
        '''
        The correct url should display the content discribed in
        the view
        '''
        view = resolve('/gravitacionais/')
        self.assertEquals(view.func, index)

    def test_gravitacionais_list_view_with_gravitacional(self):
        '''
        If some gravitacional is already registered, the table should
        display the four collumns related do the gravitacional
        '''
        gravitacional = cria_gravitacional()
        response = self.load_page()
        self.assertContains(response, '<td', 7)
        self.assertQuerysetEqual(
            response.context['gravitacionais'],
            [gravitacional]
        )
        
    def test_gravitacional_list_view_without_gravitacional(self):
        '''
        If there is no gravitacional in db, the table should not
        display any line
        '''
        response = self.load_page()
        self.assertContains(response, '<td', 0)
        self.assertQuerysetEqual(
            response.context['gravitacionais'],
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
            "<a href='{0}'>{1}".format(
                reverse('gravitacionais:gerir_gravitacional',
                        kwargs= {
                            'gravitacional_id' : gravitacional.id
                        }
                        ),
                Aplicacao.objects.filter(
                    gravitacional_aplicacao=gravitacional.id,
                    ativo=True
                ).count()
            ),
            1
        )
        
    def test_gravitacional_contains_link_to_novo_gravitacional(self):
        response = self.load_page()
        self.assertContains(
            response,
            "<a href='{0}'".format(
                reverse('gravitacionais:novo_gravitacional')
            ),
            1
        )
            
        
        
