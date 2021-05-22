from django.test import TestCase
from django.urls import reverse, resolve
from ..views import gerir_gravitacional
from .cria_objetos import *

class GerirGravitacionalTests(TestCase):
    def load_page(self, gravitacional_id):
        url = reverse(
            'gravitacionais:gerir_gravitacional',
            kwargs = {
                'gravitacional_id' : gravitacional_id
            }
        )
        return self.client.get(url)

    def test_gerir_gravitacional_return_status_code(self):
        gravitacional = cria_gravitacional()
        result = self.load_page(gravitacional_id=gravitacional.id)
        self.assertEquals(result.status_code, 200)

    def test_gerir_gravitacional_rendered_view(self):
        gravitacional = cria_gravitacional()
        view = resolve(
            '/gravitacionais/gerir_gravitacional/{0}'.format(
                gravitacional.id
            )
        )
        self.assertEquals(view.func, gerir_gravitacional)

    def test_gerir_gravitacional_contains_link_to_index(self):
        gravitacional = cria_gravitacional()
        response = self.load_page(gravitacional_id=gravitacional.id)
        self.assertContains(
            response,
            "<a href='{0}'".format(reverse('gravitacionais:index')),
            1
        )

    def test_gerir_gravitacional_invalid_id(self):
        response = self.load_page(gravitacional_id=99)
        self.assertEquals(response.status_code, 404)

    def test_gerir_gravitacional_without_aplicacao(self):
        gravitacional = cria_gravitacional()
        response = self.load_page(gravitacional_id=gravitacional.id)
        self.assertContains(response, "<table", 0)
        self.assertContains(response, "<input", 8)
        self.assertContains(response, "<button type='submit'", 1)
        self.assertContains(
            response,
            "Nenhum item cadastrado ainda!",
            1
        )
        
    def test_gerir_gravitacional_with_aplicacao(self):
        gravitacional = cria_gravitacional()
        aplicacao = cria_aplicacao(gravitacional=gravitacional)
        response = self.load_page(gravitacional_id=gravitacional.id)
        self.assertContains(response, "<table", 1)
        self.assertContains(response, "<th>", 5)
        self.assertContains(response, "<input", 8)
        self.assertContains(response, "<button type='submit'", 1)
        self.assertContains(
            response,
            "<a href='{0}'".format(
                reverse(
                    "gravitacionais:remover_aplicacao",
                    kwargs = {
                        'aplicacao_id': aplicacao.id
                    }
                )
            )
        )

        
