# -*- coding: utf-8 -*-

# pytaxize

'''
pytaxize library
~~~~~~~~~~~~~~~~~~~~~

pytaxize is a taxonomic toolkit for Python. Example usage:

Usage::

   import pytaxize
   pytaxize.col_children(name=["Apis"])
'''

from .refactor import *
from .tnrs import tnrs_resolve
from .gnr import gnr_datasources, gnr_resolve
from .gni import gni_parse, gni_search, gni_details
from .col import col_children, col_downstream, col_search
from .tax import names_list, vascan_search, gbif_parse, scrapenames
from .ids import Ids
from .itis import itis_ping, getacceptednamesfromtsn, getanymatchcount, getcommentdetailfromtsn, getcommonnamesfromtsn, getcoremetadatafromtsn, getcoveragefromtsn, getcredibilityratingfromtsn, getcredibilityratings, getcurrencyfromtsn, getdatedatafromtsn, getexpertsfromtsn, gettaxonomicranknamefromtsn, getfullhierarchyfromtsn, getfullrecordfromlsid, getfullrecordfromtsn, getgeographicdivisionsfromtsn, getgeographicvalues, getglobalspeciescompletenessfromtsn, gethierarchydownfromtsn, gethierarchyupfromtsn, getitistermsfromcommonname, getitisterms, getitistermsfromscientificname, itis_hierarchy, getjurisdictionaloriginfromtsn, getjurisdictionoriginvalues, getjurisdictionvalues, getkingdomnamefromtsn, getkingdomnames, getlastchangedate, getlsidfromtsn, getothersourcesfromtsn, getparenttsnfromtsn, getpublicationsfromtsn, getranknames, getrecordfromlsid, getreviewyearfromtsn, getscientificnamefromtsn, gettaxonauthorshipfromtsn, gettaxonomicranknamefromtsn, gettaxonomicusagefromtsn, gettsnbyvernacularlanguage, gettsnfromlsid, getunacceptabilityreasonfromtsn, getvernacularlanguages, searchbycommonname, searchbycommonnamebeginswith, searchbycommonnameendswith, itis_searchcommon, searchbyscientificname, searchforanymatch, searchforanymatchpaged
