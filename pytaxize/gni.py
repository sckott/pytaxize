import sys
import requests
import json

class NoResultException(Exception):
    pass

def gni_parse(names):
    '''
    Uses the Global Names Index to parse scientific names

    :param names: List of scientific names.

    Usage:
    >>> import pytaxize
    >>> pytaxize.gni_parse(names = ['Cyanistes caeruleus','Helianthus annuus'])
    [{u'scientificName': {u'canonical': u'Cyanistes caeruleus',
       u'details': [{u'genus': {u'string': u'Cyanistes'},
         u'species': {u'string': u'caeruleus'}}],
       u'hybrid': False,
       u'normalized': u'Cyanistes caeruleus',
       u'parsed': True,
       u'parser_run': 1,
       u'parser_version': u'3.1.2',
       u'positions': {u'0': [u'genus', 9], u'10': [u'species', 19]},
       u'verbatim': u'Cyanistes caeruleus'}},
     {u'scientificName': {u'canonical': u'Helianthus annuus',
       u'details': [{u'genus': {u'string': u'Helianthus'},
         u'species': {u'string': u'annuus'}}],
       u'hybrid': False,
       u'normalized': u'Helianthus annuus',
       u'parsed': True,
       u'parser_run': 1,
       u'parser_version': u'3.1.2',
       u'positions': {u'0': [u'genus', 10], u'11': [u'species', 17]},
       u'verbatim': u'Helianthus annuus'}}]
    '''
    url = 'http://gni.globalnames.org/parsers.json'
    names = '|'.join(names)
    out = requests.get(url, params = {'names': names})
    out.raise_for_status()
    return out.json()

def gni_search(search_term='ani*', per_page=30, page=1):
    '''
    Search for names against the Global names index

    :param search_term: Search term
    :param per_page: Items to return per page
    :param page: Page to return

    Usage:
    >>> import pytaxize
    >>> pytaxize.gni_search(search_term = 'ani*')
    '''
    url = 'http://gni.globalnames.org/name_strings.json'
    out = requests.get(url, params = {'search_term': search_term, 'per_page': per_page, 'page': page})
    out.raise_for_status()
    return out.json()

def gni_details(id=17802847, all_records=1):
    '''
    Usage:
    >>> import pytaxize
    >>> pytaxize.gni_details(id = 17802847)
    {u'data': [{u'data_source': {u'created_at': u'2009/08/14 18:56:01 +0000',
        u'data_hash': u'da39a3ee5e6b4b0d3255bfef95601890afd80709',
        u'data_url': u'http://gnapartnership.org/gna_test/ion/data.xml',
        u'data_zip_compressed': None,
        u'description': u'ION will ultimately contain all the organism names related data found within the Thomson Reuters life science literature databases.',
        u'id': 30,
        u'name_strings_count': 4104326,
        u'refresh_period_days': 14,
        u'title': u'Index to Organism Names',
        u'unique_names_count': 2511782,
        u'updated_at': u'2010/05/14 22:47:59 +0000',
        u'web_site_url': u'http://www.organismnames.com/'},
       u'name_index_id': 98448788,
       u'records': [{u'created_at': u'2009/09/27 10:27:31 +0000',
         u'global_id': None,
         u'id': 127858346,
         u'kingdom_id': None,
         u'local_id': u'2521957',
         u'name_index_id': 98448788,
         u'name_rank_id': 2,
         u'nomenclatural_code_id': None,
         u'original_name_string': None,
         u'record_hash': None,
         u'updated_at': u'2009/09/27 10:27:31 +0000',
         u'url': u'http://www.organismnames.com/details.htm?lsid=2521957'}],
       u'records_number': 1}],
     u'name_string': {u'canonical_form_id': 5703176,
      u'created_at': u'2009/08/14 15:14:10 +0000',
      u'has_words': True,
      u'id': 17802847,
      u'is_canonical_form': 1,
      u'lsid': u'urn:lsid:globalnames.org:index:35fa270e-1a07-5e5d-914c-90230dc8680a',
      u'name': u'Acallepitrix anila',
      u'normalized': u'ACALLEPITRIX ANILA',
      u'resource_uri': None,
      u'updated_at': u'2009/08/14 15:14:10 +0000',
      u'uuid_hex': u'35fa270e-1a07-5e5d-914c-90230dc8680a'}}
    '''
    url = 'http://gni.globalnames.org/name_strings/'
    mylist = [url, str(id), '.json']
    url2 = ''.join(mylist)
    out = requests.get(url2, params = {'all_records': all_records})
    out.raise_for_status()
    try:
        data = out.json()
        return data
    except (ValueError):
        raise NoResultException("GNI didn't return a result (id: %s)" % id)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
