import vcr

from pytaxize.children import Children


class TestChildren:
    @vcr.use_cassette("test/vcr_cassettes/children_itis.yml")
    def test_children_itis(self):
        "Children: itis"
        x = Children([179913, 174321, 9999999])
        assert isinstance(x, Children)
        assert x.ids == [179913, 174321, 9999999]
        assert len(x.ids) == 3
        res = x.itis()
        assert len(x.ids) == 3
        assert isinstance(res, dict)
        assert isinstance(res[179913], list)
        assert isinstance(res[179913][0], dict)
