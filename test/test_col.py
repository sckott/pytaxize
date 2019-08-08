"""Tests for col module of pytaxize"""
import os
from nose.tools import *
import unittest
import vcr
import pandas
import pytaxize

class COL(unittest.TestCase):

    @vcr.use_cassette('test/vcr_cassettes/col_children.yml')
    def test_col_children(self):
        "COL: col_children"
        self.assertIsInstance(pytaxize.col.col_children(name=["Apis"]), list)

    @raises(ValueError)
    def test_col_children_fail_well(self):
        "COL: col_children checklist param fails well"
        pytaxize.col.col_children(name=["Apis"], checklist=2008)

    @vcr.use_cassette('test/vcr_cassettes/col_downstream.yml')
    def test_col_downstream(self):
        "COL: col_downstream"
        res = pytaxize.col.col_downstream(name=["Apis"], downto="Species")
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0][0], pandas.core.frame.DataFrame)
