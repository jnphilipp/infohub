from parsers.parsers.base import HTMLParser
import re
import urllib

class SuddeutscheParser(HTMLParser):
	def get_text(self, document):
		try:
			org = super().fetch(document.url)
			text = super().fetch(super().get_print_link(org))
		except (urllib.error.HTTPError, urllib.error.URLError) as e:
			return

		s = ''
		m = re.search(r'<div[^>]*class="body"[^>]*>(.+)<div[^>]*class="footer"[^>]*>', text, re.DOTALL | re.MULTILINE)
		if m:
			matchs = re.finditer(r'<p>(.+?)</p>', m.group(1), re.DOTALL | re.MULTILINE)
			for match in matchs:
				s += ' ' + super().clean_unescape(re.sub('\s\s+', ' ', re.sub('\n', ' ', match.group(1)))).strip()

		document.text = s.strip()

		match = re.search('name="news_keywords" content="([^"]+)"', org)
		if match:
			topics = set(match.group(1).split(', '))
			if '' in topics: topics.remove('')
			document.meta += '<topics>%s</topics>' % ''.join(['<topic>%s</topic>' % super(SuddeutscheParser, self).clean_unescape(topic).strip() for topic in topics])