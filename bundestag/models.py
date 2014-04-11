from django.db import models
from sources.models import Source

class TextFieldSingleLine(models.TextField):
	pass

class Plenarprotokoll(Source):
	class Meta:
		verbose_name_plural = 'Plenarprotokolle'