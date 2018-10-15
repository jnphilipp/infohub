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

from .models import Parser


@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['slug', 'name']}),
    ]
    list_display = ('name', 'updated_at')
    readonly_fields = ('slug',)
    search_fields = ('name',)
    ordering = ('name',)
