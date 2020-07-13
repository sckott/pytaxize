from ..refactor import Refactor
from .format_helpers import _make_id


def eol_query_for_single_name(name):
    # will replace later with either a pre-made package
    # or with an implementation of EoL in taxize
    response = (
        Refactor(
            url="https://eol.org/api/search/1.0.json?q=%s&exact=true" % name,
            request="get",
        )
        .json()
        .get("results", {})
    )
    return response


def process_eol_response(list_of_response_dicts):
    extracted_ids = list(
        map(
            lambda x: _make_id(x.get("id", None), None, None, "eol"),
            list_of_response_dicts,
        )
    )
    return extracted_ids