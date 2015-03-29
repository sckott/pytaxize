import sys
import requests
import json

class NoResultException(Exception):
    pass

def tnrs_resolve(names='Homo sapiens', retrieve='all'):
    '''
    Uses the Global Names Resolver to resolve scientific names
    :param names: List of taxonomic names
    :param retrieve: all OR best
    Usage:
    >>> import pytaxize
    >>> pytaxize.tnrs_resolve('Helianthus annus')
    [{u'selected': True, u'infraspecific2Rank': u'', u'family': u'Asteraceae', u'infraspecific1EpithetScore': u'', u'infraspecific1Rank': u'', u'nameScientific': u'Helianthus annuus', u'speciesMatched': u'annuus', u'authorScore': u'', u'group': u'0', u'author': u'', u'acceptance': u'No opinion', u'authorAttributed': u'L.', u'unmatched': u"'", u'nameSubmitted': u"Helianthus annus'", u'genusScore': u'1', u'matchedFamilyScore': u'', u'infraspecific2EpithetScore': u'', u'infraspecific1Epithet': u'', u'infraspecific2Epithet': u'', u'familySubmitted': u'', u'epithet': u'annuus', u'acceptedName': u'Helianthus annuus', u'overall': u'0.8694502693699', u'speciesMatchedScore': u'0.83333333333333', u'matchedFamily': u'', u'acceptedNameUrl': u'http://www.tropicos.org/Name/2700851', u'epithetScore': u'0.83333333333333', u'annotation': u'', u'url': u'http://www.tropicos.org/Name/2700851', u'scientificScore': u'0.9694502693699', u'acceptedAuthor': u'L.', u'genus': u'Helianthus'}, {u'selected': False, u'infraspecific2Rank': u'', u'family': u'Violaceae', u'infraspecific1EpithetScore': u'', u'infraspecific1Rank': u'', u'nameScientific': u'Hybanthus nanus', u'speciesMatched': u'nanus', u'authorScore': u'', u'group': u'0', u'author': u'', u'acceptance': u'No opinion', u'authorAttributed': u'(A. St.-Hil.) Paula-Souza', u'unmatched': u"'", u'nameSubmitted': u"Helianthus annus'", u'genusScore': u'0.7', u'matchedFamilyScore': u'', u'infraspecific2EpithetScore': u'', u'infraspecific1Epithet': u'', u'infraspecific2Epithet': u'', u'familySubmitted': u'', u'epithet': u'nanus', u'acceptedName': u'Hybanthus nanus', u'overall': u'0.67149326622765', u'speciesMatchedScore': u'0.8', u'matchedFamily': u'', u'acceptedNameUrl': u'http://www.tropicos.org/Name/100000197', u'epithetScore': u'0.8', u'annotation': u'', u'url': u'http://www.tropicos.org/Name/100000197', u'scientificScore': u'0.77149326622765', u'acceptedAuthor': u'(A. St.-Hil.) Paula-Souza', u'genus': u'Hybanthus'}]
    >>> pytaxize.tnrs_resolve(['Helianthus annus','Poa annua'])
    '''
    url = 'http://tnrs.iplantc.org/tnrsm-svc/matchNames'
    if(names.__class__.__name__ == 'list'):
        names = ",".join(names)
    else:
        pass
    payload = {'retrieve': retrieve, 'names': names }
    out = requests.get(url, params = payload)
    out.raise_for_status()
    result_json = out.json()

    data = []
    #List to accumulate results for each queried name
    single_list=[]
    index = result_json['items'][0]['group']
    for each_result in result_json['items']:
        if each_result['group'] == index:
            single_list.append(each_result)
        else:
            data.append(single_list)
            single_list = []
            single_list.append(each_result)
            index = each_result['group']
    data.append(single_list)
    return data

if __name__ == "__main__":
    import doctest
    doctest.testmod()
