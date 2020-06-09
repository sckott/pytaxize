"""Tests for GNR module of pytaxize"""
import os
from nose.tools import *
import unittest
import vcr
from pytaxize import gn

# expected results
exp1 = {
    u"canonical_form": u"Helianthus annus",
    u"classification_path": u"",
    u"classification_path_ids": u"",
    u"classification_path_ranks": u"",
    u"data_source_id": 12,
    u"data_source_title": u"EOL",
    u"edit_distance": 0,
    u"gni_uuid": u"f5674e32-00cc-57e3-b632-6a0b89fa4df4",
    u"imported_at": u"2012-05-08T02:42:50Z",
    u"local_id": u"468106",
    u"match_type": 1,
    u"match_value": u"Exact string match",
    u"name_string": u"Helianthus annus",
    u"prescore": u"3|0|0",
    u"score": 0.988,
    u"taxon_id": u"s_5106367",
    u"url": u"http://eol.org/pages/468106/names/synonyms",
}


class Gnr(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/gnr_resolve.yml")
    def test_gnr_resolve(self):
        "gnr_resolve"
        assert exp1 == gn.gnr_resolve("Helianthus annus")[0][0]


# def test_gnr_resolve_remove_temporary_file():
#   """test if delete temporary name list file in gnr_resolve"""
#   with open('test/data/species_list.txt', 'rb') as f:
#     name_list = f.readlines()
#   pytaxize.gnr_resolve( name_list[0:301] )
#   assert os.path.isfile('names_list.txt') == False

# def test_gnr_resolve_larger_1000():
#   """test if work well when queried number larger than 1000"""
#   with open('test/data/species_list.txt', 'rb') as f:
#     name_list = f.readlines()
#   assert len(pytaxize.gnr_resolve( name_list )) == len(name_list)
