import sys
import requests
import pandas as pd
from lxml import etree

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

def gettaxonomicranknamefromtsn(tsn):
    '''
    Returns the kingdom and rank information for the TSN.
    
    :param tsn: TSN for a taxonomic group (numeric)

    Usage:
    pytaxize.gettaxonomicranknamefromtsn(tsn = 202385)
    '''
    url = 'http://www.itis.gov/ITISWebService/services/ITISService/getTaxonomicRankNameFromTSN'
    payload = {'tsn': tsn}
    out = requests.get(url, params = payload)
    out.raise_for_status()
    xmlparser = etree.XMLParser()
    tt = etree.fromstring(out.content, xmlparser)

    ns = {'ax21':'http://data.itis_service.itis.usgs.gov/xsd'}
    ss_nodes = tt.xpath('//ax21:*', namespaces=ns)
    vals = [x.text for x in ss_nodes]
    keys = [x.tag.split('}')[1] for x in ss_nodes]
    # df = pd.DataFrame([dict(zip(keys, vals))])
    df = dict(zip(keys, vals))
    return df

def getfullhierarchyfromtsn(tsn):
    '''
    Get full hierarchy from tsn
    
    :param tsn: TSN for a taxonomic group (numeric)
    
    Usage:
    pytaxize.getfullhierarchyfromtsn(tsn = 37906)
    pytaxize.getfullhierarchyfromtsn(tsn = 100800)
    '''
    url = 'http://www.itis.gov/ITISWebService/services/ITISService/getFullHierarchyFromTSN'
    payload = {'tsn': tsn}
    out = requests.get(url, params = payload)
    out.raise_for_status()
    xmlparser = etree.XMLParser()
    tt = etree.fromstring(out.content, xmlparser)
    ns = {'ax21':'http://data.itis_service.itis.usgs.gov/xsd'}
    ss_nodes = tt.xpath('//ax21:hierarchyList', namespaces=ns)
    uu = []
    for i in xrange(len(ss_nodes)):
        uu.append([x.text for x in ss_nodes[i]])
    df = pd.DataFrame(uu, columns=['tsn','author','parentName','parentTsn','rankName','taxonName'])
    df = df.drop('author', axis=1)
    df = df.reindex_axis(['tsn','rankName','taxonName','parentName','parentTsn'], axis=1)
    return df

def gethierarchydownfromtsn(tsn):
    '''
    Get hierarchy down from tsn

    :param tsn: TSN for a taxonomic group (numeric)
    
    Usage:
    pytaxize.gethierarchydownfromtsn(tsn = 161030)
    '''
    url = 'http://www.itis.gov/ITISWebService/services/ITISService/getHierarchyDownFromTSN'
    payload = {'tsn': tsn}
    out = requests.get(url, params = payload)
    out.raise_for_status()
    xmlparser = etree.XMLParser()
    tt = etree.fromstring(out.content, xmlparser)
    ns = {'ax21':'http://data.itis_service.itis.usgs.gov/xsd'}
    ss_nodes = tt.xpath('//ax21:hierarchyList', namespaces=ns)
    uu = []
    for i in xrange(len(ss_nodes)):
        uu.append([x.text for x in ss_nodes[i]])
    df = pd.DataFrame(uu, columns=['tsn','author','parentName','parentTsn','rankName','taxonName'])
    df = df.drop('author', axis=1)
    df = df.reindex_axis(['tsn','rankName','taxonName','parentName','parentTsn'], axis=1)
    return df

def gethierarchyupfromtsn(tsn):
    '''
    Get hierarchy up from tsn

    :param tsn: TSN for a taxonomic group (numeric)
    
    Usage:
    pytaxize.gethierarchyupfromtsn(tsn = 36485)
    pytaxize.gethierarchyupfromtsn(tsn = 37906)
    '''
    url = 'http://www.itis.gov/ITISWebService/services/ITISService/getHierarchyUpFromTSN'
    payload = {'tsn': tsn}
    out = requests.get(url, params = payload)
    out.raise_for_status()
    xmlparser = etree.XMLParser()
    tt = etree.fromstring(out.content, xmlparser)
    ns = {'ax21':'http://data.itis_service.itis.usgs.gov/xsd'}
    ss_nodes = tt.xpath('//ax21:*', namespaces=ns)
    vals = [x.text for x in ss_nodes]
    keys = [x.tag.split('}')[1] for x in ss_nodes]
    df = pd.DataFrame([dict(zip(keys, vals))])
    return df

