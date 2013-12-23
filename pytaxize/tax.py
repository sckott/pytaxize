import sys
import requests
from lxml import etree
import pandas as pd
import re
import json
from simplejson import JSONDecodeError

class NoResultException(Exception):
    pass

def itis_ping():
    '''
    Ping the ITIS API

    Usage:
    >>> import pytaxize
    >>> pytaxize.itis_ping()
    u'<ns:getDescriptionResponse xmlns:ns="http://itis_service.itis.usgs.gov"><ns:return xmlns:ax21="http://data.itis_service.itis.usgs.gov/xsd" xmlns:ax26="http://itis_service.itis.usgs.gov/xsd" xmlns:ax23="http://metadata.itis_service.itis.usgs.gov/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax26:SvcDescription"><ax26:description>This is the ITIS Web Service, providing access to the data behind www.itis.gov. The database contains 641,468 scientific names (486,232 of them valid/accepted) and 118,145 common names.</ax26:description></ns:return></ns:getDescriptionResponse>'
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
    except KeyError, IndexError:
        raise NoResultException("GNR didn't return a result (names: %s)" % names)

def gni_parse(names):
    '''
    Uses the Global Names Index to parse scientific names
    
    :param names: List of scientific names.

    Usage: 
    >>> import pytaxize
    >>> pytaxize.gni_parse(names = ['Cyanistes caeruleus','Helianthus annuus'])
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
    >>> import pytaxize
    >>> pytaxize.gni_search(search_term = 'ani*')
    '''
    url = 'http://gni.globalnames.org/name_strings.json'
    out = requests.get(url, params = {'search_term': search_term, 'per_page': per_page, 'page': page})
    out.raise_for_status()
    return out.json()

def gni_details(id=17802847, all_records=1):
    '''
    Usage: 
    >>> import pytaxize
    >>> pytaxize.gni_details(id = 17802847)
    '''
    url = 'http://gni.globalnames.org/name_strings/'
    mylist = [url, str(id), '.json']
    url2 = ''.join(mylist)
    out = requests.get(url2, params = {'all_records': all_records})
    out.raise_for_status()
    try:
        data = out.json()
        return data
    except JSONDecodeError:
        raise NoResultException("GNI didn't return a result (id: %s)" % id)

def names_list(rank = 'genus', size = 10):
    '''
    Get a random vector of species names.
    
    :param rank: Taxonomic rank, one of species, genus (default), family, order. 
    :param size: Number of names to get. Maximum depends on the rank.

    Usage:
    >>> import pytaxize
    >>> pytaxize.names_list()
    >>> pytaxize.names_list('species')
    >>> pytaxize.names_list('family')
    >>> pytaxize.names_list('order')
    >>> pytaxize.names_list('order', 2)
    >>> pytaxize.names_list('order', 15)
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
    >>> import pytaxize
    >>> pytaxize.vascan_search(q = ["Helianthus annuus"])
    >>> pytaxize.vascan_search(q = ["Helianthus annuus"], raw=True)
    >>> pytaxize.vascan_search(q = ["Helianthus annuus", "Crataegus dodgei"], raw=True)

    # format type
    ## json
    >>> pytaxize.vascan_search(q = ["Helianthus annuus"], format="json", raw=True)
    u'{"apiVersion":"0.1","results":[{"searchedTerm":"Helianthus annuus","numMatches":1,"matches":[{"taxonID":3189,"scientificName":"Helianthus annuus Linnaeus","scientificNameAuthorship":"Linnaeus","canonicalName":"Helianthus annuus","taxonRank":"species","taxonomicAssertions":[{"acceptedNameUsage":"Helianthus annuus Linnaeus","acceptedNameUsageID":3189,"nameAccordingTo":"FNA Editorial Committee. 2006. Flora of North America north of Mexico. Volume 21: Magnoliophyta: Asteridae, part 8: Asteraceae, part 3. Oxford University Press, New York.","nameAccordingToID":"http://www.efloras.org/volume_page.aspx?volume_id=1021&flora_id=1","taxonomicStatus":"accepted","parentNameUsageID":1235,"higherClassification":"Equisetopsida;Magnoliidae;Asteranae;Asterales;Asteraceae;Asteroideae;Heliantheae;Helianthus"}],"vernacularNames":[{"vernacularName":"tournesol","language":"fr","source":"Darbyshire S.J., M. Favreau & M. Murray (revu et augment\xe9 par). 2000. Noms populaires et scientifiques des plantes nuisibles du Canada. Agriculture et Agroalimentaire Canada. Publication 1397. 132 pp.","preferredName":true},{"vernacularName":"common sunflower","language":"en","source":"FNA Editorial Committee. 2006. Flora of North America north of Mexico. Volume 21: Magnoliophyta: Asteridae, part 8: Asteraceae, part 3. Oxford University Press, New York.","preferredName":true},{"vernacularName":"h\xe9lianthe annuel","language":"fr","source":"Marie-Victorin, Fr. 1995. Flore laurentienne. 3e \xe9d. Mise \xe0 jour et annot\xe9e par L. Brouillet, S.G. Hay, I. Goulet, M. Blondeau, J. Cayouette et J. Labrecque. Ga\xe9tan Morin \xe9diteur. 1093 pp.","preferredName":false},{"vernacularName":"soleil","language":"fr","source":"Marie-Victorin, Fr. 1995. Flore laurentienne. 3e \xe9d. Mise \xe0 jour et annot\xe9e par L. Brouillet, S.G. Hay, I. Goulet, M. Blondeau, J. Cayouette et J. Labrecque. Ga\xe9tan Morin \xe9diteur. 1093 pp.","preferredName":false},{"vernacularName":"grand soleil","language":"fr","source":"Louis-Marie, P. 1953. Flore-Manuel de la province de Qu\xe9bec. 2i\xe8me \xe9d. Institut agricole d\'Oka. 323 pp.","preferredName":false},{"vernacularName":"garden sunflower","language":"en","source":"Robert W. Freckmann Herbarium (UWSP), University of Wisconsin-Stevens Point, Wisc.","preferredName":false}],"distribution":[{"locationID":"ISO 3166-2:CA-BC","locality":"BC","establishmentMeans":"introduced","occurrenceStatus":"introduced"},{"locationID":"ISO 3166-2:CA-AB","locality":"AB","establishmentMeans":"introduced","occurrenceStatus":"introduced"},{"locationID":"ISO 3166-2:CA-SK","locality":"SK","establishmentMeans":"introduced","occurrenceStatus":"introduced"},{"locationID":"ISO 3166-2:CA-MB","locality":"MB","establishmentMeans":"introduced","occurrenceStatus":"introduced"},{"locationID":"ISO 3166-2:CA-ON","locality":"ON","establishmentMeans":"introduced","occurrenceStatus":"introduced"},{"locationID":"ISO 3166-2:CA-QC","locality":"QC","establishmentMeans":"introduced","occurrenceStatus":"introduced"},{"locationID":"ISO 3166-2:CA-NB","locality":"NB","establishmentMeans":"introduced","occurrenceStatus":"introduced"},{"locationID":"ISO 3166-2:CA-PE","locality":"PE","establishmentMeans":"","occurrenceStatus":"excluded"},{"locationID":"ISO 3166-2:CA-NS","locality":"NS","establishmentMeans":"introduced","occurrenceStatus":"introduced"},{"locationID":"","locality":"NL_N","establishmentMeans":"","occurrenceStatus":"excluded"},{"locationID":"ISO 3166-2:FR-PM","locality":"PM","establishmentMeans":"introduced","occurrenceStatus":"ephemeral"},{"locationID":"ISO 3166-2:CA-NT","locality":"NT","establishmentMeans":"","occurrenceStatus":"doubtful"}]}]}]}'

    ## xml
    >>> pytaxize.vascan_search(q = ["Helianthus annuus"], format="xml", raw=True)
    u'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><vascanAPIResponse><apiVersion>0.1</apiVersion><results><searchedName><matches><result><taxonomicAssertions><taxonomicAssertion><acceptedNameUsage>Helianthus annuus Linnaeus</acceptedNameUsage><acceptedNameUsageID>3189</acceptedNameUsageID><higherClassification>Equisetopsida;Magnoliidae;Asteranae;Asterales;Asteraceae;Asteroideae;Heliantheae;Helianthus</higherClassification><nameAccordingTo>FNA Editorial Committee. 2006. Flora of North America north of Mexico. Volume 21: Magnoliophyta: Asteridae, part 8: Asteraceae, part 3. Oxford University Press, New York.</nameAccordingTo><nameAccordingToID>http://www.efloras.org/volume_page.aspx?volume_id=1021&amp;flora_id=1</nameAccordingToID><parentNameUsageID>1235</parentNameUsageID><taxonomicStatus>accepted</taxonomicStatus></taxonomicAssertion></taxonomicAssertions><canonicalName>Helianthus annuus</canonicalName><distribution><establishmentMeans>introduced</establishmentMeans><locality>BC</locality><locationID>ISO 3166-2:CA-BC</locationID><occurrenceStatus>introduced</occurrenceStatus></distribution><distribution><establishmentMeans>introduced</establishmentMeans><locality>AB</locality><locationID>ISO 3166-2:CA-AB</locationID><occurrenceStatus>introduced</occurrenceStatus></distribution><distribution><establishmentMeans>introduced</establishmentMeans><locality>SK</locality><locationID>ISO 3166-2:CA-SK</locationID><occurrenceStatus>introduced</occurrenceStatus></distribution><distribution><establishmentMeans>introduced</establishmentMeans><locality>MB</locality><locationID>ISO 3166-2:CA-MB</locationID><occurrenceStatus>introduced</occurrenceStatus></distribution><distribution><establishmentMeans>introduced</establishmentMeans><locality>ON</locality><locationID>ISO 3166-2:CA-ON</locationID><occurrenceStatus>introduced</occurrenceStatus></distribution><distribution><establishmentMeans>introduced</establishmentMeans><locality>QC</locality><locationID>ISO 3166-2:CA-QC</locationID><occurrenceStatus>introduced</occurrenceStatus></distribution><distribution><establishmentMeans>introduced</establishmentMeans><locality>NB</locality><locationID>ISO 3166-2:CA-NB</locationID><occurrenceStatus>introduced</occurrenceStatus></distribution><distribution><establishmentMeans></establishmentMeans><locality>PE</locality><locationID>ISO 3166-2:CA-PE</locationID><occurrenceStatus>excluded</occurrenceStatus></distribution><distribution><establishmentMeans>introduced</establishmentMeans><locality>NS</locality><locationID>ISO 3166-2:CA-NS</locationID><occurrenceStatus>introduced</occurrenceStatus></distribution><distribution><establishmentMeans></establishmentMeans><locality>NL_N</locality><locationID></locationID><occurrenceStatus>excluded</occurrenceStatus></distribution><distribution><establishmentMeans>introduced</establishmentMeans><locality>PM</locality><locationID>ISO 3166-2:FR-PM</locationID><occurrenceStatus>ephemeral</occurrenceStatus></distribution><distribution><establishmentMeans></establishmentMeans><locality>NT</locality><locationID>ISO 3166-2:CA-NT</locationID><occurrenceStatus>doubtful</occurrenceStatus></distribution><scientificName>Helianthus annuus Linnaeus</scientificName><scientificNameAuthorship>Linnaeus</scientificNameAuthorship><taxonID>3189</taxonID><taxonRank>species</taxonRank><vernacularNames><language>fr</language><preferredName>true</preferredName><source>Darbyshire S.J., M. Favreau &amp; M. Murray (revu et augment\xe9 par). 2000. Noms populaires et scientifiques des plantes nuisibles du Canada. Agriculture et Agroalimentaire Canada. Publication 1397. 132 pp.</source><vernacularName>tournesol</vernacularName></vernacularNames><vernacularNames><language>en</language><preferredName>true</preferredName><source>FNA Editorial Committee. 2006. Flora of North America north of Mexico. Volume 21: Magnoliophyta: Asteridae, part 8: Asteraceae, part 3. Oxford University Press, New York.</source><vernacularName>common sunflower</vernacularName></vernacularNames><vernacularNames><language>fr</language><preferredName>false</preferredName><source>Marie-Victorin, Fr. 1995. Flore laurentienne. 3e \xe9d. Mise \xe0 jour et annot\xe9e par L. Brouillet, S.G. Hay, I. Goulet, M. Blondeau, J. Cayouette et J. Labrecque. Ga\xe9tan Morin \xe9diteur. 1093 pp.</source><vernacularName>h\xe9lianthe annuel</vernacularName></vernacularNames><vernacularNames><language>fr</language><preferredName>false</preferredName><source>Marie-Victorin, Fr. 1995. Flore laurentienne. 3e \xe9d. Mise \xe0 jour et annot\xe9e par L. Brouillet, S.G. Hay, I. Goulet, M. Blondeau, J. Cayouette et J. Labrecque. Ga\xe9tan Morin \xe9diteur. 1093 pp.</source><vernacularName>soleil</vernacularName></vernacularNames><vernacularNames><language>fr</language><preferredName>false</preferredName><source>Louis-Marie, P. 1953. Flore-Manuel de la province de Qu\xe9bec. 2i\xe8me \xe9d. Institut agricole d\'Oka. 323 pp.</source><vernacularName>grand soleil</vernacularName></vernacularNames><vernacularNames><language>en</language><preferredName>false</preferredName><source>Robert W. Freckmann Herbarium (UWSP), University of Wisconsin-Stevens Point, Wisc.</source><vernacularName>garden sunflower</vernacularName></vernacularNames></result></matches><numMatches>1</numMatches><searchedTerm>Helianthus annuus</searchedTerm></searchedName></results></vascanAPIResponse>'

    # lots of names, in this case 50
    >>> splist = pytaxize.names_list(rank='species', size=50)
    >>> pytaxize.vascan_search(q = splist)
    {u'apiVersion': u'0.1',
     u'results': [{u'numMatches': 0, u'searchedTerm': u'Monechma spartioides'},
      {u'numMatches': 0, u'searchedTerm': u'Ruellia solitaria'},
      {u'numMatches': 0, u'searchedTerm': u'Justicia californica'},
      {u'numMatches': 0, u'searchedTerm': u'Crossandra cinnabarina'},
      {u'numMatches': 0, u'searchedTerm': u'Thunbergia lamellata'},
      {u'numMatches': 0, u'searchedTerm': u'Eusiphon geayi'},
      {u'numMatches': 0, u'searchedTerm': u'Ruellia geminiflora'},
      {u'numMatches': 0, u'searchedTerm': u'Dicliptera fionae'},
      {u'numMatches': 0, u'searchedTerm': u'Monechma lolioides'},
      {u'numMatches': 0, u'searchedTerm': u'Strobilanthes botryantha'},
      {u'numMatches': 0, u'searchedTerm': u'Mayna parvifolia'},
      {u'numMatches': 0, u'searchedTerm': u'Erythrospermum acuminatissimum'},
      {u'numMatches': 0, u'searchedTerm': u'Xylotheca kraussiana'},
      {u'numMatches': 0, u'searchedTerm': u'Hydnocarpus anthelminthicus'},
      {u'numMatches': 0, u'searchedTerm': u'Chiangiodendron mexicanum'},
      {u'numMatches': 0, u'searchedTerm': u'Caloncoba lophocarpa'},
      {u'numMatches': 0, u'searchedTerm': u'Lindackeria ovata'},
      {u'numMatches': 0, u'searchedTerm': u'Caloncoba brevipes'},
      {u'numMatches': 0, u'searchedTerm': u'Dendrostylis suaveolens'},
      {u'numMatches': 0, u'searchedTerm': u'Mayna suaveolens'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus praecox'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus praecox'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus microcarpus'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus hasslerianus'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus oaxacanus'},
      {u'numMatches': 0, u'searchedTerm': u'Phaulothamnus spinescens'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus nigricans'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus brevipedicellatus'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus praecox'},
      {u'numMatches': 0, u'searchedTerm': u'Achatocarpus pubescens'},
      {u'numMatches': 0, u'searchedTerm': u'Gymnanthe belangeriana'},
      {u'numMatches': 0, u'searchedTerm': u'Tylimanthus urvilleanus'},
      {u'numMatches': 0, u'searchedTerm': u'Acrobolbus lophocoleoides'},
      {u'numMatches': 0, u'searchedTerm': u'Acrobolbus titibuensis'},
      {u'numMatches': 0, u'searchedTerm': u'Acrobolbus surculosus'},
      {u'numMatches': 0, u'searchedTerm': u'Lethocolea radicosa'},
      {u'numMatches': 0, u'searchedTerm': u'Acrobolbus ciliatus'},
      {u'numMatches': 0, u'searchedTerm': u'Tylimanthus approximatus'},
      {u'numMatches': 0, u'searchedTerm': u'Acrobolbus ochrophyllus'},
      {u'numMatches': 0, u'searchedTerm': u'Acrobolbus bustillosii'},
      {u'numMatches': 0, u'searchedTerm': u'Cheilanthes myriophylla'},
      {u'numMatches': 0, u'searchedTerm': u'Pityrogramma calomelanos'},
      {u'numMatches': 0, u'searchedTerm': u'Coniogramme taiwanensis'},
      {u'numMatches': 0, u'searchedTerm': u'Eriosorus glaberrimus'},
      {u'numMatches': 0, u'searchedTerm': u'Trachypteris induta'},
      {u'numMatches': 0, u'searchedTerm': u'Pityrogramma calomelanos'},
      {u'numMatches': 0, u'searchedTerm': u'Cheilanthes rufa'},
      {u'numMatches': 0, u'searchedTerm': u'Cheilanthes mickelii'},
      {u'numMatches': 0, u'searchedTerm': u'Pityrogramma argentea'},
      {u'numMatches': 0, u'searchedTerm': u'Cheilanthes smithii'}]}
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
    >>> import pytaxize
    >>> pytaxize.col_children(name=["Apis"])
    [        id                name     rank
    0  6971712  Apis andreniformis  Species
    1  6971713         Apis cerana  Species
    2  6971714        Apis dorsata  Species
    3  6971715         Apis florea  Species
    4  6971716  Apis koschevnikovi  Species
    5  6845885      Apis mellifera  Species
    6  6971717    Apis nigrocincta  Species]

    # An example where there is no classification, results in data.frame with no rows
    >>> pytaxize.col_children(id=[15669061])
    [        id                name     rank
    0  6971712  Apis andreniformis  Species
    1  6971713         Apis cerana  Species
    2  6971714        Apis dorsata  Species
    3  6971715         Apis florea  Species
    4  6971716  Apis koschevnikovi  Species
    5  6845885      Apis mellifera  Species
    6  6971717    Apis nigrocincta  Species]

    # Use a specific year's checklist
    >>> pytaxize.col_children(name=["Apis"], checklist="2012")
    [        id                name     rank
    0  6971712  Apis andreniformis  Species
    1  6971713         Apis cerana  Species
    2  6971714        Apis dorsata  Species
    3  6971715         Apis florea  Species
    4  6971716  Apis koschevnikovi  Species
    5  6845885      Apis mellifera  Species
    6  6971717    Apis nigrocincta  Species]

    >>> pytaxize.col_children(name=["Apis"], checklist="2009")
    [        id            name     rank
    0  1628188  Apis mellifera  Species]

    # Pass in many names or many id's
    >>> out = pytaxize.col_children(name=["Buteo","Apis","Accipiter"], checklist="2012")
    # get just one element in list of output
    >>> out[0] 
             id                 name     rank
    0   6848078   Buteo albicaudatus  Species
    1   6866408       Buteo albigula  Species
    2   6848077    Buteo albonotatus  Species
    3   6866409        Buteo archeri  Species
    4   6848090     Buteo areophilus  Species
    5   6866410          Buteo augur  Species
    6   6848083      Buteo auguralis  Species
    7   6848084   Buteo brachypterus  Species
    8   6848079     Buteo brachyurus  Species
    9   6848085          Buteo buteo  Species
    10  6848086  Buteo galapagoensis  Species
    11  6848087     Buteo hemilasius  Species
    12  6848073    Buteo jamaicensis  Species
    13  6848080        Buteo lagopus  Species
    14  6848088    Buteo leucorrhous  Species
    15  6848074       Buteo lineatus  Species
    16  6848089   Buteo magnirostris  Species
    17  6848082        Buteo nitidus  Species
    18  6866411     Buteo oreophilus  Species
    19  6848075    Buteo platypterus  Species
    20  6848091  Buteo poecilochrous  Species
    21  6848092      Buteo polyosoma  Species
    22  6848081        Buteo regalis  Species
    23  6848093       Buteo ridgwayi  Species
    24  6848094        Buteo rufinus  Species
    25  6848095     Buteo rufofuscus  Species
    26  6848096     Buteo solitarius  Species
    27  6848076      Buteo swainsoni  Species
    28  6848097      Buteo ventralis  Species

    # or combine to one DataFrame
    >>> import pandas as pd
    >>> pd.concat(out).head()
            id                name     rank
    0  6848078  Buteo albicaudatus  Species
    1  6866408      Buteo albigula  Species
    2  6848077   Buteo albonotatus  Species
    3  6866409       Buteo archeri  Species
    4  6848090    Buteo areophilus  Species

    # or pass many id's
    >>> out = pytaxize.col_children(id=[15669061,15700333,15638488])
    # combine to one DataFrame
    >>> import pandas as pd
    >>> pd.concat(out).head()
            id                name     rank
    0  6971712  Apis andreniformis  Species
    1  6971713         Apis cerana  Species
    2  6971714        Apis dorsata  Species
    3  6971715         Apis florea  Species
    4  6971716  Apis koschevnikovi  Species
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
    >>> import pytaxize
    >>> pytaxize.gbif_parse(scientificname=['x Agropogon littoralis'])
      authorsParsed         canonicalName  canonicalNameComplete  \
    0          True  Agropogon littoralis  ×Agropogon littoralis

      canonicalNameWithMarker genusOrAbove    notho          scientificName  \
    0   ×Agropogon littoralis    Agropogon  GENERIC  x Agropogon littoralis

      specificEpithet     type
    0      littoralis  SCINAME

    >>> pytaxize.gbif_parse(scientificname=['Arrhenatherum elatius var. elatius', 
                 'Secale cereale subsp. cereale', 'Secale cereale ssp. cereale',
                 'Vanessa atalanta (Linnaeus, 1758)'])
      authorsParsed bracketAuthorship bracketYear                  canonicalName  \
    0          True               NaN         NaN  Arrhenatherum elatius elatius
    1          True               NaN         NaN         Secale cereale cereale
    2          True               NaN         NaN         Secale cereale cereale
    3          True          Linnaeus        1758               Vanessa atalanta

                    canonicalNameComplete             canonicalNameWithMarker  \
    0  Arrhenatherum elatius var. elatius  Arrhenatherum elatius var. elatius
    1       Secale cereale subsp. cereale       Secale cereale subsp. cereale
    2       Secale cereale subsp. cereale       Secale cereale subsp. cereale
    3   Vanessa atalanta (Linnaeus, 1758)                    Vanessa atalanta

        genusOrAbove infraSpecificEpithet rankMarker  \
    0  Arrhenatherum              elatius       var.
    1         Secale              cereale     subsp.
    2         Secale              cereale     subsp.
    3        Vanessa                  NaN        NaN

                           scientificName specificEpithet        type
    0  Arrhenatherum elatius var. elatius         elatius  WELLFORMED
    1       Secale cereale subsp. cereale         cereale  WELLFORMED
    2         Secale cereale ssp. cereale         cereale     SCINAME
    3   Vanessa atalanta (Linnaeus, 1758)        atalanta  WELLFORMED
    '''
    url = "http://apidev.gbif.org/parser/name"
    headers = {'content-type': 'application/json'}
    tt = requests.post(url, data=json.dumps(scientificname), headers=headers)
    tt.raise_for_status()
    res = pd.DataFrame(tt.json())
    return res

if __name__ == "__main__":
    import doctest
    doctest.testmod()