from django.test import TestCase
from django.urls import reverse, resolve
from ..views import index, gerir_gravitacional, novo_gravitacional
from pecas.models import Peca, Aplicacao
from ..models import Gravitacional
from .cria_objetos import *
from ..forms import NovoGravitacionalForm

class TestNovoGravitacional(TestCase):
    def load_page(self):
        url = reverse('gravitacionais:novo_gravitacional')
        return self.client.get(url)

    def test_novo_gravitacional_status_code(self):
        response = self.load_page()
        self.assertEquals(response.status_code, 200)

    def test_novo_gravitacional_resolves_view(self):
        view = resolve('/gravitacionais/novo_gravitacional')
        self.assertEquals(view.func, novo_gravitacional)        

    def test_novo_gravitacional_contains_token(self):
        response = self.load_page()
        self.assertContains(
            response,
            'csrfmiddlewaretoken',
            1
        )

    def test_novo_gravitacional_form(self):
        response = self.load_page()
        self.assertContains(
            response,
            '<input type="text"',
            5
        )
        self.assertContains(
            response,
            "<button type='submit'",
            1
        )

    def test_novo_gravitacional_redirects(self):
        url = reverse('gravitacionais:novo_gravitacional')
        codigo = '123'
        descricao = 'abc'
        posto = '1'
        linha = '2'
        galpao = '3'
        response = self.client.post(
            url,
            {
                'codigo' : codigo,
                'descricao' : descricao,
                'posto' : posto,
                'linha' : linha,
                'galpao' : galpao
            })
        self.assertRedirects(
            response,
            reverse('gravitacionais:index')
        )

    def test_novo_gravitacional_invalid_data(self):
        url = reverse('gravitacionais:novo_gravitacional')
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_nova_peca_exists(self):
        url = reverse('gravitacionais:novo_gravitacional')
        codigo = '123'
        descricao = 'abc'
        posto = '1'
        linha = '2'
        galpao = '3'
        response = self.client.post(
            url,
            {
                'codigo' : codigo,
                'descricao' : descricao,
                'posto' : posto,
                'linha' : linha,
                'galpao' : galpao
            })
        self.assertTrue(Gravitacional.objects.exists())

    def test_novo_gravitacional_contains_link_return(self):
        response = self.load_page()
        self.assertContains(
            response,
            "<a href='{0}'".format(reverse('gravitacionais:index')),
            1
        )

    def test_novo_gravitacional_empty_data(self):
        url = reverse('gravitacionais:novo_gravitacional')
        response = self.client.post(
            url,
            {
                'codigo' : '',
                'descricao' : '',
                'posto' : '',
                'linha' : '',
                'galpao' : ''
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Gravitacional.objects.exists())
            
    def test_nova_peca_contains_form(self):
        response = self.load_page()
        form = response.context.get('form')
        self.assertIsInstance(form, NovoGravitacionalForm)
