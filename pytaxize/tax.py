import sys
import requests
from lxml import etree
import pandas as pd
import re
import json
from pkg_resources import resource_filename
from pytaxize.refactor import Refactor

class NoResultException(Exception):
    pass

def names_list(rank = 'genus', size = 10):
    '''
    Get a random vector of species names.

    :param rank: Taxonomic rank, one of species, genus (default), family, order.
    :param size: Number of names to get. Maximum depends on the rank.

    Usage::

        import pytaxize
        pytaxize.names_list()
        pytaxize.names_list('species')
        pytaxize.names_list('family')
        pytaxize.names_list('order')
        pytaxize.names_list('order', 2)
        pytaxize.names_list('order', 15)
    '''
    if(rank == 'species'):
      return names_list_helper(size, 'data/plantNames.csv')
    if(rank == 'genus'):
      return names_list_helper(size, 'data/plantGenusNames.csv')
    if(rank == 'family'):
      return names_list_helper(size, 'data/apg_families.csv')
    if(rank == 'order'):
      return names_list_helper(size, 'data/apg_orders.csv')
    else:
      return 'rank must be one of species, genus, family, or order'

def names_list_helper(size, path):
  pnpath = resource_filename(__name__, path)
  dat = pd.read_csv(pnpath, header=False)
  dat2 = dat['names'][:size]
  return [x for x in dat2]

def vascan_search(q, format='json', raw=False):
    '''
    Search the CANADENSYS Vascan API.

    :param q: Taxonomic rank, one of species, genus (default), family, order.
    :param format: Number of names to get. Maximum depends on the rank.
    :param raw: Raw data or not (default)
    :param callopts: Further args passed to request

    Usage::

        import pytaxize
        pytaxize.vascan_search(q = ["Helianthus annuus"])
        pytaxize.vascan_search(q = ["Helianthus annuus"], raw=True)
        pytaxize.vascan_search(q = ["Helianthus annuus", "Crataegus dodgei"], raw=True)

        # format type
        ## json
        pytaxize.vascan_search(q = ["Helianthus annuus"], format="json", raw=True)

        ## xml
        pytaxize.vascan_search(q = ["Helianthus annuus"], format="xml", raw=True)

        # lots of names, in this case 50
        splist = pytaxize.names_list(rank='species', size=50)
        pytaxize.vascan_search(q = splist)
    '''
    if(format == 'json'):
        url = "http://data.canadensys.net/vascan/api/0.1/search.json"
    else:
        url = "http://data.canadensys.net/vascan/api/0.1/search.xml"

    if(len(q) > 1):
        query = "\n".join(q)
        payload = {'q': query}
        if(format == 'json'):
          out = Refactor(url, payload, request='post').json()
        else:
          out = Refactor(url, payload, request='post').raw()
        return out
    else:
        payload = {'q': q}
        if(format == 'json'):
          out = Refactor(url, payload, request='get').json()
        else:
          out = Refactor(url, payload, request='get').raw()
        return out

def scrapenames(url = None, file = None, text = None, engine = None,
  unique = None, verbatim = None, detect_language = None, all_data_sources = None,
  data_source_ids = None):
  '''
  Resolve names using Global Names Recognition and Discovery.

  Uses the Global Names Recognition and Discovery service, see
  http://gnrd.globalnames.org/.

  :param url: An encoded URL for a web page, PDF, Microsoft Office document, or
     image file, see examples
  :param file: When using multipart/form-data as the content-type, a file may be sent.
     This should be a path to your file on your machine.
  :param text: Type: string. Text content; best used with a POST request, see
     examples
  :param engine: (optional) Type: integer, Default: 0. Either 1 for TaxonFinder,
     2 for NetiNeti, or 0 for both. If absent, both engines are used.
  :param unique: (optional) Type: boolean. If TRUE (default),
     response has unique names without offsets.
  :param verbatim: (optional) Type: boolean, If TRUE (default to FALSE),
     response excludes verbatim strings.
  :param detect_language: (optional) Type: boolean, When
     TRUE (default), NetiNeti is not used if the language of incoming text is
     determined not to be English. When 'false', NetiNeti will be used if requested.
  :param all_data_sources: (optional) Type: bolean. Resolve found
     names against all available Data Sources.
  :param data_source_ids: (optional) Type: string. Pipe separated list of data
     source ids to resolve found names against. See list of Data Sources.

  Usage::

      # Get data from a website using its URL
      out = pytaxize.scrapenames(url = 'http://en.wikipedia.org/wiki/Araneae')
      out['data'].head() # data
      out['meta'] # metadata

      # Scrape names from a pdf at a URL
      out = pytaxize.scrapenames(url = 'http://www.mapress.com/zootaxa/2012/f/z03372p265f.pdf')
      out['data'].head() # data
      out['meta'] # metadata

      # With arguments
      pytaxize.scrapenames(url = 'http://www.mapress.com/zootaxa/2012/f/z03372p265f.pdf',
      unique=TRUE)
      pytaxize.scrapenames(url = 'http://www.mapress.com/zootaxa/2012/f/z03372p265f.pdf', all_data_sources=TRUE)

      # Get data from text string as an R object
      pytaxize.scrapenames(text='A spider named Pardosa moesta Banks, 1892')
  '''
  method = {'url': url, 'file': file, 'text': text}
  method = {key: value for key, value in method.items() if value != None}
  if(len(method) > 1):
    sys.exit("Only one of url, file, or text can be used")

  base = "http://gnrd.globalnames.org/name_finder.json"
  payload = {'url':url, 'text':text, 'engine':engine, 'unique':unique,
             'verbatim':verbatim, 'detect_language':detect_language,
             'all_data_sources':all_data_sources, 'data_source_ids':data_source_ids}

  ss = []
  for i in range(len(method.keys())):
    ss.append(list(method.keys())[i] in ['url','text'])
  out = requests_refactor(base, payload, 'get', content=True)

  if(out['status'] != 303):
    sys.exit("Woops, something went wrong")
  else:
    token_url = out['token_url']
    st = 303
    while(st == 303):
      datout = requests_refactor(token_url, content=True)
      st = datout['status']
    dd = pd.DataFrame(datout['names'])
    datout.pop('names')
    meta = datout
    return {'meta': meta, 'data': dd}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
