from parsers.parsers.base import HTMLParser
import re
import urllib

class FocusParser(HTMLParser):
	def get_text(self, document):
		try:
			text = super().fetch('%s?drucken=1' % document.url)
		except (urllib.error.HTTPError, urllib.error.URLError) as e:
			return

		s = ''
		match = re.search(r'<div class="leadIn">\s*?<p>(.+?)</p>\s*?</div>', text, re.DOTALL | re.MULTILINE)
		if match:
			s = super().clean_unescape(match.group(1))

		matchs = re.finditer(r'<div class="textBlock">(.+?)</div>', text, re.DOTALL | re.MULTILINE)
		for match in matchs:
			ps = re.finditer(r'(<p>(.+?)</p>|<h2>(.+?)</h2>)', match.group(1), re.DOTALL | re.MULTILINE)
			for m in ps:
				s += ' ' + super().clean_unescape(m.group(1))


		match = re.search('name="news_keywords" content="([^"]+)"', text)
		if match:
			topics = set(super().clean_unescape(match.group(1)).split(', '))
			if '' in topics: topics.remove('')
			document.meta += '<topics>%s</topics>' % ''.join(['<topic>%s</topic>' % topic for topic in topics])

		document.text = s.strip()