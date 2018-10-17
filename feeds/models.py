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

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from infohub.fields import SingleLineTextField


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
    alive = models.BooleanField(
        default=True,
        verbose_name=_('Alive')
    )

    def get_absolute_url(self):
        return reverse('feed', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        else:
            orig = Feed.objects.get(pk=self.id)
            if orig.name != self.name:
                self.slug = slugify(self.name)
        super(Feed, self).save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else self.url

    class Meta:
        abstract = True
        ordering = ('alive', 'title')
