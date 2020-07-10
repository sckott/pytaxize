import os
from nose.tools import *
import unittest
import vcr
from pytaxize import Children
import pytest

class ChildrenTest(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/children_itis.yml")
    def test_children_itis(self):
        "Children: itis"
        x = Children([179913, 174321, 9999999])
        assert type(x) == Children
        assert x.ids == [179913, 174321, 9999999]
        assert len(x.ids) == 3
        res = x.itis()
        assert len(x.ids) == 3
        assert type(res) == dict
        assert type(res[179913]) == list
        assert type(res[179913][0]) == dict
