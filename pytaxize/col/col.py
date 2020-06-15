import sys
import requests
import datetime
from lxml import etree
import re
import json
import pkg_resources
from pytaxize.refactor import Refactor
from pytaxize.utils import *

# try:
#     import pandas as pd
# except ImportError:
#     warnings.warn("Pandas library not installed, dataframes disabled")
#     pd = None


def children(name=None, id=None, format=None, start=None, checklist=None):
    """
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
        year's checklist instead of the lastest as default (numeric). Valid years
        are 2010 through the previous year from the current date. If none given,
        the "lastest" checklist is used
    
    You must provide one of name or id. The other parameters (format and start) are
    optional. Returns A list of data.frame's.

    Usage::

        from pytaxize import col
        col.children(name=["Apis"])

        # An example where there is no classification, results in data.frame with no rows
        col.children(id=["4fdb38d6220462049eab9e3f285144e0"])

        # Use a specific year's checklist
        col.children(name=["Apis"], checklist="2012")
        col.children(name=["Apis"], checklist="2009")

        # Pass in many names or many id's
        out = col.children(name=["Buteo","Apis","Accipiter"], checklist="2012")
        # get just one element in list of output
        out[0]
    """

    assert_range_numeric(checklist, 2010, datetime.datetime.now().year)

    def func(x, y, checklist):
        url = "https://www.catalogueoflife.org/col/webservice"

        if checklist is None:
            pass
        else:
            checklist = str(checklist)
            if checklist in ["2012", "2011", "2010"]:
                url = re.sub("col", "annual-checklist/" + checklist, url)
            else:
                url = "https://www.catalogueoflife.org/annual-checklist/year/webservice"
                url = re.sub("year", checklist, url)

        payload = {
            "name": x,
            "id": y,
            "format": format,
            "response": "full",
            "start": start,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        tt = Refactor(url, payload, request="get").xml()
        childtaxa = tt.xpath("//child_taxa//taxon")
        if len(childtaxa) == 0:
            sys.exit("Please enter a valid search name")
        outlist = []
        for i in range(len(childtaxa)):
            tt_ = childtaxa[i].getchildren()
            outlist.append(dict(zip(["id", "name", "rank"], [x.text for x in tt_[:3]])))
        return outlist

    if id is None:
        temp = []
        for i in range(len(name)):
            ss = func(name[i], None, checklist)
            temp.append(ss)
        return temp
    else:
        temp = []
        for i in range(len(id)):
            ss = func(None, id[i], checklist)
            temp.append(ss)
        return temp


# def downstream(name=None, downto=None, format=None, start=None, checklist=None):
#     """
#     :param name: The string to search for. Only exact matches found the name given
#         will be returned, unless one or wildcards are included in the search
#         string. An * (asterisk) character denotes a wildcard; a % (percentage)
#         character may also be used. The name must be at least 3 characters long,
#         not counting wildcard characters.
#     :param downto: The taxonomic level you want to go down to. See examples below.
#         The taxonomic level IS case sensitive, and you do have to spell it
#         correctly. See rank_ref for spelling.
#     :param checklist: The year of the checklist to query, if you want a specific
#         year's checklist instead of the lastest as default (numeric).
#     :param format: The returned format (default = None). If NULL xml is used.
#         Currently only xml is supported.
#     :param start:  The first record to return (default = None). If NULL, the
#        results are returned from the first record (start=0). This is useful if
#        the total number of results is larger than the maximum number of results
#        returned by a single Web service query (currently the maximum number of
#        results returned by a single query is 500 for terse queries and 50 for
#        full queries).

#     Returns a list of Pandas DataFrame's.

#     Usage::
        
#         from pytaxize import col

#         col.downstream(name="Apis", downto="Species")
#         col.downstream(name="Insecta", downto="Order")

#         # Multiple names at once
#         col.downstream(name=["Insecta","Diplopoda"], downto="Order")

#         # Using a checklist from a specific year
#         col.downstream(name="Apis", downto="Species", checklist=2011)
#     """
#     col_url = "https://www.catalogueoflife.org/col/webservice"
#     year_url = "https://www.catalogueoflife.org/annual-checklist/year/webservice"

#     def func(name, downto, format, start, checklist):
#         if checklist is None:
#             url = col_url
#         else:
#             checklist = str(checklist)
#             if checklist in ["2012", "2011", "2010"]:
#                 url = re.sub("col", "annual-checklist/" + checklist, col_url)
#             else:
#                 url = re.sub("year", checklist, year_url)

#         rank_ref_path = pkg_resources.resource_filename("pytaxize", "data/rank_ref.csv")
#         dat = pd.read_csv(rank_ref_path)

#         stuff = [x for x in dat.ranks]
#         things = []
#         for i in range(len(stuff)):
#             ss = downto in stuff[i]
#             things.append(ss)
#         dat2 = dat.join(pd.DataFrame(things, columns=["match"]))
#         subset = dat2[dat2.loc[dat2.match == True].index[0] : dat2.shape[0]]
#         torank = [x.split(",")[0] for x in subset.ranks]

#         toget = name
#         stop_ = "not"
#         notout = pd.DataFrame(columns=["rankName"])
#         out = []
#         iter = 0
#         while stop_ == "not":
#             iter += 1

#             def searchcol(x, url):
#                 payload = {
#                     "name": x,
#                     "format": format,
#                     "response": "full",
#                     "start": start,
#                 }
#                 payload = {k: v for k, v in payload.items() if v is not None}
#                 tt = Refactor(url, payload, request="get").xml()
#                 childtaxa = tt.xpath("//child_taxa//taxon")
#                 outlist = []
#                 for i in range(len(childtaxa)):
#                     tt_ = childtaxa[i].getchildren()
#                     outlist.append([x.text for x in tt_[:3]])
#                 df = pd.DataFrame(outlist, columns=["id", "name", "rank"])
#                 return df

#             tt = searchcol(toget, url)

#             if downto in [x for x in tt["rank"]]:
#                 out.append(tt.loc[tt["rank"] == downto])

#             if tt.loc[tt["rank"] != downto].shape[0] > 0:
#                 sh = [x for x in tt["rank"]]
#                 bb = []
#                 for i in range(len(sh)):
#                     bb.append(sh[i] in torank)
#                 notout = tt[bb]
#             else:
#                 vals = list()
#                 vals.append(downto)
#                 notout = pd.DataFrame(vals, columns=["rank"])

#             if all(notout["rank"] == downto):
#                 stop_ = "fam"
#             else:
#                 toget = notout["name"]
#                 stop_ = "not"

#         return out

#     if isinstance(name, str):
#         nametmp = list()
#         nametmp.append(name)
#         name = nametmp
#     temp = []
#     for i in range(len(name)):
#         tt = func(name[i], downto, format, start, checklist)
#         temp.append(tt)
#     return temp


def search(name=None, id=None, start=None, checklist=None):
    """
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

    You must provide one of name or id. The other parameters (format and start)
    are optional.

    Usage::

        from pytaxize import col

        col.search(name=["Apis"])
        col.search(id=15669061)

        # Many names
        col.search(name=["Apis","Puma concolor"])

        # Many ids - DOESNT WORK
        col.search(id=[15669061,6862841])

        # An example where there is no data
        col.search(id=11935941)

        # Example with more than 1 result
        col.search(name=['Poa'])
    """

    def func(x, y):
        url = "https://www.catalogueoflife.org/col/webservice"
        if checklist is None:
            pass
        else:
            if checklist in ["2012", "2011", "2010"]:
                url = re.sub("col", "annual-checklist/" + checklist, url)
            else:
                url = "https://www.catalogueoflife.org/annual-checklist/year/webservice"
                url = re.sub("year", checklist, url)

        payload = {"name": x, "id": y, "start": start}
        tt = Refactor(url, payload, request="get").xml()
        stuff = tt.xpath("//result")
        outlist = []
        for i in range(len(stuff)):
            tt_ = stuff[i]
            each = {}
            for g in range(len(tt_)):
                for e in tt_[g].iter():
                    each.update({e.tag: e.text})
            outlist.append(each)
        return outlist

    if id is None:
        temp = []
        for i in range(len(name)):
            temp.append(func(name[i], y=None))
    else:
        id = str(id)
        temp = []
        for i in range(len(id)):
            temp.append(func(x=None, y=id[i]))
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
