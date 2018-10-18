# -*- coding: utf-8 -*-
# Copyright (C) 2018 Nathanael Philipp (jnphilipp) <mail@jnphilipp.org>
#
# This file is part of infohub.
#
# infohub is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# infohub is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with infohub.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView
from infohub.decorators import piwik

from . import views


app_name = 'profiles'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='profiles:profile'),
         name='index'),
    path('profile/', views.profile, name='profile'),

    path('password/',
         piwik('Password change • Profile • infohub')(
            auth_views.PasswordChangeView.as_view(
                success_url='/profiles/password/done/')),
         name='password_change'),
    path('password/done/',
         piwik('Password change • Profile • infohub')(
            auth_views.PasswordChangeDoneView.as_view()),
         name='password_change_done'),


    path('password/reset/',
         piwik('Password reset • Profile • infohub')(
            auth_views.PasswordResetView.as_view(
                success_url='/profiles/password/reset/done/')),
         name='password_reset'),

    path('password/reset/done/',
         piwik('Password reset • Profile • infohub')(
            auth_views.PasswordResetDoneView.as_view()),
         name='password_reset_done'),

    path('password/reset/complete/',
         piwik('Password reset • Profile • infohub')(
            auth_views.PasswordResetCompleteView.as_view()),
         name='password_reset_complete'),

    path('password/reset/confirm/<uidb64>/<token>/',
         piwik('Password reset • Profile • infohub')(
            auth_views.PasswordResetConfirmView.as_view()),
         name='password_reset_confirm'),

    path('signin/', views.signin, name='signin'),
    path('signout/',
         piwik('Sign out • Profile • infohub')(
            auth_views.LogoutView.as_view(
                template_name='registration/signout.html')), name='signout'),
    # path('signup/', views.signup, name='signup'),
]
