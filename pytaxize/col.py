import sys
import requests
from lxml import etree
import pandas as pd
import re
import json
from pytaxize.refactor import requests_refactor

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
        tt = requests_refactor(url, payload, 'get', content=False)
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

def col_downstream(name = None, downto = None, format = None, start = None, checklist = None):
    '''
    :param name: The string to search for. Only exact matches found the name given
        will be returned, unless one or wildcards are included in the search
        string. An * (asterisk) character denotes a wildcard; a % (percentage)
        character may also be used. The name must be at least 3 characters long,
        not counting wildcard characters.
    :param downto: The taxonomic level you want to go down to. See examples below.
        The taxonomic level IS case sensitive, and you do have to spell it
        correctly. See \code{data(rank_ref)} for spelling.
    :param checklist: The year of the checklist to query, if you want a specific
        year's checklist instead of the lastest as default (numeric).
    :param format: The returned format (default = None). If NULL xml is used.
        Currently only xml is supported.
    :param start:  The first record to return (default = None). If NULL, the
       results are returned from the first record (start=0). This is useful if
       the total number of results is larger than the maximum number of results
       returned by a single Web service query (currently the maximum number of
       results returned by a single query is 500 for terse queries and 50 for
       full queries).

    Returns a list of DataFrame's.

    Usage:
    # Some basic examples
    >>> pytaxize.col_downstream(name=["Apis"], downto="Species")
    >>> pytaxize.col_downstream(name=["Bryophyta"], downto="Family")

    # An example that takes a bit longer
    >>> pytaxize.col_downstream(name=["Plantae","Animalia"], downto="Class")

    # Using a checklist from a specific year
    >>> pytaxize.col_downstream(name=["Bryophyta"], downto=["Family"], checklist="2009")
    '''
    url = "http://www.catalogueoflife.org/col/webservice"
    def func(name):
        if(checklist.__class__.__name__ == 'NoneType'):
            pass
        else:
            if(checklist in ['2012','2011','2010']):
                url = re.sub("col", "annual-checklist/" + checklist, url)
            else:
                url = "http://www.catalogueoflife.org/annual-checklist/year/webservice"
                url = re.sub("year", checklist, url)

        dat = pd.read_csv("rank_ref.csv", header=False)

        stuff = [x for x in dat.ranks]
        things = []
        for i in range(len(stuff)):
            ss = downto in stuff[i]
            things.append(ss)
        dat2 = dat.join(pd.DataFrame(things, columns=['match']))
        subset = dat2[dat2.loc[dat2.match == True].index[0]: dat2.shape[0]]
        torank = [x.split(',')[0] for x in subset.ranks]

        toget = name
        stop_ = "not"
        notout = pd.DataFrame(columns=['rankName'])
        out = []
        iter = 0
        while(stop_ == "not"):
            iter = iter + 1

            def searchcol(x):
                payload = {'name':x, 'format':format, 'response':"full", 'start':start}
                tt = requests_refactor(url, payload, 'get', content=False)
                childtaxa = tt.xpath('//child_taxa//taxon')
                outlist = []
                for i in range(len(childtaxa)):
                    tt_ = childtaxa[i].getchildren()
                    outlist.append([x.text for x in tt_[:3]])
                df = pd.DataFrame(outlist, columns=['id','name','rank'])
                return df

            tt = searchcol(toget)

            if(downto in [x for x in tt['rank']]):
                out.append(tt.loc[tt['rank'] == downto])

            if(tt.loc[tt['rank'] != downto].index[-1] > 0):
                sh = [x for x in tt['rank']]
                bb = []
                for i in range(len(sh)):
                  bb.append(sh[i] in torank)
                notout = tt[bb]
            else:
                notout = pd.DataFrame(downto, columns=['rankName'])

            if(all(notout['rank'] == downto)):
                stop_ = "fam"
            else:
                toget = notout['name']
                stop_ = "not"

        return out

    temp = []
    for i in range(len(name)):
        tt = func(name[i])
        temp.append = tt
    return temp

def col_search(name=None, id=None, start=None, checklist=None):
    '''
    Search Catalogue of Life for taxonomic IDs

    :param name: The string to search for. Only exact matches found the name given
         will be returned, unless one or wildcards are included in the search
         string. An * (asterisk) character denotes a wildcard; a % (percentage)
       character may also be used. The name must be at least 3 characters long,
       not counting wildcard characters.
    :param id: The record ID of the specific record to return (only for scientific
         names of species or infraspecific taxa)
    :param start: The first record to return. If omitted, the results are returned
         from the first record (start=0). This is useful if the total number of
         results is larger than the maximum number of results returned by a single
         Web service query (currently the maximum number of results returned by a
         single query is 500 for terse queries and 50 for full queries).
    :param checklist: The year of the checklist to query, if you want a specific
         year's checklist instead of the lastest as default (numeric).

    You must provide one of name or id. The other parameters (format
        and start) are optional.

    Usage:

    # A basic example
    pytaxize.col_search(name=["Apis"])
    pytaxize.col_search(id=15669061)

    # Many names
    pytaxize.col_search(name=["Apis","Puma concolor"])

    # Many ids
    pytaxize.col_search(id=[15669061,6862841])

    # An example where there is no data
    pytaxize.col_search(id=11935941)

    # Example with more than 1 result
    pytaxize.col_search(name=['Poa'])
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

        payload = {'name': x, 'id': y, 'start': start}
        tt = requests_refactor(url, payload, 'get', content=False)
        stuff = tt.xpath('//result')
        outlist = []
        for i in range(len(stuff)):
            tt_ = stuff[i]
            each = {}
            for g in range(len(tt_)):
                for e in tt_[g].iter():
                    each.update({e.tag: e.text})
            outlist.append(each)
            # values = [x.text for x in tt_[:4]]
            # tags = [x.tag for x in tt_[:4]]
            # mydict = dict(zip(tags, values))
        df = pd.DataFrame(outlist)
        # tt_ = stuff[0].getchildren()
        # res = [x.text for x in tt_[:4]]
        return df

        # tt = xmlParse(out)
        # toget = c('id','name','rank','name_status')
        # nodes = getNodeSet(tt, "//result", fun=xmlToList)
        # ldply(nodes, parsecoldata)

    if(id.__class__.__name__ == 'NoneType'):
        temp = []
        for i in range(len(name)):
            temp.append(func(name[i], y=None))
        # names(temp) = name
    else:
        temp = []
        for i in range(len(id)):
            temp.append(func(x=None, y=id[i]))
        # names(temp) = id
    return temp

    # def parsecoldata(x):
    #     vals = x[c('id','name','rank','name_status','source_database')]
    #     vals[sapply(vals, is.null)] = NA
    #     names(vals) = c('id','name','rank','name_status','source_database')
    #     bb = data.frame(vals, stringsAsFactors=FALSE)
    #     names(bb)[4:5] = c('status','source')
    #     acc = x$accepted_name
    #     if(is.null(acc)):
    #         accdf = data.frame(acc_id=NA, acc_name=NA, acc_rank=NA, acc_status=NA, acc_source=NA)
    #     else:
    #         accdf = data.frame(acc[c('id','name','rank','name_status','source_database')], stringsAsFactors=FALSE)
    #         names(accdf) = c('acc_id','acc_name','acc_rank','acc_status','acc_source')

    #     return cbind(bb, accdf)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
