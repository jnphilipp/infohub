from django.core.management.base import BaseCommand
from documents.models import Document

class Command(BaseCommand):
	help = 'Processes the documents.'

	def handle(self, *args, **options):
		for document in Document.objects.filter(feed__parser__isnull=False).filter(state='new'):
			try:
				document.parse()
				document.save()
			except Exception as e:
				print(e)