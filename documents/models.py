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

import re
import requests

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, RETURN_VALUE, transition
from hashlib import sha512
from infohub.fields import SingleLineTextField


class Document(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    hash = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name=_('Hash')
    )
    url = models.URLField(
        max_length=2096,
        verbose_name=_('URL')
    )
    title = SingleLineTextField(
        null=True,
        blank=True,
        verbose_name=_('Title')
    )
    meta = JSONField(
        default=dict,
        verbose_name=_('Metadata')
    )
    text = models.TextField(
        verbose_name=_('Text')
    )
    state = FSMField(
        default='new',
        protected=True,
        verbose_name=_('State')
    )
    related = models.ManyToManyField(
        'self',
        verbose_name=_('Related documents')
    )
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('Content type')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('Object ID')
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_absolute_url(self):
        return reverse('documents:document_detail', args=[self.hash])

    def has_no_title(self):
        return self.title is None

    @transition(field=state, source=('new', 'failed'),
                target='links_extracted', on_error='failed')
    def extract_links(self):
        def check_link(url):
            url = re.sub(r'#[^#]+$', '', url)
            for d in Document.objects.exclude(pk=self.pk).filter(url=url):
                self.related.add(d)

        base_url = re.search(r'https?://(?P<base_url>[^/]+)/',
                             self.url).group('base_url')
        for match in re.finditer(r'href=\"(?P<url>[^\"]+)\"', self.text):
            url = match.group('url')
            if re.match(r'https?://%s' % base_url, url):
                check_link(url)
            elif url.startswith('/'):
                if self.url.startswith('https'):
                    proto = 'https://'
                else:
                    proto = 'http://'
                check_link(proto + base_url + url)

    def save(self, *args, **kwargs):
        if not self.id:
            self.hash = sha512(self.text.encode('utf-8')).hexdigest()
        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else self.url

    class Meta:
        ordering = ('-updated_at',)
