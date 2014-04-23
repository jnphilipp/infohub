from django.core import management
from django.core.mail import mail_admins
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from feeds.models import Document

import re
import urllib

class Command(BaseCommand):
	help = 'Processes the documents.'

	def handle(self, *args, **options):
		for document in Document.objects.filter(Q(feed__slug='httpwwwspiegeldeschlagzeilenindexrss') | Q(feed__slug='httpnewsfeedzeitdeall')).filter(state='new'):
			try:
				document.parse()
				document.save()
			except:
				pass