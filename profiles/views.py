# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from infohub.decorators import piwik

from .forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .models import Profile


@csrf_protect
@piwik('Sign in • Profile • infohub')
def signin(request):
    gnext = request.GET.get('next')

    if request.user.is_authenticated:
        return redirect(gnext) if gnext else redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS,
                                         _('You have successfully signed in.'))

                    return redirect(gnext) if gnext else redirect('dashboard')
                else:
                    messages.add_message(request, messages.ERROR,
                                         _('Your account is disabled.'))
                return redirect(request.META.get('HTTP_REFERER'))
        messages.add_message(request, messages.ERROR,
                             _('Please enter a correct email and password to' +
                               ' sign in. Note that both fields may be ' +
                               'case-sensitive.'))
    else:
        form = AuthenticationForm(request)
    return render(request, 'registration/signin.html', locals())


@csrf_protect
@piwik('Sign up • Profile • infohub')
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(user=new_user)
            messages.info(request, messages.SUCCESS,
                          _('Thanks for signing up. You are now logged in.'))
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('profiles:profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', locals())


@csrf_protect
@login_required
@piwik('Profile • StockAnalyzer')
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = UserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,
                             _('Your profile has been successfully updated.'))
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'profiles/profile_detail.html', locals())
