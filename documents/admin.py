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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['hash', 'url', 'title', 'state', 'content_type',
                           'object_id']}),
        (_('Content'), {'fields': ['meta', 'text', 'related']}),
    ]
    filter_horizontal = ('related',)
    list_display = ('hash', 'url', 'title', 'state', 'updated_at')
    list_filter = ('state', 'content_type', 'object_id')
    readonly_fields = ('hash', 'state')
    search_fields = ('name',)
