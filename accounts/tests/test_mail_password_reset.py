from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class PasswordResetMailTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username = 'john',
            email = 'john@doe.com',
            password = '123456'
        )
        self.response = self.client.post(
            reverse('password_reset'),
            {
                'email': 'john@doe.com'
            }
        )
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual(
            '[Kanban] Redefinir senha',
            self.email.subject
        )

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse(
            'password_reset_confirm',
            kwargs={
                'token' : token,
                'uidb64' : uid
            }
        )
        self.assertIn(
            password_reset_token_url,
            self.email.body
        )
        self.assertIn(
            'john',
            self.email.body
        )
        self.assertIn(
            'john@doe.com',
            self.email.to
        )
