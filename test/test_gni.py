"""Tests for GNI module of pytaxize"""
import os
import pytaxize

a = {u'data': [{u'data_source': {u'created_at': u'2009/08/14 18:56:01 +0000',
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

b = [{u'scientificName': {u'canonical': u'Cyanistes caeruleus',
   u'details': [{u'genus': {u'string': u'Cyanistes'},
     u'species': {u'string': u'caeruleus'}}],
   u'hybrid': False,
   u'normalized': u'Cyanistes caeruleus',
   u'parsed': True,
   u'parser_run': 1,
   u'parser_version': u'3.1.4',
   u'positions': {u'0': [u'genus', 9], u'10': [u'species', 19]},
   u'verbatim': u'Cyanistes caeruleus'}},
 {u'scientificName': {u'canonical': u'Helianthus annuus',
   u'details': [{u'genus': {u'string': u'Helianthus'},
     u'species': {u'string': u'annuus'}}],
   u'hybrid': False,
   u'normalized': u'Helianthus annuus',
   u'parsed': True,
   u'parser_run': 1,
   u'parser_version': u'3.1.4',
   u'positions': {u'0': [u'genus', 10], u'11': [u'species', 17]},
   u'verbatim': u'Helianthus annuus'}}]

c = {u'per_page': 1,
    u'name_strings': [{u'uuid_hex': u'efef32c0-8314-5c6e-b427-7d5b121898e8',
    u'lsid': u'urn:lsid:globalnames.org:index:efef32c0-8314-5c6e-b427-7d5b121898e8',
    u'id': 22067449, u'name': u'? Anisolabidinae',
    u'resource_uri': u'http://gni.globalnames.org/name_strings/22067449.xml'}],
    u'page_number': u'1', u'name_strings_total': 27059}

def test_gni_parse():
    "Basic test of gni_parse"
    assert b == pytaxize.gni_parse(names = ['Cyanistes caeruleus','Helianthus annuus'])

def test_gni_search():
    "Basic test of gni_search"
    assert c == pytaxize.gni_search('ani*', per_page=1)

def test_gni_details():
    "Basic test of gni_details"
    assert a == pytaxize.gni_details(id = 17802847)
