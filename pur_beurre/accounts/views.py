""" Views.py dedicated for views , in 'accounts' application """
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from accounts.forms import UserRegisterForm
from pur_beurre.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.http import HttpResponse


def register(request):
    """ Method for welcome page """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, ('Please confirm your email to complete your registration'))
            user = form.save()
            user.is_active = True
            current_site = get_current_site(request)
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_subject = 'Activez votre compte Pur Beurre'
            to_email = [user.email]
            email = EmailMessage(email_subject, message, 'damiengalassooc@gmail.com', to_email)
            email.send()
            return redirect('welcome:home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/create_account.html', {'form': form})


@login_required
def my_account(request):
    """ Method for my_account page"""
    return render(request, 'accounts/my_account.html')


def activate(request, uidb64, token):
    """ Method to activate the account, with
    the link received by email"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, ('Votre compte est validé.'))
        return redirect('welcome:home')
    else:
        messages.warning(request, ("Votre lien d'activation est invalide."))
        return redirect('welcome:home')