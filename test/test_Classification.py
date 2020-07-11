
import os
from nose.tools import *
import unittest
import vcr
from pytaxize import Classification
import pytest


class Classification_tests(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/classify_itis_1.yml")   
    def test_classification_itis_single(self):
        self.individual_id_retrieval("itis",558090)

    @vcr.use_cassette("test/vcr_cassettes/classify_itis_2.yml")   
    def test_classification_itis_list(self):
        self.individual_id_retrieval("itis",[558090,183671])

    def individual_id_retrieval(self,db,data):
        expected_data = data
        if isinstance(data,int):
            expected_data = [expected_data]
        x = Classification(data)
        assert type(x) == Classification
        assert x.ids == expected_data
        result = self.load_appropriate_result(x,db)
        assert len(x.ids) == len(expected_data)
        assert isinstance(result,list)

    def load_appropriate_result(self,instance,db):
        if db == "gbif":
            return instance.gbif()
        if db == "eol":
            return instance.eol()
        if db == "itis":
            return instance.itis()
        if db == "ncbi":
            return instance.ncbi() 