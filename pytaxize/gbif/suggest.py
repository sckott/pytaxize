import json
import warnings
from pytaxize.refactor import Refactor
from .constants import gbif_suggest_url

"""
    Get a list of suggested names from GBIF.

    Author Daniel Davies (dd16785@bristol.ac.uk)
    References https://www.gbif.org/developer/species
    
    Usage
        
        from pytaxize import gbif
        response = gbif.suggest(
            name         :: string,
            rank         :: string (OPTIONAL),
            as_dataframe :: bool (OPTIONAL) 
        )
"""


def suggest(name, rank=None, as_dataframe=False):
    validate_suggest_inputs(name, rank)
    request_url = prepare_suggested_names_url(name, rank)
    response = Refactor(request_url, request="get").json()
    if as_dataframe:
        return transform_to_frame_if_available(response)
    return response


def validate_suggest_inputs(name, rank):
    if name is None or not isinstance(name, str):
        raise ValueError(
            "Input name must be a string, describing a single species."
        )

    if rank is not None and not isinstance(rank, str):
        raise ValueError(
            "Input rank must be a string, describing a proposed taxonomic rank."
        )


def prepare_suggested_names_url(name, rank):
    base_url = gbif_suggest_url + "?q=" + name
    if rank is not None:
        base_url += "&rank=" + rank
    return base_url


def transform_to_frame_if_available(response):
    try:
        import pandas as pd

        return pd.DataFrame(response)
    except ImportError:
        warnings.warn("Pandas library not installed, falling back to json output")
        return response
