import sys
import requests
import pandas as pd
import json
import time

class NoResultException(Exception):
    pass

def gnr_datasources(todf=True):
    '''
    Get data sources for the Global Names Resolver.

    Retrieve data sources used in Global Names Index, see
       http://gni.globalnames.org/ for information.

    :param todf: logical; Should a DataFrame be returned?

    Usage:
    # all data sources
    >>> import pytaxize
    >>> out = pytaxize.gnr_datasources()
    >>> out.head()
       id              title
    0   1  Catalogue of Life
    1   2        Wikispecies
    2   3               ITIS
    3   4               NCBI
    4   5     Index Fungorum

    # give me the id for EOL
    >>> out = pytaxize.gnr_datasources()
    >>> out.ix[out['title'] == 'EOL']
        id title
    11  12   EOL

    # Output json
    >>> pytaxize.gnr_datasources(False)
    '''
    url = "http://resolver.globalnames.org/data_sources.json"
    if(todf):
        out = requests.get(url)
        out.raise_for_status()
        out = out.json()
        data = []
        for i in range(len(out)):
            data.append([out[i]['id'],out[i]['title']])
        df = pd.DataFrame(data, columns=['id','title'])
    else:
        df = requests.get(url)
        df.raise_for_status()
        df = df.json()
    return df

def gnr_resolve(names='Homo sapiens', source=None, format='json', resolve_once='false',
    with_context='false', best_match_only='false', header_only='false', preferred_data_sources='false', http='get'):
    if names.__class__.__name__ != 'list':
        return _gnr_resolve(names, source, format, resolve_once,
    with_context, best_match_only, header_only, preferred_data_sources, http)
    
    maxlen = 1000
    #splitting list to smaller lists of size <= 1000
    names_sublists = [names[x:x+maxlen] for x in xrange(0, len(names), maxlen)]
    data = []
    for sublist in names_sublists:
        data.extend(_gnr_resolve(sublist, source, format, resolve_once,
    with_context, best_match_only, header_only, preferred_data_sources, http))
    
    return data

def _gnr_resolve(names='Homo sapiens', source=None, format='json', resolve_once='false',
    with_context='false', best_match_only='false', header_only='false', preferred_data_sources='false', http='get'):
    '''
    Uses the Global Names Resolver to resolve scientific names
    :param names: List of taxonomic names
    :param source: Source to pull from, one of x, y, z
    :param format: One of json or xml
    :param resolve_once: Logical, true or false
    :param with_context: Return context with taxonomic names
    :param best_match_only: Logical, if true (default) return the best match only
    :param header_only: Return header only, logical
    :param preferred_data_sources: Return only preferred data sources.
    :param http: The HTTP method to use, one of "get" or "post". Default="get"
    Usage:
    >>> import pytaxize
    >>> pytaxize.gnr_resolve('Helianthus annus')
    [{u'classification_path': u'', u'data_source_title': u'EOL', u'match_type': 1, u'score': 0.988, u'url': u'http://eol.org/pages/468106/names/synonyms', u'classification_path_ranks': u'', u'name_string': u'Helianthus annus', u'prescore': u'3|0|0', u'canonical_form': u'Helianthus annus', u'classification_path_ids': u'', u'local_id': u'468106', u'data_source_id': 12, u'taxon_id': u's_5106367', u'gni_uuid': u'f5674e32-00cc-57e3-b632-6a0b89fa4df4'}, {u'classification_path': u'|Helianthus annus', u'data_source_title': u'uBio NameBank', u'match_type': 1, u'score': 0.988, u'url': u'http://www.ubio.org/browser/details.php?namebankID=10130157', u'classification_path_ranks': u'kingdom|', u'name_string': u'Helianthus annus', u'global_id': u'urn:lsid:ubio.org:namebank:10130157', u'prescore': u'3|0|0', u'canonical_form': u'Helianthus annus', u'classification_path_ids': u'', u'local_id': u'urn:lsid:ubio.org:namebank:10130157', u'data_source_id': 169, u'taxon_id': u'102910884', u'gni_uuid': u'f5674e32-00cc-57e3-b632-6a0b89fa4df4'}, {u'classification_path': u'', u'data_source_title': u'EOL', u'match_type': 2, u'score': 0.988, u'url': u'http://eol.org/pages/468106', u'classification_path_ranks': u'', u'name_string': u'Helianthus annus L.', u'prescore': u'3|0|0', u'canonical_form': u'Helianthus annus', u'classification_path_ids': u'', u'local_id': u'468106', u'data_source_id': 12, u'taxon_id': u'20584982', u'gni_uuid': u'e757b3c1-421f-5bb9-a27f-d56259baaf3d'}]
    >>> pytaxize.gnr_resolve(['Helianthus annus','Poa annua'])
    '''
    url = 'http://resolver.globalnames.org/name_resolvers'
    payload = {'data_source_ids': source, 'format': format,
                'resolve_once': resolve_once, 'with_context': with_context,
                'best_match_only': best_match_only, 'header_only': header_only,
                'preferred_data_sources': preferred_data_sources}
    if names.__class__.__name__ == 'list':
        if len(names) > 300 and http == 'get':
            http = 'post'
        else:
            names = "|".join(names)
            payload['names'] = names
    else:
        payload['names'] = names
    if http == 'get':
        out = requests.get(url, params = payload)
        out.raise_for_status()
        result_json = out.json()
    else:
        if names.__class__.__name__ != 'list':
            out = requests.post(url, params = payload)
            out.raise_for_status()
            result_json = out.json()
        else:
            with open('names_list.txt', 'wb') as f:
                for name in names:
                    f.write(name+"\n")
            f.close()
            out = requests.post(url, params = payload, files = {'file': open('names_list.txt', 'rb')} )
            out.raise_for_status()
            result_json = out.json()
            while result_json['status'] == 'working':
                result_url = result_json['url']
                time.sleep(10)
                out = requests.get(url=result_url)
                result_json = out.json()

    data = []
    for each_result in result_json['data']:
        data.append( each_result['results'] if 'results' in each_result else [])
    if data == [[]]:
        sys.exit('No matching results to the query')
    return data
 
if __name__ == "__main__":
    import doctest
    doctest.testmod()
