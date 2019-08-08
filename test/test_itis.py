"""Tests for ITIS module of pytaxize"""
import os
from nose.tools import *
import unittest
import vcr
import pytaxize

class ITIS(unittest.TestCase):

    @vcr.use_cassette('test/vcr_cassettes/itis_getacceptednamesfromtsn.yml')
    def test_itis_getacceptednamesfromtsn(self):
        "ITIS: getaccepednamesfromtsn"
        assert pytaxize.itis.getacceptednamesfromtsn('208527') == '208527'

    @vcr.use_cassette('test/vcr_cassettes/itis_getcommentdetailfromtsn.yml')
    def test_itis_getcommentdetailfromtsn(self):
        "ITIS: getcommentdetailfromtsn"
        comments =  pytaxize.itis.getcommentdetailfromtsn(tsn=180543)
        assert set(comments.keys()) == set(['commentator', 'comment', 'commtime',
                                         'updatedate', 'commid'])

    @vcr.use_cassette('test/vcr_cassettes/itis_searchbycommonname.yml')
    def test_itis_searchbycommonname(self):
        "ITIS: searchbycommonname"
        df = pytaxize.searchbycommonname("grizzly")
        assert set(list(df.columns)) == set(['tsn', 'language', 'commonname'])

    @vcr.use_cassette('test/vcr_cassettes/tis_gethierarchyupfromtsn.yml')
    def test_itis_gethierarchyupfromtsn(self):
        "ITIS: gethierarchyupfromtsn"
        hierarchy = pytaxize.gethierarchyupfromtsn(tsn = 36485)
        assert hierarchy[0]['rankName'] == 'Genus'
