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

import feedparser
import re
import requests

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition
from infohub.fields import SingleLineTextField


class Type(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )
    name = SingleLineTextField(
        unique=True,
        verbose_name=_('Name')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Type')
        verbose_name_plural = _('Types')


class Feed(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    slug = models.SlugField(
        max_length=4096,
        unique=True,
        verbose_name=_('Slug')
    )
    url = models.URLField(
        max_length=2096,
        unique=True,
        verbose_name=_('URL')
    )
    title = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=_('Title')
    )
    state = FSMField(
        default='alive',
        verbose_name=_('State')
    )
    type = models.ForeignKey(
        Type,
        models.CASCADE,
        related_name='feeds',
        verbose_name=_('Type')
    )

    documents = GenericRelation(
        'documents.Document',
        related_query_name='feeds',
        verbose_name=_('Documents')
    )

    @transition(field=state, source=('alive', 'failed'), target='alive',
                on_error='failed')
    def update(self):
        from documents.models import Document

        if self.type.name == 'RSS':
            rssfeed = feedparser.parse(self.url)
            if self.title != rssfeed.feed.title:
                self.title = rssfeed.feed.title
                self.save()

            for entry in rssfeed.entries:
                if not Document.objects.filter(url=entry.link).exists():
                    title = re.sub(r'\s\s+', ' ',
                                   entry.title.replace('\n', ' '))
                    text = requests.get(entry.link).text
                    Document.objects.create(url=entry.link, title=title,
                                            content_object=self, meta=entry,
                                            text=text).hash

    def get_absolute_url(self):
        return reverse('feeds:feed_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.url)
        else:
            orig = Feed.objects.get(pk=self.id)
            if orig.url != self.url:
                self.slug = slugify(self.url)
        super(Feed, self).save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else self.url

    class Meta:
        ordering = ('state', 'url')
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
