from parsers.parsers.base import HTMLParser
import re
import urllib

class FAZParser(HTMLParser):
	def get_text(self, document):
		try:
			org = super().fetch('%s?printPagedArticle=true' % document.url)
		except (urllib.error.HTTPError, urllib.error.URLError) as e:
			return

		s = ''
		m = re.search(r'<div[^>]*class="FAZArtikelText"[^>]*>(.+?)<div class="ArtikelFooter">', org, re.DOTALL | re.MULTILINE)
		if m:
			text = re.sub(r'<span class="Bildunterschrift[^>]*>.+?</span>', ' ', m.group(1), 0, re.DOTALL | re.MULTILINE)
			text = re.sub(r'<p class="Bildunterschrift[^>]*>.+?</p>', ' ', text, 0, re.DOTALL | re.MULTILINE)
			matchs = re.finditer(r'<p[^>]*>(.+?)</p>', text, re.DOTALL | re.MULTILINE)
			for match in matchs:
				s += ' ' + super().clean_unescape(re.sub(r'<[^>]*>.+<[^>]*>', '', match.group(1), 0, re.DOTALL | re.MULTILINE))

		match = re.search('name="keywords" content="([^"]+)"', org)
		if match:
			topics = set(super().clean_unescape(match.group(1)).split(', '))
			if '' in topics: topics.remove('')
			document.meta += '<topics>%s</topics>' % ''.join(['<topic>%s</topic>' % topic for topic in topics])

		document.text = super().clean_unescape(s)