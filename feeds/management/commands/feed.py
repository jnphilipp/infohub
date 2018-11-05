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

from django.core.mail import mail_admins
from django.core.management.base import BaseCommand
from feeds.models import Feed
from infohub.management.base import SingleInstanceCommand


class Command(SingleInstanceCommand):
    help = 'Update the feeds.'

    def add_arguments(self, parser):
        parser.add_argument('feeds', nargs='*', default=[], help='Feeds')
        parser.add_argument('--state', default='alive',
                            choices=['alive', 'failed'], help='Source state')

    def handle(self, *args, **options):
        self._run_once()

        if options['feeds']:
            feeds = Feed.objects.filter(Q(slug__in=options['feeds']) |
                                        Q(url__in=options['feeds']) |
                                        Q(title__in=options['feeds']))
        else:
            feeds = Feed.objects.filter(state=options['state'])

        msg = ''
        for feed in feeds:
            try:
                nb = feed.documents.count()
                feed.update()
                nb = feed.documents.count() - nb
                self._success('* %s: %+d' % (feed, nb))
            except Exception as e:
                self._error('* %s: %s' % (feed, e))
                msg += '* %s: %s' % (feed, e)
            feed.save()

        if msg:
            mail_admins('Feed failed', msg)
