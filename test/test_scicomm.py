import vcr

from pytaxize import scicomm


class TestSciComm:
    @vcr.use_cassette("test/vcr_cassettes/sci2comm_str_ncbi.yml",
      filter_query_parameters=['api_key'])
    def test_sci2comm_str_ncbi(self):
        "sci2comm/str/ncbi"
        x = "Helianthus annuus"
        res = scicomm.sci2comm(x)
        assert isinstance(res, dict)
        assert set(res.keys()) == {x}
