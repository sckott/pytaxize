"""Tests for col module of pytaxize"""
import os
from nose.tools import *
import unittest
import vcr
import pytaxize

class COL(unittest.TestCase):

    @vcr.use_cassette('test/vcr_cassettes/col_children.yml')
    def test_col_children(self):
        "Basic test of its col_children"
        self.assertIsInstance(pytaxize.col.col_children(name=["Apis"]), list)

    @raises(ValueError)
    def test_col_children_fail_well(self):
        "col_children checklist param fail well"
        pytaxize.col.col_children(name=["Apis"], checklist=2008)

    @vcr.use_cassette('test/vcr_cassettes/col_children.yml')
    def test_col_children(self):
        "Basic test of its col_downstream"
        res = pytaxize.col.col_downstream(name=["Apis"], downto="Species")
        self.assertIsInstance(pytaxize.col.col_children(name=["Apis"]), list)
