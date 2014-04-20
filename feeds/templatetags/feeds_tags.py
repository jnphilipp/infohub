from django.core.urlresolvers import reverse
from django.db.models import Count, Max, Min
from django.template import Library
from django.utils.safestring import mark_safe
from feeds.models import Report, Feed

import json

register = Library()

@register.filter
def startswith(value, start):
	return value.startswith(start)

@register.filter
def num_new_entries(report):
	new_entries = json.loads(report.text)

	count = 0
	for v in new_entries.values():
		try:
			count += v
		except:
			pass

	return count

@register.filter(needs_autoescape=True)
def report_text(report, autoescape=None):
	s = '<table>'
	s += '<tr><th>feed</th><th>number of new documents</th></tr>'
	i = 0
	for key, val in json.loads(report.text).items():
		feed = ''
		try:
			f = Feed.objects.get(slug=key)
			feed = '<a href="%s">%s</a>' % (reverse('feed', args=[f.slug]), f.title)
		except Feed.DoesNotExist:
			feed = key

		s += '<tr class="%s"><td>%s</td><td style="text-align: center;">%s</td></tr>' % ('row1' if i % 2 == 0 else 'row2', feed, val)
		i += 1

	s += '</table>'

	return mark_safe(s)