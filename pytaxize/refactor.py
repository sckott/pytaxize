import requests
from lxml import etree

class Refactor:
    def __init__(self, url, payload={}, request='get'):
        self.url = url
        self.payload = payload
        self.request = request

    def return_requests(self, **kwargs):
        if self.request == 'get':
            return requests.get(self.url, params = self.payload, **kwargs)
        else:
            return requests.post(self.url, params = self.payload, **kwargs)

    def xml(self, **kwargs):
        if self.request == 'get':
            out = requests.get(self.url, params = self.payload, **kwargs)
            out.raise_for_status()
            xmlparser = etree.XMLParser()
            tt = etree.fromstring(out.content, xmlparser)
            return tt
        else:
            out = requests.post(self.url, params = self.payload, **kwargs)
            out.raise_for_status()
            xmlparser = etree.XMLParser()
            tt = etree.fromstring(out.content, xmlparser)
            return tt

    def json(self, **kwargs):
        if self.request == 'get':
            out = requests.get(self.url, params = self.payload, **kwargs)
            out.raise_for_status()
            return out.json()
        else:
            out = requests.post(self.url, params = self.payload, **kwargs)
            out.raise_for_status()
            return out.json()

    def raw(self, **kwargs):
        if self.request == 'get':
            out = requests.get(self.url, params = self.payload, **kwargs)
            out.raise_for_status()
            return out.text
        else:
            out = requests.post(self.url, params = self.payload, **kwargs)
            out.raise_for_status()
            return out.text
