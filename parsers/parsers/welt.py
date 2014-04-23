from parsers.parsers.base import HTMLParser
import re
import urllib

class DieWeltParser(HTMLParser):
	def get_text(self, document):
		try:
			text = super().fetch('%s?config=print' % document.url)
		except (urllib.error.HTTPError, urllib.error.URLError) as e:
			return

		s = ''
		matchs = re.finditer(r'<p class="text">(.+?)</p>', text, re.DOTALL | re.MULTILINE)
		for match in matchs:
			s += ' ' + super().clean_unescape(re.sub('\s\s+', ' ', re.sub('\n', ' ', re.sub(r'<span class="url">.+?</span>', '', match.group(1), re.DOTALL | re.MULTILINE)))).strip()

		document.text = s.strip()