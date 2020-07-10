# -*- coding: utf-8 -*-

# pytaxize

"""
pytaxize library
~~~~~~~~~~~~~~~~

pytaxize is a taxonomic toolkit for Python. Example usage:
"""

__version__ = "0.7.1"
__title__ = "pytaxize"
__author__ = "Scott Chamberlain"
__license__ = "MIT"

from .col import children, search
from .gn import gni
from .gn import gnr
from .ncbi import search
from .itis import (
    accepted_names,
    any_match_count,
    comment_detail,
    common_names,
    core_metadata,
    coverage,
    credibility_rating,
    credibility_ratings,
    currency,
    date_data,
    experts,
    rank_name,
    hierarchy_full,
    full_record,
    geographic_divisions,
    geographic_values,
    hierarchy_down,
    hierarchy_up,
    terms,
    global_species_completeness,
    jurisdictional_origin,
    jurisdiction_origin_values,
    jurisdiction_values,
)
from .tax import names_list, vascan_search, scrapenames
from .taxo import taxo_datasources, taxo_resolve
from .ids import Ids
from .children import Children
from .scicomm import sci2comm
