""" Test file dedicated to test views """
from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from unittest.mock import patch
from accounts.models import Profile
from accounts import views
from accounts.tokens import account_activation_token

from accounts.tokens import account_activation_token



class RedirectTest(TestCase):
    """ Class which is used to test if pages redirections work """
    def setUp(self):
        self.client = Client()

    def test_redirect_if__try_access_myaccount_without_login(self):
        """ test redirection if user try to access the
        'my_account' page without login """
        response = self.client.get('/myaccount/')
        self.assertEqual(response.status_code, 302)

    def test_redirect_when_account_created_to_homepage(self):
        """ test redirection when the user create his account """
        response = self.client.post('/register/', {'username': 'seiph',
                                                   'first_name': 'Jean',
                                                   'last_name': 'Robert',
                                                   'email': 'jbr@aol.com',
                                                   'password1': 'kevin1234',
                                                   'password2': 'kevin1234'})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('welcome/index.html')

    def test_redirect_when_login_to_homepage(self):
        """ test that the use is redirected when he logs in """
        User.objects.create_user(username="test",
                                 first_name="Al",
                                 last_name="taga",
                                 email="albg@sfr.fr",
                                 password="kevin1234")
        response = self.client.post('/login/', {'username': 'test',
                                                'password': 'kevin1234'})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('welcome/index.html')

class EmailTest(TestCase):
    """Test to check if the email is sent
    when the user Sign up"""

    def setUp(self):
        self.client.post('/register/', {'username': 'seiph',
                                        'first_name': 'Jean',
                                        'last_name': 'Robert',
                                        'email': 'jbr@aol.com',
                                        'password1': 'kevin1234',
                                        'password2': 'kevin1234'})

    def test_if_confirmation_email_is_sent(self):
        """ Test if the email is sent and if
        the subject is the good one"""
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activez votre compte Pur Beurre')

    def test_if_the_email_is_sent_to_the_new_account(self):
        """ Test if the email is sent to the right
        destination """
        self.assertEqual(mail.outbox[0].to, ['jbr@aol.com'])

class AccountTest(TestCase):
    """ Class for test the email is well confirmed when
    we click on the confirmation link """
    def setUp(self):
        self.client = Client()

    def test_if_the_user_confirm_his_account_is_false(self):
        """ Test if the confirmation email needs to be unique
        to be confirmed """
        self.client.post('/register/', {'username': 'seiph',
                                        'first_name': 'Jean',
                                        'last_name': 'Robert',
                                        'email': 'jbr@aol.com',
                                        'password1': 'kevin1234',
                                        'password2': 'kevin1234'})

        user = User.objects.first()
        user_id = user.id

        self.client.get('/activate/', {'uidb64': user_id,
                                    'token': 'abcdef'})
        profile = Profile.objects.get(user=user_id)
        self.assertEqual(profile.email_confirmed, False)

    def test_if_the_user_confirm_his_account_(self):
        """ Test if after the user clicked on the right
        link, his account is well confirmed"""
        class WrapperMakeToken():
            """Class which allow us to isolate the token
            for the test """
            token = ''
            original_make_token = account_activation_token.make_token

            def make_token(self, user):
                """ Class method which allow us to isolate
                the token generation to re-use on the activation page"""
                self.token = self.original_make_token(user)
                return self.token

        wrap_make_token = WrapperMakeToken()
        with patch( 'accounts.tokens.AccountActivationTokenGenerator.make_token', wraps=wrap_make_token.make_token):
            self.client.post('/register/', {'username': 'seiph',
                                    'first_name': 'Jean',
                                    'last_name': 'Robert',
                                    'email': 'jbra@aol.com',
                                    'password1': 'kevin1234',
                                    'password2': 'kevin1234'})

            user = User.objects.last()
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))

            self.client.get('/activate/' + uidb64 +'/' + wrap_make_token.token + '/')
            profile = Profile.objects.get(user=user.id)
            self.assertEqual(profile.email_confirmed, True)
