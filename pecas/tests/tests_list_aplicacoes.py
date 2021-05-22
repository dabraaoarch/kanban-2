from django.test import TestCase
from django.urls import reverse, resolve
from ..views import index, aplicacoes
from ..models import Peca, Aplicacao
from gravitacionais.models import Gravitacional
from .cria_objetos import *

class AplicacaoTests(TestCase):
    def load_page(self, peca_id):
        '''
        Get the page to run the tests
        '''
        url = reverse(
            'pecas:aplicacoes',
            kwargs = {
                'peca_id' : peca_id
            }
        )

        return self.client.get(url)

    def test_aplicacoes_list_view_status_code(self):
        '''
        For a correct url the return status code must be 200
        '''
        peca = cria_pecas()
        aplicacao = cria_aplicacao(peca)
        response = self.load_page(peca_id=peca.id)
        self.assertEquals(response.status_code, 200)

    def test_aplicacoes_list_view_resolves_view(self):
        aplicacao = cria_aplicacao()
        view = resolve('/pecas/{0}/'.format(
            aplicacao.peca_aplicacao.id
        ))
        self.assertEquals(view.func, aplicacoes)

    def test_aplicacoes_list_page_not_found(self):
        '''
        If peca_id is not a valid item, the sistem must
        return a 404 response
        '''
        response = self.load_page(peca_id=99)
        self.assertEquals(response.status_code, 404)

    def test_aplicacoes_list_got_link_pecas_list_view(self):
        '''
        Test if the page has a link to the item list view
        '''
        peca = cria_pecas()
        aplicacao = cria_aplicacao(peca=peca)
        response = self.load_page(peca_id=peca.id)
        self.assertContains(
            response,
            "<a href='{0}'".format(reverse('pecas:index')),
            1
        )

    def test_aplicacoes_list_context(self):
        '''
        Test if the aplicacoes list receives the correct context
        '''
        peca_aplicacao = cria_pecas()
        aplicacao = cria_aplicacao(peca=peca_aplicacao)
        response = self.load_page(peca_id=peca_aplicacao.id)
        self.assertQuerysetEqual(
            response.context['aplicacoes'],
            [aplicacao]
        )


    def test_aplicacoes_list_view_without_aplicacao_redirects(self):
        '''
        If the item has no aplication added yet, it should
        redirect back to the pecas list view page
        '''
        peca = cria_pecas()
        response = self.load_page(peca_id=peca.id)
        self.assertRedirects(response, reverse('pecas:index'))
            
    
        

