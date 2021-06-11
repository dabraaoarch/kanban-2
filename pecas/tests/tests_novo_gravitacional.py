from django.test import TestCase
from django.urls import reverse, resolve
from ..views import NovoGravitacionalView
from ..models import Gravitacional, Peca, Aplicacao
from .cria_objetos import *
from ..forms import NovoGravitacionalForm


class TestNovoGravitacional(TestCase):
    def setUp(self):
        if not User.objects.exists():
            user = cria_usuario()
            self.user = self.client.force_login(
                user = user
            )
        self.response = self.load_page()
        
    def load_page(self):
        '''
        Return the rendered page response
        '''
        url = reverse('pecas:novo_gravitacional')
        return self.client.get(url)

    def test_novo_gravitacional_status_code(self):
        '''
        If the right url is given, the page must return a 200
        status code
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_novo_gravitacional_resolves_view(self):
        '''
        Validates if the rendered page equals to what is describe
        in the view function
        '''
        view = resolve('/pecas/novo_gravitacional/')
        self.assertEquals(
            view.func.view_class,
            NovoGravitacionalView
        )

    def test_novo_gravitacional_contains_token(self):
        '''
        The page must contains a CSRF Token
        '''
        self.assertContains(
            self.response,
            'csrfmiddlewaretoken',
            1
        )

    def test_novo_gravitacional_form(self):
        '''
        Validates if the form is rendered as expected with 5 input
        text boxes and 1 submit button
        '''
        self.assertContains(
            self.response,
            '<input type="text"',
            5
        )
        self.assertContains(
            self.response,
            "<button type='submit'",
            1
        )

    def test_novo_gravitacional_redirects(self):
        '''
        When a valid set of data is given, the object should be added
        to the database and the user redirected to the
        gravitacionais:index view
        '''
        url = reverse('pecas:novo_gravitacional')
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
            reverse('pecas:gravitacionais')
        )

    def test_novo_gravitacional_invalid_data(self):
        '''
        If the view receives no data, the user must remain on the
        gravitacionais:novo_gravitacional view, it must not be
        redirect
        '''
        url = reverse('pecas:novo_gravitacional')
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_novo_gravitacional_exists(self):
        '''
        Checks if the gravitacional is in the database after a
        set o valid data is given to the view
        '''
        url = reverse('pecas:novo_gravitacional')
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
        '''
        The page must contain a link back to gravitacionais:index view
        '''
        self.assertContains(
            self.response,
            "<a href='{0}'".format(reverse('pecas:gravitacionais')),
            1
        )

    def test_novo_gravitacional_empty_data(self):
        '''
        If empty form is sent to the gravitacionais:novo_gravitacional
        view, the user must no be redirected and no object should
        added to the database
        '''
        url = reverse('pecas:novo_gravitacional')
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
        '''
        The form should be rendered exactly as described in the forms
        file
        '''
        form = self.response.context.get('form')
        self.assertIsInstance(form, NovoGravitacionalForm)
