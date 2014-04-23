from feeds.parsers.base import HTMLParser
import re
import urllib

class SpiegelParser(HTMLParser):
	def get_text(self, document):
		try:
			text = super().fetch(document.url)
			print_link = super().get_print_link(text)
			text = super().fetch('http://www.spiegel.de%s' % print_link)
		except (urllib.error.HTTPError, urllib.error.URLError) as e:
			return

		s = ''
		match = re.search(r'(<p>.+</p>).*?(?=<p><i>.+?</i></p>|URL)', text, re.MULTILINE | re.DOTALL)
		if match:
			matchs = re.finditer(r'<p>(.+?)</p>', match.group(1), re.MULTILINE | re.DOTALL)
			for m in matchs:
				end = re.search(r'<p><i>.+?</i></p>', m.group(0))
				if end:
					continue

				s += ' ' + super().clean_unescape(re.sub('\s\s+', ' ', re.sub('\n', ' ', m.group(1)))).strip()
		else:
			return

		match = re.search('name="keywords" content="([^"]+)"', text)
		if match:
			topics = set(match.group(1).split(', '))
			if '' in topics: topics.remove('')
			document.meta += '<topics>%s</topics>' % ''.join(['<topic>%s</topic>' % topic for topic in topics])

		document.text = s.strip()