import sys
import requests
from lxml import etree
import pandas as pd
import re
import json
from simplejson import JSONDecodeError

class NoResultException(Exception):
    pass

def names_list(rank = 'genus', size = 10):
    '''
    Get a random vector of species names.
    
    :param rank: Taxonomic rank, one of species, genus (default), family, order. 
    :param size: Number of names to get. Maximum depends on the rank.

    Usage:
    >>> import pytaxize
    >>> pytaxize.names_list()
    ['Anomacanthus',
     'Monothecium',
     'Trichosanchezia',
     'Anisotes',
     'Cosmianthemum',
     'Razisea',
     'Cyclacanthus',
     'Harpochilus',
     'Aechmanthera',
     'Sarotheca']

    >>> pytaxize.names_list('species')
    ['Monechma spartioides',
     'Ruellia solitaria',
     'Justicia californica',
     'Crossandra cinnabarina',
     'Thunbergia lamellata',
     'Eusiphon geayi',
     'Ruellia geminiflora',
     'Dicliptera fionae',
     'Monechma lolioides',
     'Strobilanthes botryantha']

    >>> pytaxize.names_list('family')
    ['Acoraceae',
     'Arisaraceae',
     'Blyxaceae',
     'Caladiaceae',
     'Callaceae',
     'Colocasiaceae',
     'Cryptocorynaceae',
     'Damasoniaceae',
     'Dracontiaceae',
     'Elodeaceae']

    >>> pytaxize.names_list('order')
    ['Icacinales',
     'Aponogetonales',
     'Arales',
     'Butomales',
     'Cymodoceales',
     'Elodeales',
     'Hydrocharitales',
     'Juncaginales',
     'Lemnales',
     'Najadales']

    >>> pytaxize.names_list('order', 2)
    ['Icacinales', 'Aponogetonales']

    >>> pytaxize.names_list('order', 15)
    ['Icacinales',
     'Aponogetonales',
     'Arales',
     'Butomales',
     'Cymodoceales',
     'Elodeales',
     'Hydrocharitales',
     'Juncaginales',
     'Lemnales',
     'Najadales',
     'Orontiales',
     'Pistiales',
     'Posidoniales',
     'Potamogetonales',
     'Ruppiales']
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

def scrapenames(url = None, file = None, text = None, engine = None, 
  unique = None, verbatim = None, detect_language = None, all_data_sources = None,
  data_source_ids = None):
  '''
  Resolve names using Global Names Recognition and Discovery.

  Uses the Global Names Recognition and Discovery service, see 
  http://gnrd.globalnames.org/.

  :param url: An encoded URL for a web page, PDF, Microsoft Office document, or 
     image file, see examples
  :param file: When using multipart/form-data as the content-type, a file may be sent.
     This should be a path to your file on your machine.
  :param text: Type: string. Text content; best used with a POST request, see 
     examples
  :param engine: (optional) Type: integer, Default: 0. Either 1 for TaxonFinder, 
     2 for NetiNeti, or 0 for both. If absent, both engines are used.
  :param unique: (optional) Type: boolean. If TRUE (default), 
     response has unique names without offsets.  
  :param verbatim: (optional) Type: boolean, If TRUE (default to FALSE), 
     response excludes verbatim strings. 
  :param detect_language: (optional) Type: boolean, When 
     TRUE (default), NetiNeti is not used if the language of incoming text is 
     determined not to be English. When 'false', NetiNeti will be used if requested. 
  :param all_data_sources: (optional) Type: bolean. Resolve found 
     names against all available Data Sources. 
  :param data_source_ids: (optional) Type: string. Pipe separated list of data 
     source ids to resolve found names against. See list of Data Sources.

  Usage:
  # Get data from a website using its URL
  out = pytaxize.scrapenames(url = 'http://en.wikipedia.org/wiki/Araneae')
  out['data'].head() # data
  out['meta'] # metadata

  # Scrape names from a pdf at a URL
  out = pytaxize.scrapenames(url = 'http://www.mapress.com/zootaxa/2012/f/z03372p265f.pdf')
  out['data'].head() # data
  out['meta'] # metadata

  # With arguments
  pytaxize.scrapenames(url = 'http://www.mapress.com/zootaxa/2012/f/z03372p265f.pdf', 
  unique=TRUE)
  pytaxize.scrapenames(url = 'http://www.mapress.com/zootaxa/2012/f/z03372p265f.pdf', all_data_sources=TRUE)

  # Get data from text string as an R object
  pytaxize.scrapenames(text='A spider named Pardosa moesta Banks, 1892')
  '''
  method = {'url': url, 'file': file, 'text': text}
  method = {key: value for key, value in method.items() if value != None}
  if(len(method) > 1):
    sys.exit("Only one of url, file, or text can be used")

  base = "http://gnrd.globalnames.org/name_finder.json"
  payload = {'url':url, 'text':text, 'engine':engine, 'unique':unique,
             'verbatim':verbatim, 'detect_language':detect_language, 
             'all_data_sources':all_data_sources, 'data_source_ids':data_source_ids}
  
  ss = []
  for i in range(len(method.keys())):
    ss.append(method.keys()[i] in ['url','text'])
  if(any(ss)):
    tt = requests.get(base, params=payload)
  else:
    pass
    # tt = requests.post(base, params=payload, multipart=True, body = [file=upload_file(file)])

  tt.raise_for_status()
  out = tt.json()

  if(out['status'] != 303):
    sys.exit("Woops, something went wrong")
  else:
    token_url = out['token_url']
    st = 303
    while(st == 303):
      dat = requests.get(token_url)
      dat.raise_for_status
      datout = dat.json()
      st = datout['status']
    dd = pd.DataFrame(datout['names'])
    datout.pop('names')
    meta = datout
    return {'meta': meta, 'data': dd}

if __name__ == "__main__":
    import doctest
    doctest.testmod()