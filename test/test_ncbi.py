import os
from nose.tools import *
import unittest
import vcr
from pytaxize import ncbi


class NcbiTest(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/ncbi_search.yml", filter_query_parameters=['api_key'])
    def test_ncbi_search(self):
        "ncbi.search"
        x = ncbi.search(sci_com = "Apis")
        assert type(x) == dict
        assert list(x.keys()) == ["Apis"]
        assert type(x['Apis']) == list
        assert type(x['Apis'][0]) == dict
        assert x['Apis'][0]['ScientificName'] == "Apis"
        assert x['Apis'][0]['TaxId'] == "7459"
