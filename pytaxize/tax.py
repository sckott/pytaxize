import sys
import requests
from BeautifulSoup import BeautifulSoup as Soup
from lxml import etree
import pandas as pd
import re
import json

class NoResultException(Exception):
    pass

def itis_ping():
    '''
    Ping the ITIS API

    Usage: 
    pytaxize.itis_ping()
    '''
    r = requests.get('http://www.itis.gov/ITISWebService/services/ITISService/getDescription')
    r.raise_for_status()
    return r.text

def gnr_datasources(todf=True):
    '''
    Get data sources for the Global Names Resolver.

    Retrieve data sources used in Global Names Index, see 
       http://gni.globalnames.org/ for information. 

    @param todf logical; Should a DataFrame be returned?

    Usage:
    # all data sources
    pytaxize.gnr_datasources() 

    # give me the id for EOL
    out <- pytaxize.gnr_datasources()
    out[out$title == "EOL", "id"]

    # Fuzzy search for sources with the word zoo
    out <- pytaxize.gnr_datasources()
    out[agrep("zoo", out$title, ignore.case = TRUE), ]

    # Output as a list
    pytaxize.gnr_datasources(FALSE)
    '''
    url = "http://resolver.globalnames.org/data_sources.json"
    if(todf):
        out = requests.get(url).json()
        out.raise_for_status()
        data = []
        for i in range(len(out)):
            data.append([out[i]['id'],out[i]['title']])
        df = pd.DataFrame(data, columns=['id','title'])
    else:
        df = requests.get(url)
        df.raise_for_status()
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
    pytaxize.gnr_resolve('Helianthus annus')
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
    except KeyError, IndexError:
        raise NoResultException("GNR didn't return a result (names: %s)" % names)

def gni_parse(names):
    '''
    Uses the Global Names Index to parse scientific names
    
    :param names: List of scientific names.

    Usage: 
    pytaxize.gni_parse(names = ['Cyanistes caeruleus','Helianthus annuus'])
    '''
    url = 'http://gni.globalnames.org/parsers.json'
    names = '|'.join(names)
    out = requests.get(url, params = {'names': names})
    out.raise_for_status()
    return out.json()

def gni_search(search_term='ani*', per_page=30, page=1):
    '''
    Search for names against the Global names index

    :param search_term: Search term
    :param per_page: Items to return per page
    :param page: Page to return

    Usage: 
    pytaxize.gni_search(search_term = 'ani*')
    '''
    url = 'http://gni.globalnames.org/name_strings.json'
    out = requests.get(url, params = {'search_term': search_term, 'per_page': per_page, 'page': page})
    return out.json()

def gni_details(id=17802847, all_records=1):
    '''
    E.g,: 
    pytaxize.gni_details(id = 17802847)
    '''
    url = 'http://gni.globalnames.org/name_strings/'
    mylist = [url, str(id), '.json']
    url2 = ''.join(mylist)
    out = requests.get(url2, params = {'all_records': all_records})
    out.raise_for_status()
    return out.json()

def names_list(rank = 'genus', size = 10):
    '''
    Get a random vector of species names.
    
    :param rank: Taxonomic rank, one of species, genus (default), family, order. 
    :param size: Number of names to get. Maximum depends on the rank.

    Usage:
    pytaxize.names_list()
    pytaxize.names_list('species')
    pytaxize.names_list('family')
    pytaxize.names_list('order')
    pytaxize.names_list('order', 2)
    pytaxize.names_list('order', 15)
    '''
    if(rank == 'species'):
        dat = pd.read_csv("plantNames.csv", header=False)
        dat2 = dat['names'][:size]
        return [x for x in dat2]
    if(rank == 'genus'):
        dat = pd.read_csv("plantGenusNames.csv", header=False)
        dat2 = dat['names'][:size]
        return [x for x in dat2]
    if(rank == 'family'):
        dat = pd.read_csv("apg_families.csv", header=False)
        dat2 = dat['this'][:size]
        return [x for x in dat2]
    if(rank == 'order'):
        dat = pd.read_csv("apg_orders.csv", header=False)
        dat2 = dat['this'][:size]
        return [x for x in dat2]
    else:
        return 'Pass in to rank one of species, genus, family, or order'

def vascan_search(q, format='json', raw=False):
    '''
    Search the CANADENSYS Vascan API.
    
    :param q: Taxonomic rank, one of species, genus (default), family, order. 
    :param format: Number of names to get. Maximum depends on the rank.
    :param raw: Raw data or not (default)
    :param callopts: Further args passed to request

    Usage:
    pytaxize.vascan_search(q = ["Helianthus annuus"])
    pytaxize.vascan_search(q = ["Helianthus annuus"], raw=True)
    pytaxize.vascan_search(q = ["Helianthus annuus", "Crataegus dodgei"], raw=True)

    # format type
    ## json
    c = pytaxize.vascan_search(q = ["Helianthus annuus"], format="json", raw=True)
    c.json()

    ## xml
    d = pytaxize.vascan_search(q = ["Helianthus annuus"], format="xml", raw=True)
    print(d.prettify())

    # lots of names, in this case 50
    splist = pytaxize.names_list(rank='species', size=50)
    pytaxize.vascan_search(q = splist)
    '''
    if(format == 'json'):
        url = "http://data.canadensys.net/vascan/api/0.1/search.json"
    else:
        url = "http://data.canadensys.net/vascan/api/0.1/search.xml"

    if(len(q) > 1):
        query = "\n".join(q)
        payload = {'q': query}
        out = requests.post(url, data=payload)
        out.raise_for_status()
        if(format == 'json'):
            if(raw):
                return out.text
            else:
                return out.json()
        else:
            return out.text
    else:
        payload = {'q': q}
        out = requests.get(url, params = payload)
        out.raise_for_status()
        if(format == 'json'):
            if(raw):
                return out.text
            else:
                return out.json()
        else:
            return out.text

