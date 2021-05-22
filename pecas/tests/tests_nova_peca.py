from django.test import TestCase
from django.urls import reverse, resolve
from ..views import index, aplicacoes, nova_peca
from ..models import Peca, Aplicacao
from gravitacionais.models import Gravitacional
from .cria_objetos import *
from ..forms import NovaPecaForm

class TestNovaPeca(TestCase):
    def load_page(self):
        url = reverse('pecas:nova_peca')
        return self.client.get(url)

    def test_nova_peca_status_code(self):
        response = self.load_page()
        self.assertEquals(response.status_code, 200)

    def test_nova_peca_resolves_view(self):
        view = resolve('/pecas/nova_peca/')
        self.assertEquals(view.func, nova_peca)        

    def test_nova_peca_contains_token(self):
        response = self.load_page()
        self.assertContains(
            response,
            'csrfmiddlewaretoken',
            1
        )

    def test_nova_peca_form(self):
        response = self.load_page()
        self.assertContains(
            response,
            '<input type="text"',
            2
        )
        self.assertContains(
            response,
            "<button type='submit'",
            1
        )

    def test_nova_peca_redirects(self):
        url = reverse('pecas:nova_peca')
        codigo_peca = '123'
        nome_peca = 'abd'
        response = self.client.post(
            url,
            {
                'codigo_peca' : codigo_peca,
                'nome_peca' : nome_peca
            })
        self.assertRedirects(
            response,
            reverse('pecas:index')
        )

    def test_nova_peca_invalid_data(self):
        url = reverse('pecas:nova_peca')
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_nova_peca_exists(self):
        url = reverse('pecas:nova_peca')
        codigo_peca = '123'
        nome_peca = 'abd'
        response = self.client.post(
            url,
            {
                'codigo_peca' : codigo_peca,
                'nome_peca' : nome_peca
            })
        self.assertTrue(Peca.objects.exists())

    def test_nova_peca_contains_link_return(self):
        response = self.load_page()
        self.assertContains(
            response,
            "<a href='{0}'".format(reverse('pecas:index')),
            1
        )

    def test_nova_peca_empty_data(self):
        url = reverse('pecas:nova_peca')
        response = self.client.post(
            url,
            {
                'codigo_peca': '',
                'nome_peca': ''
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Peca.objects.exists())
            
    def test_nova_peca_contains_form(self):
        response = self.load_page()
        form = response.context.get('form')
        self.assertIsInstance(form, NovaPecaForm)
