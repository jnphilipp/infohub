from parsers.parsers.base import BaseParser
from html import unescape
import re

class DefaultParser(BaseParser):
	def get_text(self, document):
		document.text = unescape(re.sub(r'<[^>]+>', '', document.content))