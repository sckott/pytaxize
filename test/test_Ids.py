import os
from nose.tools import *
import unittest
import vcr
from pytaxize import Ids

class IdsTest(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/ids_ncbi.yml")
    def test_ids_ncbi(self):
        "Ids: ncbi"
        x = Ids('Poa annua')
        assert type(x) == Ids
        assert x.name == ["Poa annua"]
        assert len(x.ids) == 0
        x.ncbi()
        assert len(x.ids) > 0
        assert x.db_ids == "ncbi"
