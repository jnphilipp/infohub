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

from django.urls import path

from .views import feed


app_name = 'feeds'
urlpatterns = [
    path('feed/', feed.ListView.as_view(), name='feed_list'),
    path('feed/<slug:slug>/', feed.DetailView.as_view(), name='feed_detail'),
    path('feed/<slug:slug>/<slug:hash>', feed.document,
         name='feed_document_detail'),
]
