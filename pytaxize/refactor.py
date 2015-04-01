import requests
from lxml import etree

def requests_refactor(endpt, payload, request, content=True, format= 'json', **kwargs):
    if request == 'get':
        out = requests.get(endpt, params = payload, **kwargs)
        out.raise_for_status()
        if content == True:
            if format == 'json':
                return out.json()
            else:
                return out.raw()
        else:
            xmlparser = etree.XMLParser()
            tt = etree.fromstring(out.content, xmlparser)
            return tt
    else:
        out = requests.post(endpt, params = payload)
        out.raise_for_status()
        if content == True:
            if format == 'json':
                return out.json()
            else:
                return out.raw()
        else:
            xmlparser = etree.XMLParser()
            tt = etree.fromstring(out.content, xmlparser)
            return tt
