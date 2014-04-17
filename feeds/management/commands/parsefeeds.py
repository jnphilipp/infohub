from django.core import management
from django.core.mail import mail_admins
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from feeds.models import Feed

class Command(BaseCommand):
	help = 'Parses the new feeds.'

	def handle(self, *args, **options):
		new_entries = dict()
		for feed in Feed.objects.all():
			old = feed.document_set.count()
			feed.parse()
			new_entries[str(feed)] = feed.document_set.count() - old

		print(new_entries)