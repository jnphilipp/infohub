# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from html import unescape
import re
import urllib

class BaseParser(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def get_text(self, document):
		pass

class HTMLParser(BaseParser):
	user_agent = 'Mozilla/4.0'

	def fetch(self, url):
		response = urllib.request.urlopen(url)
		text = response.read()
		encoding = str(text).lower().split('charset=', 1)[-1].split('"', 1)[0]

		if encoding:
			text = text.decode(encoding)
		else:
			text = str(text)

		response.close()

		return text

	def fetch_with_data(self, url, values):
		headers = {'User-Agent': self.user_agent}
		data = urllib.urlencode(values)
		req = urllib.Request(url, data, headers)
		response = urllib.reques.request.urlopen(req)
		return response.read()

	def get_redirect_url(self, url):
		response = urllib.request.urlopen(url)
		return response.url

	def clean_unescape(self, text):
		return unescape(re.sub(r'<[^>]+>', '', text))

	def get_print_link(self, text):
		match = re.search(r'<a[^>]*href="([^"]+)"[^>]*>([Dd]rucken|[Pp]rint)</a>', text)
		if match:
			return match.group(1)
		else:
			return None