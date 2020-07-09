from pytaxize import gbif
import vcr
import unittest
import pytest
import os


def pandas_installed():
    return False
    try:
        import pandas as pd

        return True
    except:
        return False


class GbifTest(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/gbif_suggest.yml")
    @pytest.mark.skipif(
        "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
        reason="Skipping this test on Travis CI.",
    )
    def test_gbif_suggest_basic_normal_usage(self):
        respose = gbif.suggest(name="puma con", as_dataframe=False)
        assert isinstance(respose, list)
        required_keys_per_record = ["key", "scientificName", "rank"]
        assert all(
            map(
                lambda indiv_record: all(
                    [key in indiv_record for key in required_keys_per_record]
                ),
                respose,
            )
        )

    @vcr.use_cassette("test/vcr_cassettes/gbif_suggest.yml")
    @pytest.mark.skipif(
        "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
        reason="Skipping this test on Travis CI.",
    )
    def test_gbif_suggest_basic_dataframe(self):
        if pandas_installed():
            import pandas as pd

            respose = gbif.suggest(name="puma con", as_dataframe=True)
            assert isinstance(respose, pd.DataFrame)
            required_keys_per_record = ["key", "scientificName", "rank"]

            assert all(
                map(lambda indiv_key: indiv_key in respose, required_keys_per_record)
            )

    @pytest.mark.skipif(
        "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
        reason="Skipping this test on Travis CI.",
    )
    def test_invalid_name_input(self):
        with pytest.raises(ValueError):
            gbif.suggest(name=["puma con"])

        with pytest.raises(ValueError):
            gbif.suggest(name=None)

        with pytest.raises(ValueError):
            gbif.suggest(name=1, rank="species", as_dataframe=False)

    @pytest.mark.skipif(
        "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
        reason="Skipping this test on Travis CI.",
    )
    def test_invalid_rank_input(self):
        with pytest.raises(ValueError):
            gbif.suggest(name="puma con", rank=["species"])

        with pytest.raises(ValueError):
            gbif.suggest(name="puma con", rank=1)
