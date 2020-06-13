# -*- coding: utf-8 -*-

# pytaxize

"""
pytaxize library
~~~~~~~~~~~~~~~~

pytaxize is a taxonomic toolkit for Python. Example usage:

Usage::

   from pytaxize import col
   col.col_children(name=["Apis"])
"""

__version__ = "0.6.94"
__title__ = "pytaxize"
__author__ = "Scott Chamberlain"
__license__ = "MIT"

from .gbif import parse
from .col import children, downstream, search
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
)
from .tax import names_list, vascan_search, scrapenames
from .taxo import taxo_datasources, taxo_resolve
from .ids import Ids
from .scicomm import sci2comm
