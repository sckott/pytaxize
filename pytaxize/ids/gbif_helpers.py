from pygbif import species

from .format_helpers import _make_id


def gbif_query_for_single_name(name, rank):
    response = species.name_usage(name=name, rank=rank.upper())["results"]
    return response


def process_gbif_response(list_of_response_dicts, rank):
    key = rank + "Key"
    extracted_ids = list(
        map(
            lambda x: _make_id(x.get(key, None), x.get(rank, None), rank, "gbif"),
            list_of_response_dicts,
        )
    )
    return extracted_ids
