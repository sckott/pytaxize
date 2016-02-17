import sys
import requests
import json
from pytaxize.refactor import Refactor

class NoResultException(Exception):
    pass

def tnrs_resolve(names='Homo sapiens', retrieve='all'):
    '''
    Uses the Global Names Resolver to resolve scientific names

    :param names: List of taxonomic names
    :param retrieve: all OR best

    Usage::

        import pytaxize
        pytaxize.tnrs_resolve('Helianthus annus')
        pytaxize.tnrs_resolve(['Helianthus annus','Poa annua'])
    '''
    url = 'http://tnrs.iplantc.org/tnrsm-svc/matchNames'
    if(names.__class__.__name__ == 'list'):
        names = ",".join(names)
    else:
        pass
    payload = {'retrieve': retrieve, 'names': names }
    result_json = Refactor(url, payload, request='get').json()

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
