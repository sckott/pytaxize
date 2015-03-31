"""Tests for TNRS module of pytaxize"""
import os
import pytaxize

a = [{u'selected': True, u'infraspecific2Rank': u'', u'family': u'Asteraceae',
     u'infraspecific1EpithetScore': u'', u'infraspecific1Rank': u'',
     u'nameScientific': u'Helianthus annuus', u'speciesMatched': u'annuus',
     u'authorScore': u'', u'group': u'0', u'author': u'', u'acceptance': u'No opinion',
     u'authorAttributed': u'L.', u'unmatched': u"'", u'nameSubmitted': u"Helianthus annus'",
     u'genusScore': u'1', u'matchedFamilyScore': u'', u'infraspecific2EpithetScore': u'',
     u'infraspecific1Epithet': u'', u'infraspecific2Epithet': u'', u'familySubmitted': u'',
     u'epithet': u'annuus', u'acceptedName': u'Helianthus annuus', u'overall': u'0.8694502693699',
     u'speciesMatchedScore': u'0.83333333333333', u'matchedFamily': u'',
     u'acceptedNameUrl': u'http://www.tropicos.org/Name/2700851',
     u'epithetScore': u'0.83333333333333', u'annotation': u'',
     u'url': u'http://www.tropicos.org/Name/2700851', u'scientificScore': u'0.9694502693699',
     u'acceptedAuthor': u'L.', u'genus': u'Helianthus'},
     {u'selected': False, u'infraspecific2Rank': u'', u'family': u'Violaceae',
     u'infraspecific1EpithetScore': u'', u'infraspecific1Rank': u'',
     u'nameScientific': u'Hybanthus nanus', u'speciesMatched': u'nanus',
     u'authorScore': u'', u'group': u'0', u'author': u'', u'acceptance': u'No opinion',
     u'authorAttributed': u'(A. St.-Hil.) Paula-Souza', u'unmatched': u"'",
     u'nameSubmitted': u"Helianthus annus'", u'genusScore': u'0.7',
     u'matchedFamilyScore': u'', u'infraspecific2EpithetScore': u'',
     u'infraspecific1Epithet': u'', u'infraspecific2Epithet': u'',
     u'familySubmitted': u'', u'epithet': u'nanus', u'acceptedName': u'Hybanthus nanus',
     u'overall': u'0.67149326622765', u'speciesMatchedScore': u'0.8',
     u'matchedFamily': u'', u'acceptedNameUrl': u'http://www.tropicos.org/Name/100000197',
     u'epithetScore': u'0.8', u'annotation': u'', u'url': u'http://www.tropicos.org/Name/100000197',
     u'scientificScore': u'0.77149326622765', u'acceptedAuthor': u'(A. St.-Hil.) Paula-Souza',
     u'genus': u'Hybanthus'}]

def test_tnrs_resolve():
    " Basic test for tnrs"
    assert a == pytaxize.tnrs_resolve('Helianthus annus')