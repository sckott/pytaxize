"""Tests for UBIO module of pytaxize"""
import os
import pytaxize

a = {'fullNameString': {0: 'Q2VyeWxvbiBlbGVwaGFudA=='}, 'rankID': {0: '24'},
     'nameString': {0: 'Q2VyeWxvbiBlbGVwaGFudA=='},
     'packageName': {0: 'Cerylonidae'}, 'packageID': {0: '80'},
     'rankName': {0: 'species'}, 'basionymunit': {0: '6938660'},
     'namebankID': {0: '6938660'}}

def test_ubio_search():
    assert a == pytaxize.ubio_search(searchName = 'elephant', sci = 1, vern = 0).to_dict()