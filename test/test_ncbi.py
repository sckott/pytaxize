import vcr

from pytaxize import ncbi


class TestNcbi:
    @vcr.use_cassette("test/vcr_cassettes/ncbi_search.yml",
      filter_query_parameters=['api_key'])
    def test_ncbi_search(self):
        "ncbi.search"
        x = ncbi.search(sci_com = "Apis")
        assert isinstance(x, dict)
        assert list(x.keys()) == ["Apis"]
        assert isinstance(x['Apis'], list)
        assert isinstance(x['Apis'][0], dict)
        assert x['Apis'][0]['ScientificName'] == "Apis"
        assert x['Apis'][0]['TaxId'] == "7459"
