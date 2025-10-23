import vcr

from pytaxize import taxo


class TestTaxosaurus:
    @vcr.use_cassette("test/vcr_cassettes/taxo_datasources.yml")
    def test_taxo_datasources(self):
        "taxo_datasources"
        res = taxo.taxo_datasources()
        assert isinstance(res, list)
        assert isinstance(res[0], dict)
        assert [z["sourceId"] for z in res] == ["NCBI", "iPlant_TNRS", "MSW3"]

    @vcr.use_cassette("test/vcr_cassettes/taxo_resolve.yml")
    def test_taxo_resolve(self):
        "taxo_resolve"
        res = taxo.taxo_resolve(query="Helianthus annus")
        assert isinstance(res, list)
        assert isinstance(res[0], list)
        assert isinstance(res[0][0], dict)
