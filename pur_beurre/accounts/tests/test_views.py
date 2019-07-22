""" Test file dedicated to test views """
from django.core import mail
from django.test import TestCase
from accounts.models import Profile
from accounts import views
from django.contrib.auth.models import User
from accounts.tokens import account_activation_token
from django.contrib import messages


class RedirectTest(TestCase):
    """ Class which is used to test if pages redirections work """

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