def itis_hierarchy(tsn=None, what="full"):
    '''
    Get hierarchies from TSN values, full, upstream only, or immediate downstream 
    only. Uses the ITIS database.

    :param tsn: One or more TSN's (taxonomic serial number)
    :param what: One of full (full hierarchy), up (immediate upstream), or down 
       (immediate downstream)
    
    Details Note that \code{\link{itis_downstream}} gets taxa downstream to a particular
       rank, whilc this function only gets immediate names downstream.
    
    Usage:
    # Get full hierarchy
    pytaxize.itis_hierarchy(tsn=180543)

    # Get hierarchy upstream
    pytaxize.itis_hierarchy(tsn=180543, "up")

    # Get hierarchy downstream
    pytaxize.itis_hierarchy(tsn=180543, "down")

    # Many tsn's
    pytaxize.itis_hierarchy(tsn=[180543,41074,36616])
    '''
    tsn2 = convertsingle(tsn)
    temp = []
    if(what == 'full'):
        for i in xrange(len(tsn2)):
            temp.append(getfullhierarchyfromtsn(tsn2[i]))
    elif(what == 'up'):
        for i in xrange(len(tsn2)):
            temp.append(gethierarchyupfromtsn(tsn2[i]))
    else:
        for i in xrange(len(tsn2)):
            temp.append(gethierarchydownfromtsn(tsn2[i]))
    return temp

def convertsingle(x):
    if(x.__class__.__name__ == 'int'):
        return [x]
    else:
        return x

# def itis_downstream(tsn, downto):
#     '''
#     Retrieve all taxa names or TSNs downstream in hierarchy from given TSN.
    
#     :param tsn: A taxonomic serial number. 
#     :param downto: The taxonomic level you want to go down to. See examples below.
#          The taxonomic level IS case sensitive, and you do have to spell it 
#          correctly. See \code{data(rank_ref)} for spelling.
#     :param verbose: logical; If TRUE (default), informative messages printed.
    
#     Usage:
#     pytaxize.itis_downstream(tsn=846509, downto="Genus")
    
#     # getting families downstream from Acridoidea
#     pytaxize.itis_downstream(tsn=650497, "Family")
    
#     # getting species downstream from Ursus
#     pytaxize.itis_downstream(tsn=180541, downto="Species")
#     '''
#     dat = pd.read_csv("rank_ref.csv", header=False)
#     downto2 = dat[dat['ranks'].str.contains(downto)]['rankId']
#     torank_ids = dat[dat[dat['ranks'].str.contains(downto)].index : dat.shape[0]]['rankId']
    
#     # stuff = [x for x in dat.ranks]
#     # things = []
#     # for i in range(len(stuff)):
#     #     ss = downto in stuff[i]
#     #     things.append(ss)
#     # dat2 = dat.join(pd.DataFrame(things, columns=['match']))
#     # subset = dat2[dat2.loc[dat2.match == True].index[0]: dat2.shape[0]]
#     # torank = [x.split(',')[0] for x in subset.ranks]

#     tsn2 = convertsingle(tsn)

#     stop_ = "not"
#     notout = pd.DataFrame(columns=['rankName'])
#     out = []
#     while(stop_ == "not"):
#         temp = []
#         if(len([x for x in notout.rankName]) == 0):
#             temp = pytaxize.gettaxonomicranknamefromtsn(tsn2)
#         else:
#             temp = notout
#         tt = pytaxize.gethierarchydownfromtsn(temp['tsn'])
        
#         names = []
#         for i in xrange(len(tt['tsn'])):
#             d = pytaxize.gettaxonomicranknamefromtsn(tt['tsn'][i])
#             names.append(d)
#         names2 = pd.DataFrame(names)
#         tt = tt.merge(names2, on='tsn')
#         if(tt[tt['rankId'].str.contains(downto2.to_string().split(' ')[-1])].shape[0] > 0): 
#             out.append(tt[tt['rankId'].str.contains(downto2.to_string().split(' ')[-1])])

#         if(tt.drop(matched.index).shape[0] > 0):
#             shit = list(set([str(x) for x in torank_ids.tolist()]) - set(tt['rankId'].tolist()))
#             notout = pd.DataFrame([tt[tt['rankId'].str.contains(x)] for x in shit])
#         else:
#             notout = pd.DataFrame([downto], columns=['rankName'])
        
#         if(all(notout['rankName'] == downto)):
#             stop_ = "fam"
#         else:
#             tsns = notout$tsn
#             stop_ = "not"
#     tmp = ldply(out)
#     names(tmp) = tolower(names(tmp))
#     tmp

if __name__ == "__main__":
    import doctest
    doctest.testmod()