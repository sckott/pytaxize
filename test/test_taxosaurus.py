import os
from nose.tools import *
import unittest
import vcr
import pytaxize

class Taxosaurus(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/taxo_datasources.yml")
    def test_taxo_datasources(self):
        "taxo_datasources"
        res = pytaxize.taxo_datasources()
        assert isinstance(res, list)
        assert isinstance(res[0], dict)
        assert [z["sourceId"] for z in res] == ['NCBI', 'iPlant_TNRS', 'MSW3']

    @vcr.use_cassette("test/vcr_cassettes/taxo_resolve.yml")
    def test_taxo_resolve(self):
        "taxo_resolve"
        res = pytaxize.taxo_resolve(query='Helianthus annus')
        assert isinstance(res, list)
        assert isinstance(res[0], list)
        assert isinstance(res[0][0], dict)
