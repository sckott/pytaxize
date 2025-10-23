"""Tests for ITIS module of pytaxize"""
import vcr

from pytaxize import itis


class TestITIS:
    @vcr.use_cassette("test/vcr_cassettes/itis_accepted_names.yml")
    def test_itis_accepted_names(self):
        "ITIS: accepted_names"
        assert itis.accepted_names("208527") == {}

    @vcr.use_cassette("test/vcr_cassettes/itis_comment_detail.yml")
    def test_itis_comment_detail(self):
        "ITIS: comment_detail"
        comments = itis.comment_detail(tsn=180543)
        assert isinstance(comments, list)
        assert isinstance(comments[0], dict)
        assert len(comments) == 2

    # @vcr.use_cassette("test/vcr_cassettes/itis_searchbycommonname.yml")
    # def test_itis_searchbycommonname(self):
    #     "ITIS: searchbycommonname"
    #     df = itis.searchbycommonname("grizzly")
    #     assert set(list(df.columns)) == set(["tsn", "language", "commonname"])

    # @vcr.use_cassette("test/vcr_cassettes/itis_gethierarchyupfromtsn.yml")
    # def test_itis_gethierarchyupfromtsn(self):
    #     "ITIS: gethierarchyupfromtsn"
    #     hierarchy = itis.gethierarchyupfromtsn(tsn=36485)
    #     assert hierarchy[0]["rankName"] == "Genus"

    @vcr.use_cassette("test/vcr_cassettes/itis_common_names.yml")
    def test_itis_common_names(self):
        "ITIS: common_names"
        common_names = itis.common_names(tsn=180543, as_dataframe=False)
        assert set(common_names[1]) == set(["commonName", "language", "tsn"])

    @vcr.use_cassette("test/vcr_cassettes/itis_common_names_dataframe.yml")
    def test_itis_common_names_dataframe(self):
        "ITIS: common_names"
        common_names = itis.common_names(tsn=180543, as_dataframe=False)
        assert set(common_names[1]) == set(["commonName", "language", "tsn"])
