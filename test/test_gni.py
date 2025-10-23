"""Tests for GNI module of pytaxize"""
import unittest

import vcr

from pytaxize import gn

a = {
    "data": [
        {
            "data_source": {
                "created_at": "2009/08/14 18:56:01 +0000",
                "data_hash": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                "data_url": "http://gnapartnership.org/gna_test/ion/data.xml",
                "data_zip_compressed": None,
                "description": "ION will ultimately contain all the organism names related data found within the Thomson Reuters life science literature databases.",
                "id": 30,
                "name_strings_count": 4104326,
                "refresh_period_days": 14,
                "title": "Index to Organism Names",
                "unique_names_count": 2511782,
                "updated_at": "2010/05/14 22:47:59 +0000",
                "web_site_url": "http://www.organismnames.com/",
            },
            "name_index_id": 98448788,
            "records": [
                {
                    "created_at": "2009/09/27 10:27:31 +0000",
                    "global_id": None,
                    "id": 127858346,
                    "kingdom_id": None,
                    "local_id": "2521957",
                    "name_index_id": 98448788,
                    "name_rank_id": 2,
                    "nomenclatural_code_id": None,
                    "original_name_string": None,
                    "record_hash": None,
                    "updated_at": "2009/09/27 10:27:31 +0000",
                    "url": "http://www.organismnames.com/details.htm?lsid=2521957",
                }
            ],
            "records_number": 1,
        }
    ],
    "name_string": {
        "canonical_form_id": 5703176,
        "created_at": "2009/08/14 15:14:10 +0000",
        "has_words": True,
        "id": 17802847,
        "is_canonical_form": 1,
        "lsid": "urn:lsid:globalnames.org:index:35fa270e-1a07-5e5d-914c-90230dc8680a",
        "name": "Acallepitrix anila",
        "normalized": "ACALLEPITRIX ANILA",
        "resource_uri": None,
        "updated_at": "2009/08/14 15:14:10 +0000",
        "uuid_hex": "35fa270e-1a07-5e5d-914c-90230dc8680a",
    },
}

b = [
    {
        "scientificName": {
            "canonical": "Cyanistes caeruleus",
            "details": [
                {
                    "genus": {"string": "Cyanistes"},
                    "species": {"string": "caeruleus"},
                }
            ],
            "hybrid": False,
            "normalized": "Cyanistes caeruleus",
            "parsed": True,
            "parser_run": 1,
            "parser_version": "3.1.4",
            "positions": {"0": ["genus", 9], "10": ["species", 19]},
            "verbatim": "Cyanistes caeruleus",
        }
    },
    {
        "scientificName": {
            "canonical": "Helianthus annuus",
            "details": [
                {
                    "genus": {"string": "Helianthus"},
                    "species": {"string": "annuus"},
                }
            ],
            "hybrid": False,
            "normalized": "Helianthus annuus",
            "parsed": True,
            "parser_run": 1,
            "parser_version": "3.1.4",
            "positions": {"0": ["genus", 10], "11": ["species", 17]},
            "verbatim": "Helianthus annuus",
        }
    },
]

c = {
    "per_page": 1,
    "name_strings": [
        {
            "uuid_hex": "efef32c0-8314-5c6e-b427-7d5b121898e8",
            "lsid": "urn:lsid:globalnames.org:index:efef32c0-8314-5c6e-b427-7d5b121898e8",
            "id": 22067449,
            "name": "? Anisolabidinae",
            "resource_uri": "http://gni.globalnames.org/name_strings/22067449.xml",
        }
    ],
    "page_number": "1",
    "name_strings_total": 27059,
}


class Gni(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/gn_parse.yml")
    def test_gni_parse(self):
        "gn.parse"
        assert b == gn.parse(names=["Cyanistes caeruleus", "Helianthus annuus"])

    @vcr.use_cassette("test/vcr_cassettes/gn_search.yml")
    def test_gni_search(self):
        "gn.search"
        assert c == gn.search("ani*", per_page=1)

    @vcr.use_cassette("test/vcr_cassettes/gn_details.yml")
    def test_gni_details(self):
        "gn.details"
        assert a == gn.details(id=17802847)
