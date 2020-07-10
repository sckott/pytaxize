"""Tests for GNR module of pytaxize"""
import os
from nose.tools import *
import unittest
import vcr
from pytaxize import gn

# expected results
exp1 = {
    "data_source_id": 169,
    "data_source_title": "uBio NameBank",
    "gni_uuid": "f5674e32-00cc-57e3-b632-6a0b89fa4df4",
    "name_string": "Helianthus annus",
    "canonical_form": "Helianthus annus",
    "classification_path": "|Helianthus annus",
    "classification_path_ranks": "kingdom|",
    "classification_path_ids": "",
    "taxon_id": "102910884",
    "local_id": "urn:lsid:ubio.org:namebank:10130157",
    "global_id": "urn:lsid:ubio.org:namebank:10130157",
    "edit_distance": 0,
    "url": "http://www.ubio.org/browser/details.php?namebankID=10130157",
    "imported_at": "2013-05-31T20:12:19Z",
    "match_type": 1,
    "match_value": "Exact string match",
    "prescore": "3|0|0",
    "score": 0.988,
}


class Gnr(unittest.TestCase):
    @vcr.use_cassette("test/vcr_cassettes/gn_resolve.yml")
    def test_gnr_resolve(self):
        "gn.resolve"
        assert exp1 == gn.resolve("Helianthus annus")[0][0]


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
