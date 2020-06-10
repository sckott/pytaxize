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

__version__ = "0.6.91"
__title__ = "pytaxize"
__author__ = "Scott Chamberlain"
__license__ = "MIT"

from .gbif import parse
from .col import children, downstream, search
from .gn import gni_parse, gni_search, gni_details
from .gn import gnr_datasources, gnr_resolve
from .ncbi import search
from .itis import (
    getacceptednamesfromtsn,
    getanymatchcount,
    getcommentdetailfromtsn,
    getcommonnamesfromtsn,
    getcoremetadatafromtsn,
    getcoveragefromtsn,
    getcredibilityratingfromtsn,
    getcredibilityratings,
    getcurrencyfromtsn,
    getdatedatafromtsn,
    getexpertsfromtsn,
    gettaxonomicranknamefromtsn,
    getfullhierarchyfromtsn,
    getfullrecordfromlsid,
    getfullrecordfromtsn,
    getgeographicdivisionsfromtsn,
)
from .tax import names_list, vascan_search, scrapenames
from .taxo import taxo_datasources, taxo_resolve
from .ids import Ids
