from ..refactor import Refactor
from .format_helpers import _make_id


def eol_search_query_for_single_name(name):
    # will replace later with either a pre-made package
    # or with an implementation of EoL in taxize
    response = (
        Refactor(
            url="https://eol.org/api/search/1.0.json",
            request="get",
            payload={'q':name,'exact':True}
        )
        .json()
        .get("results", {})
    )
    return response


def eol_taxa_query(list_of_ids):
    return list(map(eol_taxa_query_for_single_PageID, list_of_ids))


def eol_taxa_query_for_single_PageID(pid):
    # will replace later with either a pre-made package
    # or with an implementation of EoL in taxize
    response = (
        Refactor(url="https://eol.org/api/pages/1.0/%s.json" % pid, request="get",)
        .json()
        .get("taxonConcept", {})
        .get("taxonConcepts", {})
    )
    response = list(map(lambda x: {**x, "page_id": pid}, response))
    return response


def process_eol_search_response(name_response_tuple):
    user_input_name, list_of_response_dicts = name_response_tuple
    user_input_name = user_input_name.lower()
    extracted_ids = list(
        filter(
            lambda page_dict: user_input_name in page_dict["title"].lower(),
            list_of_response_dicts,
        )
    )
    extracted_ids = list(
        map(lambda page_dict: page_dict.get("id", None), list_of_response_dicts,)
    )
    extracted_ids = list(filter(lambda id_: id_ is not None, extracted_ids))
    return extracted_ids


def process_list_of_taxa_details(list_of_responses):
    useful_data = list(
        map(
            lambda x: {
                **_make_id(
                    x.get("identifier", ""),
                    x.get("scientificName", ""),
                    x.get("taxonRank", None),
                    "eol",
                ),
                "page_id": x.get("page_id", ""),
            },
            list_of_responses,
        )
    )
    for item in useful_data:
        item["uri"] = "https://eol.org/pages/" + str(item["page_id"])
    return useful_data
