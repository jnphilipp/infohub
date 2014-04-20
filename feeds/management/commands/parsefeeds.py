from django.core import management
from django.core.mail import mail_admins
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from feeds.models import Feed, Report

import json

class Command(BaseCommand):
	help = 'Parses the new feeds.'

	def handle(self, *args, **options):
		new_entries = dict()
		for feed in Feed.objects.all():
			old = feed.document_set.count()
			try:
				feed.parse()
				new_entries[feed.slug()] = feed.document_set.count() - old
			except Exception as e:
				new_entries[feed.slug()] = str(e).strip()

		report = Report.objects.create(text=json.dumps(new_entries))
		self.stdout.write('Report: (%s)\n %s' % (report.created_at, report.text))