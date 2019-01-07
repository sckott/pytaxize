"""Tests for ITIS module of pytaxize"""
import os
import pytaxize

from vcr_unittest import VCRTestCase

class ITIS(VCRTestCase):
    def test_itis_getacceptednamesfromtsn(self):
        "Basic test of its getaccepednamesfromtsn"
        assert pytaxize.itis.getacceptednamesfromtsn('208527') == '208527'

    def test_itis_getcommentdetailfromtsn(self):
        "Basic test of its getcommentdetailfromtsn"
        comments =  pytaxize.itis.getcommentdetailfromtsn(tsn=180543)
        assert set(comments.keys()) == set(['commentator', 'comment', 'commtime',
                                         'updatedate', 'commid'])

    def test_itis_searchbycommonname(self):
        "Basic test of its searchbycommonname"
        df = pytaxize.searchbycommonname("grizzly")
        assert set(list(df.columns)) == set(['tsn', 'language', 'commonname'])

    def test_itis_gethierarchyupfromtsn(self):
        "Basic test of its gethierarchyupfromtsn"
        hierarchy = pytaxize.gethierarchyupfromtsn(tsn = 36485)
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
