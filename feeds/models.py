from django.db import models
from sources.models import Source
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^feeds\.models\.TextFieldSingleLine"])

class TextFieldSingleLine(models.TextField):
	pass

class Feed(Source):
	pass