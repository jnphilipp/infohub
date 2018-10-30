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

from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic
from infohub.decorators import piwik

from ..models import Feed


@method_decorator(piwik('Feeds • Feeds • infohub'), name='dispatch')
class ListView(generic.ListView):
    context_object_name = 'feeds'
    model = Feed
    paginate_by = 100

    def get_ordering(self):
        self.order = self.request.GET.get('o', 'url')
        return self.order

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['o'] = self.order
        return context


@method_decorator(piwik('Feed • Feeds • infohub'), name='dispatch')
class DetailView(generic.DetailView):
    model = Feed

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['do'] = self.request.GET.get('do', '-updated_at')
        context['documents'] = context['feed'].documents. \
            order_by(context['do'])
        return context


@piwik('Document • Feed • Feeds • infohub')
def document(request, slug, hash):
    feed = get_object_or_404(Feed, slug=slug)
    document = get_object_or_404(feed.documents, hash=hash)
    meta_formatted = json.dumps(document.meta, indent=4)
    return render(request, 'feeds/feed_document_detail.html', locals())
