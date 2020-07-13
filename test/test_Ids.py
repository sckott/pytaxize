import os
from nose.tools import *
import unittest
import vcr
from pytaxize import Ids
import pytest


class IdsTest(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/ids_ncbi.yml")
    @pytest.mark.skipif(
        "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
        reason="Skipping this test on Travis CI.",
    )
    def test_ids_ncbi(self):
        "Ids: ncbi"
        x = Ids("Poa annua")
        assert type(x) == Ids
        assert x.name == ["Poa annua"]
        assert len(x.ids) == 0
        x.ncbi()
        assert len(x.ids) > 0
        assert x.db_ids == "ncbi"
    
    @vcr.use_cassette("test/vcr_cassettes/ids_gbif_1.yml")
    def test_ids_gbif_single_name(self):
        self.individual_id_retrieval("gbif","Panthera tigris")

    @vcr.use_cassette("test/vcr_cassettes/ids_gbif_2.yml")   
    def test_ids_gbif_list_of_names(self):
        self.individual_id_retrieval("gbif",["Panthera tigris","Panthera leo"])

    @vcr.use_cassette("test/vcr_cassettes/ids_eol_1.yml")
    def test_ids_eol_single_name(self):
        self.individual_id_retrieval("eol","Panthera tigris")

    @vcr.use_cassette("test/vcr_cassettes/ids_eol_2.yml")   
    def test_ids_eol_list_of_names(self):
        self.individual_id_retrieval("eol",["Panthera tigris","Panthera leo"])

    @vcr.use_cassette("test/vcr_cassettes/ids_itis_1.yml")
    def test_ids_itis_single_name(self):
        self.individual_id_retrieval("itis","Panthera tigris")

    @vcr.use_cassette("test/vcr_cassettes/ids_itis_2.yml")   
    def test_ids_itis_list_of_names(self):
        self.individual_id_retrieval("itis",["Panthera tigris","Panthera leo"])

    def individual_id_retrieval(self,db,data):
        expected_data = data
        if isinstance(data,str):
            expected_data = [expected_data]
        x = Ids(data)
        assert type(x) == Ids
        assert x.name == expected_data
        assert len(x.ids) == 0
        self.load_appropriate_ids(x,db)
        assert len(x.ids) == len(expected_data)
        assert x.db_ids == db
        result = x.extract_ids()
        assert isinstance(result,dict)
        assert all(x in result for x in expected_data)
    
    def load_appropriate_ids(self,instance,db):
        if db == "gbif":
            instance.gbif()
        if db == "eol":
            instance.eol()
        if db == "itis":
            instance.itis()
        if db == "ncbi":
            instance.ncbi()