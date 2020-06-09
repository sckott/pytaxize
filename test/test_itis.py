"""Tests for ITIS module of pytaxize"""
import os
from nose.tools import *
import unittest
import vcr
from pytaxize import itis

class ITIS(unittest.TestCase):

    @vcr.use_cassette('test/vcr_cassettes/itis_getacceptednamesfromtsn.yml')
    def test_itis_getacceptednamesfromtsn(self):
        "ITIS: getaccepednamesfromtsn"
        assert itis.getacceptednamesfromtsn('208527') == '208527'

    @vcr.use_cassette('test/vcr_cassettes/itis_getcommentdetailfromtsn.yml')
    def test_itis_getcommentdetailfromtsn(self):
        "ITIS: getcommentdetailfromtsn"
        comments =  itis.getcommentdetailfromtsn(tsn=180543)
        assert set(comments.keys()) == set(['commentator', 'comment', 'commtime',
                                         'updatedate', 'commid'])

    @vcr.use_cassette('test/vcr_cassettes/itis_searchbycommonname.yml')
    def test_itis_searchbycommonname(self):
        "ITIS: searchbycommonname"
        df = itis.searchbycommonname("grizzly")
        assert set(list(df.columns)) == set(['tsn', 'language', 'commonname'])

    @vcr.use_cassette('test/vcr_cassettes/tis_gethierarchyupfromtsn.yml')
    def test_itis_gethierarchyupfromtsn(self):
        "ITIS: gethierarchyupfromtsn"
        hierarchy = itis.gethierarchyupfromtsn(tsn = 36485)
        assert hierarchy[0]['rankName'] == 'Genus'

    def test_itis_getcommonnamesfromtsn(self):
        """
        Basic test of its getcommonnamesfromtsn
        """
        common_names = pytaxize.itis.getcommonnamesfromtsn(tsn=180543,
                                                       as_dataframe=False)
        assert set(common_names[1]) == set(['comname', 'lang', 'tsn'])

        common_names_df = pytaxize.itis.getcommonnamesfromtsn(tsn=180543,
                                                            as_dataframe=True)
        assert set(common_names_df.columns) == set(['comname', 'lang', 'tsn'])
