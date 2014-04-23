from feeds.parsers.base import HTMLParser
import re
import urllib

class ZeitOnlineParser(HTMLParser):
	def get_text(self, document):
		try:
			text = super().fetch('%s?print=true' % document.url)
		except (urllib.error.HTTPError, urllib.error.URLError) as e:
			return

		s = ''
		m = re.search(r'<!--start: content-->(.+?)<div[^>]*class="[^"]*articlefooter[^"]*">', text, re.DOTALL | re.MULTILINE)
		if m:
			matchs = re.finditer(r'<p>(.+?)</p>', re.sub(r'<div[^>]*class="block infobox"[^>]*><dl>.+</dl></div>', '', m.group(1), 1, re.DOTALL | re.MULTILINE), re.DOTALL | re.MULTILINE)
			for match in matchs:
				s += ' ' + super().clean_unescape(re.sub('\s\s+', ' ', re.sub('\n', ' ', match.group(1)))).strip()

		document.text = s.strip()

		try:
			text = super().fetch(document.url)
		except (urllib.error.HTTPError, urllib.error.URLError) as e:
			return

		match = re.search('name="keywords" content="([^"]+)"', text)
		if match:
			topics = set(match.group(1).split(', '))
			if '' in topics: topics.remove('')
			document.meta += '<topics>%s</topics>' % ''.join(['<topic>%s</topic>' % topic for topic in topics])