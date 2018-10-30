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

import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from infohub.decorators import piwik

from ..models import Document


@method_decorator(login_required, name='dispatch')
@method_decorator(piwik('Documents • Documents • infohub'), name='dispatch')
class ListView(generic.ListView):
    context_object_name = 'documents'
    model = Document
    paginate_by = 1000

    def get_ordering(self):
        self.order = self.request.GET.get('o', '-updated_at')
        return self.order

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['o'] = self.order
        return context


@method_decorator(piwik('Document • Documents • infohub'), name='dispatch')
class DetailView(generic.DetailView):
    model = Document
    slug_field = 'hash'
    slug_url_kwarg = 'hash'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['meta_formatted'] = json.dumps(context['document'].meta,
                                               indent=4)
        return context
