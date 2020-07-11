import os
from nose.tools import *
import unittest
import vcr
from pytaxize import Ids
import pytest


class IdsTest(unittest.TestCase):
    # @vcr.use_cassette("test/vcr_cassettes/ids_ncbi.yml")
    # @pytest.mark.skipif(
    #     "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    #     reason="Skipping this test on Travis CI.",
    # )
    # def test_ids_ncbi(self):
    #     "Ids: ncbi"
    #     x = Ids("Poa annua")
    #     assert type(x) == Ids
    #     assert x.name == ["Poa annua"]
    #     assert len(x.ids) == 0
    #     x.ncbi()
    #     assert len(x.ids) > 0
    #     assert x.db_ids == "ncbi"
    
    @vcr.use_cassette("test/vcr_cassettes/ids_gbif_1.yml")
    def test_ids_gbif_single_name(self):
        x = Ids("Panthera tigris")
        assert type(x) == Ids
        assert x.name == ["Panthera tigris"]
        assert len(x.ids) == 0
        x.gbif()
        assert len(x.ids) == 1
        assert x.db_ids == "gbif"
        result = x.extract_ids()
        assert isinstance(result,dict)
        assert 'Panthera tigris' in result 

    @vcr.use_cassette("test/vcr_cassettes/ids_gbif_2.yml")   
    def test_ids_gbif_list_of_names(self):
        entry_data = ["Panthera tigris","Panthera leo"]
        x = Ids(entry_data)
        assert x.name == entry_data
        assert len(x.ids) == 0
        x.gbif()
        assert len(x.ids) == 2
        assert x.db_ids == "gbif"
        result = x.extract_ids()
        assert isinstance(result,dict)
        assert all([x in result for x in entry_data])
