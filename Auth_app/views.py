from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.http import HttpResponse

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Forms And models
from Auth_app.models import User, Profile
from Auth_app.forms import Prifle_Form, SignUpForm

from django.contrib import messages

# Create your views here.


def Sing_up(request):
    form = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created!')
            return HttpResponseRedirect(reverse('Auth_App:login'))
    context = {
        'form' : form,
    }
    return render(request, 'Auth_app/sign_up.html', context)

def Login_user(request):
    form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Shop_App:home'))
    context = {
        'form':form
    }
    return render(request, 'Auth_app/login.html', context)

@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, 'You are loged out!')
    return HttpResponseRedirect(reverse('Shop_App:home'))


@login_required
def User_profile(request):
    profile = Profile.objects.get(user=request.user)

    form = Prifle_Form(instance=profile)
    if request.method == 'POST':
        form = Prifle_Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account sucessfully Updated')
            form = Prifle_Form(instance=profile)

    return render(request, 'Auth_app/change_profile.html', context={'form':form})