def col_children(name = None, id = None, format = None, start = None, checklist = None):
    '''
    Search Catalogue of Life for for direct children of a particular taxon.

    :param name: The string to search for. Only exact matches found the name given 
        will be returned, unless one or wildcards are included in the search 
        string. An * (asterisk) character denotes a wildcard; a % (percentage) 
        character may also be used. The name must be at least 3 characters long, 
        not counting wildcard characters.
    :param id: The record ID of the specific record to return (only for scientific 
        names of species or infraspecific taxa)
    :param format: format of the results returned. Valid values are format=xml and 
        format=php; if the format parameter is omitted, the results are returned 
        in the default XML format. If format=php then results are returned as a 
        PHP array in serialized string format, which can be converted back to an 
        array in PHP using the unserialize command
    :param start: The first record to return. If omitted, the results are returned 
        from the first record (start=0). This is useful if the total number of 
        results is larger than the maximum number of results returned by a single 
        Web service query (currently the maximum number of results returned by a 
        single query is 500 for terse queries and 50 for full queries).
    :param checklist: The year of the checklist to query, if you want a specific 
        year's checklist instead of the lastest as default (numeric).
    Details
    You must provide one of name or id. The other parameters (format and start) are 
    optional. Returns A list of data.frame's.
    
    Usage
    # A basic example
    pytaxize.col_children(name=["Apis"])

    # An example where there is no classification, results in data.frame with no rows
    pytaxize.col_children(id=[15669061])

    # Use a specific year's checklist
    pytaxize.col_children(name=["Apis"], checklist="2012")
    pytaxize.col_children(name=["Apis"], checklist="2009")

    # Pass in many names or many id's
    out = pytaxize.col_children(name=["Buteo","Apis","Accipiter"], checklist="2012")
    # get just one element in list of output
    out[0] 
    # or combine to one DataFrame
    import pandas as pd
    pd.concat(out)

    # or pass many id's
    out = pytaxize.col_children(id=[15669061,15700333,15638488])
    # combine to one DataFrame
    import pandas as pd
    pd.concat(out) 
    '''

    def func(x, y):
        url = "http://www.catalogueoflife.org/col/webservice"

        if(checklist.__class__.__name__ == 'NoneType'):
            pass
        else:
            if(checklist in ['2012','2011','2010']):
                url = re.sub("col", "annual-checklist/" + checklist, url)
            else:
                url = "http://www.catalogueoflife.org/annual-checklist/year/webservice"
                url = re.sub("year", checklist, url)
        
        payload = {'name':x, 'id':y, 'format':format, 'response':"full", 'start':start}
        out = requests.get(url, params = payload)
        out.raise_for_status()
        xmlparser = etree.XMLParser()
        tt = etree.fromstring(out.content, xmlparser)
        childtaxa = tt.xpath('//child_taxa//taxon')
        outlist = []
        for i in range(len(childtaxa)):
            tt_ = childtaxa[i].getchildren()
            outlist.append([x.text for x in tt_[:3]])
        df = pd.DataFrame(outlist, columns=['id','name','rank'])
        return df

    if(id.__class__.__name__ == 'NoneType'):
        temp = []
        for i in range(len(name)):
            ss = func(name[i], None)
            temp.append(ss)
        return temp
    else: 
        temp = []
        for i in range(len(id)):
            ss = func(None, id[i])
            temp.append(ss)
        return temp

def gbif_parse(scientificname):
    '''
    Parse taxon names using the GBIF name parser.

    :param scientificname: A character vector of scientific names.
    Returns a DataFrame containing fields extracted from parsed 
    taxon names. Fields returned are the union of fields extracted from
    all species names in scientificname

    Author John Baumgartner (johnbb@@student.unimelb.edu.au)
    References http://dev.gbif.org/wiki/display/POR/Webservice+API, 
    http://tools.gbif.org/nameparser/api.do
    
    Usage:
    pytaxize.gbif_parse(scientificname=['x Agropogon littoralis'])
    pytaxize.gbif_parse(scientificname=['Arrhenatherum elatius var. elatius', 
                 'Secale cereale subsp. cereale', 'Secale cereale ssp. cereale',
                 'Vanessa atalanta (Linnaeus, 1758)'])
    '''
    url = "http://apidev.gbif.org/parser/name"
    headers = {'content-type': 'application/json'}
    tt = requests.post(url, data=json.dumps(scientificname), headers=headers)
    tt.raise_for_status()
    res = pd.DataFrame(tt.json())
    return res