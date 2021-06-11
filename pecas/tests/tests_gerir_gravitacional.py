from django.test import TestCase
from django.urls import reverse, resolve
from ..views import GerirGravitacionalView
from .cria_objetos import *

class GerirGravitacionalTests(TestCase):
    def setUp(self):
        if not User.objects.exists():
            user = cria_usuario()
            self.user = self.client.force_login(
                user = user
            )

    def load_page(self, gravitacional_id):
        '''
        Return the rendered page content
        '''
        url = reverse(
            'pecas:gerir_gravitacional',
            kwargs = {
                'gravitacional_id' : gravitacional_id
            }
        )
        return self.client.get(url)

    def test_gerir_gravitacional_return_status_code(self):
        '''
        The page must return a 200 for a valid link and a valid
        gravitacional_id
        '''
        gravitacional = cria_gravitacional()
        result = self.load_page(gravitacional_id=gravitacional.id)
        self.assertEquals(result.status_code, 200)

    def test_gerir_gravitacional_rendered_view(self):
        '''
        The rendered result must be equal to the view function result
        '''
        gravitacional = cria_gravitacional()
        view = resolve(
            '/pecas/gerir_gravitacional/{0}'.format(
                gravitacional.id
            )
        )
        self.assertEquals(
            view.func.view_class,
            GerirGravitacionalView
        )

    def test_gerir_gravitacional_contains_link_to_index(self):
        '''
        The page must have one link back to the gravitacionais:index 
        view
        '''
        gravitacional = cria_gravitacional()
        response = self.load_page(gravitacional_id=gravitacional.id)
        self.assertContains(
            response,
            "<a href='{0}'".format(reverse('pecas:gravitacionais')),
            1
        )

    def test_gerir_gravitacional_invalid_id(self):
        '''
        Any invalid gravitacional_id must return a 404 error
        '''
        response = self.load_page(gravitacional_id=99)
        self.assertEquals(response.status_code, 404)

    def test_gerir_gravitacional_without_aplicacao(self):
        '''
        Validates how the page is rendered for a gravitacional withou
        aplicacao
        '''
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
        '''
        Validates if the page is correctly rendered for a
        gravitacional with aplicacao
        '''
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
                    "pecas:remover_aplicacao",
                    kwargs = {
                        'aplicacao_id': aplicacao.id
                    }
                )
            )
        )

        
