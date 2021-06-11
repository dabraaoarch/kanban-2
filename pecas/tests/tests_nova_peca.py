from django.test import TestCase
from django.urls import reverse, resolve
from ..views import NovaPecaView
from ..models import Peca, Aplicacao, Gravitacional
from .cria_objetos import *
from ..forms import NovaPecaForm


class TestNovaPeca(TestCase):
    def setUp(self):
        '''
        Return the rendered page
        '''
        if not User.objects.exists():
            user = cria_usuario()
            self.user = self.client.force_login(
                user = user
            )
        url = reverse('pecas:nova_peca')
        self.response = self.client.get(url)

    def test_nova_peca_status_code(self):
        '''
        If a valid url is given, the status code must be 200
        '''
        self.assertEquals(
            self.response.status_code,
            200
        )

    def test_nova_peca_resolves_view(self):
        '''
        The page must be rendered as describe in the pecas:nova_peca
        view
        '''
        view = resolve('/pecas/nova_peca/')
        self.assertEquals(view.func.view_class, NovaPecaView)        

    def test_nova_peca_contains_token(self):
        '''
        The page must contains a CSRF tolken
        '''
        self.assertContains(
            self.response,
            'csrfmiddlewaretoken',
            1
        )

    def test_nova_peca_form(self):
        '''
        Checks if the page is correctly rendered, with 2 text inputs
        and one submit button
        '''
        self.assertContains(
            self.response,
            '<input type="text"',
            2
        )
        self.assertContains(
            self.response,
            "<button type='submit'",
            1
        )

    def test_nova_peca_redirects(self):
        '''
        When valid data is sent to the view, a new object
        should be created in the database and the user
        must be redirected
        '''
        url = reverse('pecas:nova_peca')
        codigo_peca = '123'
        nome_peca = 'abd'
        response = self.client.post(
            url,
            {
                'codigo_peca' : codigo_peca,
                'nome_peca' : nome_peca
            })
        
        self.assertTrue(
            Peca.objects.exists()
        )

    def test_nova_peca_invalid_data(self):
        '''
        When no data is sent to the view, the user must remain
        in the same pecas:nova_peca view, and no objects
        should be added to the database
        '''
        url = reverse('pecas:nova_peca')
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
        self.assertFalse(Peca.objects.exists())

    def test_nova_peca_exists(self):
        '''
        After a valid set of data is sent to the view, the
        peca should be added to the database
        '''
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
        '''
        The page must contain a link back to the pecas:index view
        '''
        self.assertContains(
            self.response,
            "<a href='{0}'".format(reverse('pecas:index')),
            1
        )

    def test_nova_peca_empty_data(self):
        '''
        When a set of empty data is sent to the view, the user
        should remain in the pecas:nova_peca view and no data
        should be added to the database
        '''
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
        '''
        Checks if the form is rendered as described in the forms.py
        file
        '''
        form = self.response.context.get('form')
        self.assertIsInstance(form, NovaPecaForm)
