from datetime import timedelta, datetime

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from message.crypto import MessagingRSA
from rest_framework.authtoken.models import Token
from sign.utils import token_expire_handler
from subsections.views import get_bitcoin_address
from sudo.models import CloseRegistration
from users.models import BlacklistUser
from users.models import Profile
from users.models import User

from .forms import UserRegistrationForm, UserLoginForm, StepsForm


@require_http_methods(["GET", "POST"])
def signup(request):
    if (request.user.is_authenticated):
        return redirect(reverse('subsections:home'))
    error = ''
    success = ''
    flag = "false"
    hcaptcha_sitekey = settings.YOUR_HCAPTCHA_SITE_KEY
    if request.method == 'POST':
        your_captcha_response = request.POST.get('h-captcha-response')
        user_form = UserRegistrationForm(request.POST)

        hcapcha_validation = {
            'secret': settings.YOUR_HCAPTCHA_SECRET_KEY,
            'response': your_captcha_response
        }
        r = requests.post(settings.VERIFY_URL, data=hcapcha_validation)
        hcapcha_result = r.json()

        if hcapcha_result['success']:
            if user_form.is_valid():
                cd = user_form.cleaned_data
                new_user = user_form.save(commit=False)
                new_user.username = cd['user_hash']
                new_user.set_password(cd['password'])
                new_user.first_login = True
                new_user.is_active = True
                if cd['disposable']:
                    new_user.disposable = True
                    new_user.auto_account_delete_time = 0
                new_user.save()
                Profile.objects.create(user=new_user)
                return redirect(reverse('login'), {'new_user': new_user})
            else:
                flag = "true"
    else:
        user_form = UserRegistrationForm()

    sayches_customization = CloseRegistration.objects.filter(close_registration=True).first()
    return render(request, 'account/signup.html', {'user_form': user_form,
                                                   'hcaptcha_sitekey': hcaptcha_sitekey,
                                                   'flag': flag,
                                                   'sayches_customization': sayches_customization,
                                                   'messages': {'error': error, 'sucesss': success}})


@require_http_methods(["GET", "POST"])
def user_login(request):
    remember_me_data = {
        "password": request.COOKIES.get('password'),
        "username": request.COOKIES.get('username')
    }
    if (request.user.is_authenticated):
        return redirect(reverse('subsections:home'))
    error = ''
    flag = "false"
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data

            user = authenticate(request, username=cd['login'], password=cd['password'])
            if user is None:
                user = authenticate(request, username=cd['login'], password=cd['password'])

            if user:
                if user.is_active:
                    check_black_list = BlacklistUser.objects.filter(user=user, on_login=True).first()
                    if not check_black_list:
                        login(request, user)
                        token, created = Token.objects.get_or_create(user=user)
                        token_expire_handler(request)
                        request.session['encryption_token'] = cd['password']
                        request.session.modified = True
                        MessagingRSA.create_rsa(request)
                        response = redirect(reverse('subsections:home'))
                        if user.first_login:
                            response = redirect(reverse('steps_form'))

                        if cd['remember_me']:
                            response.set_cookie('password', cd['password'])
                            response.set_cookie('username', cd['login'])

                        if user.first_login:
                            return response
                        return response
                    else:
                        error = 'Your account has beed suspended'
                        flag = "true"
                else:
                    error = 'Disabled account'
            else:
                error = 'Username or password does not match'
                flag = "true"
        else:
            error = 'Fill the username and password'
    else:
        login_form = UserLoginForm()
    return render(request, 'account/login.html',
                  {'form': login_form, 'error': error, "flag": flag, "remember_me_data": remember_me_data})

@login_required
@require_http_methods(["GET", "POST"])
def steps_form(request):
    user = request.user
    if not (user.first_login):
        return redirect(reverse('subsections:home'))
    profile = user.profile
    initial_dic = {}
    errors = ''

    if user.name:
        initial_dic['name'] = user.name

    if profile.website:
        initial_dic['website'] = profile.website
    if user.country:
        initial_dic['country'] = user.country.name

    if request.method == 'POST':
        steps_form = StepsForm(data=request.POST, files=request.FILES)

        if steps_form.is_valid():
            cd = steps_form.cleaned_data

            user.alias = cd['alias']
            user.country = request.POST.get('location')
            user.first_login = False
            user.save()

            if cd['image']:
                profile = Profile.objects.get(user=user)
                profile.photo = cd['image']
            profile.save()
            return redirect(reverse('subsections:home'))


        else:
            for error in steps_form.errors:
                errors += error

    else:
        steps_form = StepsForm(initial=initial_dic)

    context = {'steps_form': steps_form, 'bitcoin_address': get_bitcoin_address, "errors": errors}
    return render(request, 'account/steps_form/steps_form.html', context)


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('subsections:home')
    return render(request, 'account/logout.html')
