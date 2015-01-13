import sys
import requests
import pandas as pd
import json


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
    with_context='false', best_match_only='false', header_only='false', preferred_data_sources='false'):
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

    Usage:
    >>> import pytaxize
    >>> pytaxize.gnr_resolve('Helianthus annus')
    [{u'classification_path': u'', u'data_source_title': u'EOL', u'match_type': 1, u'score': 0.988, u'url': u'http://eol.org/pages/468106/names/synonyms', u'classification_path_ranks': u'', u'name_string': u'Helianthus annus', u'prescore': u'3|0|0', u'canonical_form': u'Helianthus annus', u'classification_path_ids': u'', u'local_id': u'468106', u'data_source_id': 12, u'taxon_id': u's_5106367', u'gni_uuid': u'f5674e32-00cc-57e3-b632-6a0b89fa4df4'}, {u'classification_path': u'|Helianthus annus', u'data_source_title': u'uBio NameBank', u'match_type': 1, u'score': 0.988, u'url': u'http://www.ubio.org/browser/details.php?namebankID=10130157', u'classification_path_ranks': u'kingdom|', u'name_string': u'Helianthus annus', u'global_id': u'urn:lsid:ubio.org:namebank:10130157', u'prescore': u'3|0|0', u'canonical_form': u'Helianthus annus', u'classification_path_ids': u'', u'local_id': u'urn:lsid:ubio.org:namebank:10130157', u'data_source_id': 169, u'taxon_id': u'102910884', u'gni_uuid': u'f5674e32-00cc-57e3-b632-6a0b89fa4df4'}, {u'classification_path': u'', u'data_source_title': u'EOL', u'match_type': 2, u'score': 0.988, u'url': u'http://eol.org/pages/468106', u'classification_path_ranks': u'', u'name_string': u'Helianthus annus L.', u'prescore': u'3|0|0', u'canonical_form': u'Helianthus annus', u'classification_path_ids': u'', u'local_id': u'468106', u'data_source_id': 12, u'taxon_id': u'20584982', u'gni_uuid': u'e757b3c1-421f-5bb9-a27f-d56259baaf3d'}]
    '''
    url = 'http://resolver.globalnames.org/name_resolvers'
    payload = {'names': names, 'data_source_ids': source, 'format': format, 'resolve_once': resolve_once,
               'with_context': with_context, 'best_match_only': best_match_only, 'header_only': header_only,
               'preferred_data_sources': preferred_data_sources}
    out = requests.get(url, params = payload)
    out.raise_for_status()
    result_json = out.json()
    try:
        data = result_json['data'][0]['results']
        return data
    except (KeyError, IndexError):
        raise NoResultException("GNR didn't return a result (names: %s)" % names)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
