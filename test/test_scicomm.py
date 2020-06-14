import os
from nose.tools import *
import unittest
import vcr
from pytaxize import scicomm
from pytaxize import Ids
import pytest

class SciComm(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/sci2comm_str_ncbi.yml")
    @pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", 
reason="Skipping this test on Travis CI.")
    def test_sci2comm_str_ncbi(self):
        "sci2comm/str/ncbi"
        x = 'Helianthus annuus'
        res = scicomm.sci2comm(x)
        assert type(res) == dict
        assert set(res.keys()) == {x}
