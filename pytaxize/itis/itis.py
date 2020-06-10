import sys
import time
import requests
import warnings

from lxml import etree
from pytaxize.refactor import Refactor

try:
    import pandas as pd
except ImportError:
    warnings.warn("Pandas library not installed, dataframes disabled")
    pd = None
itis_base = "http://www.itis.gov/ITISWebService/jsonservice/"


def getacceptednamesfromtsn(tsn, **kwargs):
    """
    Get accepted names from tsn

    :param tsn: taxonomic serial number (TSN) (character or numeric)

    Usage::
        
        from pytaxize import itis
        # TSN accepted - good name
        itis.getacceptednamesfromtsn(tsn=208527)
        # TSN not accepted - input TSN is old name
        itis.getacceptednamesfromtsn(tsn=504239)
    """
    out = Refactor(
        itis_base + "getAcceptedNamesFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    if out["acceptedNames"][0] is None:
        return {}
    else:
        out["acceptedNames"][0].pop("class")
        return out["acceptedNames"][0]


def getanymatchcount(x, **kwargs):
    """
    Get any match count.

    :param x: text or taxonomic serial number (TSN) (character or numeric)
    :param **kwargs: Curl options passed on to `requests.get`

    Usage::
    
        from pytaxize import itis
        itis.getanymatchcount(x=202385)
        itis.getanymatchcount(x="dolphin")
    """
    out = Refactor(
        itis_base + "getAnyMatchCount", payload={"srchKey": x}, request="get"
    ).json(**kwargs)
    return out["return"]


def getcommentdetailfromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get comment detail from TSN

    :param tsn: TSN for a taxonomic group (numeric)
    :param as_dataframe: specify return type, if pandas is available (boolean)
    :param **kwargs: Curl options passed on to `requests.get`

    Usage::
                
        from pytaxize import itis
        itis.getcommentdetailfromtsn(tsn=180543)
    """
    out = Refactor(
        itis_base + "getCommentDetailFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    [z.pop("class") for z in out["comments"]]
    return _df(out["comments"], as_dataframe)


def getcommonnamesfromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get common names from tsn

    :param tsn: TSN for a taxonomic group (numeric)
    :param as_dataframe: specify return type, if pandas is available (boolean)
    :param **kwargs: Curl options passed on to `requests.get`

    Usage::
        
        from pytaxize import itis
        itis.getcommonnamesfromtsn(tsn=183833)
    """
    out = Refactor(
        itis_base + "getCommonNamesFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    [z.pop("class") for z in out["commonNames"]]
    return _df(out["commonNames"], as_dataframe)


def getcoremetadatafromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get core metadata from tsn

    Usage::
        
        from pytaxize import itis
        # coverage and currrency data
        itis.getcoremetadatafromtsn(tsn=28727)
        # no coverage or currrency data
        itis.getcoremetadatafromtsn(tsn=183671)
    """
    out = Refactor(
        itis_base + "getCoreMetadataFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    out.pop("class")
    return _df([out], as_dataframe)


def getcoveragefromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get coverge from tsn

    Usage::
        
        from pytaxize import itis
        # coverage data
        itis.getcoveragefromtsn(tsn=28727)
        # no coverage data
        itis.getcoveragefromtsn(526852)
        # as data_frame
        itis.getcoveragefromtsn(526852, as_dataframe=True)
    """
    out = Refactor(
        itis_base + "getCoverageFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    out.pop("class")
    return _df(out, as_dataframe)


def getcredibilityratingfromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get credibility rating from tsn

    Usage::
        
        from pytaxize import itis
        itis.getcredibilityratingfromtsn(tsn=526852)
        itis.getcredibilityratingfromtsn(28727)
    """
    out = Refactor(
        itis_base + "getCredibilityRatingFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    out.pop("class")
    return _df(out, as_dataframe)


def getcredibilityratings(**kwargs):
    """
    Get possible credibility ratings

    :param **kwargs: Curl options passed on to `requests.get`
    :return: a dict

    Usage::
        
        from pytaxize import itis
        itis.getcredibilityratings()
    """
    out = Refactor(itis_base + "getCredibilityRatings", payload={}, request="get").json(
        **kwargs
    )
    out.pop("class")
    return out["credibilityValues"]


def getcurrencyfromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get currency from tsn

    Usage::
        
        from pytaxize import itis
        # currency data
        itis.getcurrencyfromtsn(28727)
        # no currency dat
        itis.getcurrencyfromtsn(526852)
        # as data_frame
        itis.getcurrencyfromtsn(526852, as_dataframe=True)
    """
    out = Refactor(
        itis_base + "getCurrencyFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    out.pop("class")
    return _df(out, as_dataframe)


def getdatedatafromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get date data from tsn

    Usage::
        
        from pytaxize import itis
        itis.getdatedatafromtsn(tsn=180543)
    """
    out = Refactor(
        itis_base + "getDateDataFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    out.pop("class")
    return _df(out, as_dataframe)


def getexpertsfromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get expert information for the TSN.

    Usage::
        
        from pytaxize import itis
        itis.getexpertsfromtsn(tsn=180544)
    """
    out = Refactor(
        itis_base + "getExpertsFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    out.pop("class")
    return _df(out["experts"], as_dataframe)


def gettaxonomicranknamefromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Returns the kingdom and rank information for the TSN.

    :param tsn: TSN for a taxonomic group (numeric)

    Usage::
        
        from pytaxize import itis
        itis.gettaxonomicranknamefromtsn(tsn = 202385)
    """
    tt = Refactor(
        itis_base + "getTaxonomicRankNameFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    tt.pop("class")
    return _df(tt, as_dataframe)


def getfullhierarchyfromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get full hierarchy from ts

    :param tsn: TSN for a taxonomic group (numeric)

    Usage::
        
        from pytaxize import itis
        itis.getfullhierarchyfromtsn(tsn = 37906)
        itis.getfullhierarchyfromtsn(tsn = 100800)
        # as data_frame
        itis.getfullhierarchyfromtsn(tsn = 100800, as_dataframe=True)
    """
    tt = Refactor(
        itis_base + "getFullHierarchyFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    hier = tt["hierarchyList"]
    [z.pop("class") for z in hier]
    return _df(hier, as_dataframe)


# def _fullrecord(verb, args, **kwargs):
#     out = Refactor(itis_base + verb, payload=args, request="get").json(**kwargs)
#     toget = [
#         "acceptedNameList",
#         "commentList",
#         "commonNameList",
#         "completenessRating",
#         "coreMetadata",
#         "credibilityRating",
#         "currencyRating",
#         "dateData",
#         "expertList",
#         "geographicDivisionList",
#         "hierarchyUp",
#         "jurisdictionalOriginList",
#         "kingdom",
#         "otherSourceList",
#         "parentTSN",
#         "publicationList",
#         "scientificName",
#         "synonymList",
#         "taxRank",
#         "taxonAuthor",
#         "unacceptReason",
#         "usage",
#     ]

#     def parsedat(x):
#         ch = out.xpath("//ax21:" + x, namespaces=ns21)[0].getchildren()
#         return _get_text(ch)

#     return [parsedat(x) for x in toget]


def _fullrecord(verb, args, **kwargs):
    out = Refactor(itis_base + verb, payload=args, request="get").json(**kwargs)
    return out


def getfullrecordfromlsid(lsid, **kwargs):
    """
    Returns the full ITIS record for the TSN in the LSID, found by comparing the
    TSN in the search key to the TSN field. Returns an empty result set if
    there is no match or the TSN is invalid.

    :param lsid: lsid for a taxonomic group (character)
    :param **kwargs: Curl options passed on to `requests.get`

    Usage::
        
        from pytaxize import itis
        itis.getfullrecordfromlsid(lsid="urn:lsid:itis.gov:itis_tsn:180543")
        itis.getfullrecordfromlsid("urn:lsid:itis.gov:itis_tsn:37906")
        itis.getfullrecordfromlsid("urn:lsid:itis.gov:itis_tsn:100800")
    """
    return _fullrecord("getFullRecordFromLSID", {"lsid": lsid}, **kwargs)


def getfullrecordfromtsn(tsn, **kwargs):
    """
    Returns the full ITIS record for a TSN

    :param tsn: tsn for a taxonomic group (character)
    :param **kwargs: Curl options passed on to `requests.get`

    Usage::
        
        from pytaxize import itis
        itis.getfullrecordfromtsn("504239")
        itis.getfullrecordfromtsn("202385")
        itis.getfullrecordfromtsn("183833")
    """
    return _fullrecord("getFullRecordFromTSN", {"tsn": tsn}, **kwargs)


def getgeographicdivisionsfromtsn(tsn, as_dataframe=False, **kwargs):
    """
    Get geographic divisions from tsn

    Usage::
        
        from pytaxize import itis
        itis.getgeographicdivisionsfromtsn(tsn=180543)
    """
    out = Refactor(
        itis_base + "getGeographicDivisionsFromTSN", payload={"tsn": tsn}, request="get"
    ).json(**kwargs)
    out.pop("class")
    [z.pop("class") for z in out["geoDivisions"]]
    return _df(out["geoDivisions"], as_dataframe)


# def getgeographicvalues(**kwargs):
#     """
#     Get all possible geographic values

#     :param **kwargs: Curl options passed on to `requests.get`

#     Usage::

#         from pytaxize import itis
#         itis.getgeographicvalues()
#     """
#     out = Refactor(itis_base + "getGeographicValues", payload={}, request="get").xml(
#         **kwargs
#     )
#     ns = {"ax21": "http://metadata.itis_service.itis.usgs.gov/xsd"}
#     nodes = out.xpath("//ax21:geographicValues", namespaces=ns)
#     return [x.text for x in nodes]


# def getglobalspeciescompletenessfromtsn(tsn, **kwargs):
#     """
#     Get global species completeness from tsn

#     Usage::

#         from pytaxize import itis
#         itis.getglobalspeciescompletenessfromtsn(180541)
#     """
#     out = Refactor(
#         itis_base + "getGlobalSpeciesCompletenessFromTSN",
#         payload={"tsn": tsn},
#         request="get",
#     ).json(**kwargs)
#     toget = ["completeness", "rankId", "tsn"]
#     return _itis_parse(toget, out, ns21)


# def gethierarchydownfromtsn(tsn, **kwargs):
#     """
#     Get hierarchy down from tsn

#     :param tsn: TSN for a taxonomic group (numeric)

#     Usage::

#         from pytaxize import itis
#         itis.gethierarchydownfromtsn(tsn = 161030)
#     """
#     tt = Refactor(
#         itis_base + "getHierarchyDownFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     ns = {"ax21": "http://data.itis_service.itis.usgs.gov/xsd"}
#     df = _parse_hier(tt, ns)
#     return df


# def gethierarchyupfromtsn(tsn, **kwargs):
#     """
#     Get hierarchy up from tsn

#     :param tsn: TSN for a taxonomic group (numeric)

#     Usage::

#         from pytaxize import itis
#         itis.gethierarchyupfromtsn(tsn = 36485)
#         itis.gethierarchyupfromtsn(tsn = 37906)
#     """
#     tt = Refactor(
#         itis_base + "getHierarchyUpFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     ns = {"ax21": "http://data.itis_service.itis.usgs.gov/xsd"}
#     df = _parse2df(tt, ns)
#     return df


# def _itisterms(endpt, args={}, **kwargs):
#     """
#     Get itis term

#     Usage::

#         from pytaxize import itis
#         itis._itisterms("buya")
#     """
#     out = Refactor(itis_base + endpt, payload=args, request="get").json(**kwargs)

#     nodes = out.xpath("//ax21:itisTerms", namespaces=ns21)
#     nodes2 = [x.getchildren() for x in nodes]
#     allnodes = [[_get_text_single(y) for y in x] for x in nodes2]

#     output = []
#     for x in allnodes:
#         kyz = [list(y.keys())[0] for y in x]
#         notuniq = set([v for v in kyz if kyz.count(v) > 1])
#         if len(notuniq) > 0:
#             for z in notuniq:
#                 tt = ",".join(
#                     [list(m.values())[0] for m in x if list(m.keys())[0] == z]
#                 )
#                 toadd = {z: tt}
#                 uu = [v for v in x if list(v.keys())[0] not in z]
#                 uu.append(toadd)
#             output.append(uu)
#         else:
#             output.append(x)

#     df = pd.DataFrame([{k: v for d in R for k, v in d.items()} for R in output])
#     return df[[list(x.keys())[0] for x in allnodes[0]]]


# def _get_text_single(x):
#     vals = [x.text]
#     keys = [x.tag.split("}")[1]]
#     return dict(zip(keys, vals))


# def getitistermsfromcommonname(x, **kwargs):
#     """
#     Get itis terms from common names

#     Usage::

#         from pytaxize import itis
#         itis.getitistermsfromcommonname("buya")
#     """
#     return _itisterms(endpt="getITISTermsFromCommonName", args={"srchKey": x}, **kwargs)


# def getitisterms(x, **kwargs):
#     """
#     Get itis terms

#     Usage::

#         from pytaxize import itis
#         # fails
#         itis.getitisterms("bear")
#     """
#     return _itisterms(endpt="getITISTerms", args={"srchKey": x}, **kwargs)


# def getitistermsfromscientificname(x, **kwargs):
#     """
#     Get itis terms from scientific names

#     Usage::

#         from pytaxize import itis
#         itis.getitistermsfromscientificname("ursidae")
#         itis.getitistermsfromscientificname("Ursus")
#     """
#     return _itisterms(
#         endpt="getITISTermsFromScientificName", args={"srchKey": x}, **kwargs
#     )


# def hierarchy(tsn=None, what="full"):
#     """
#     Get hierarchies from TSN values, full, upstream only, or immediate downstream
#     only. Uses the ITIS database.

#     :param tsn: One or more TSN's (taxonomic serial number)
#     :param what: One of full (full hierarchy), up (immediate upstream), or down
#        (immediate downstream)

#     Details Note that `itis.itis_downstream` gets taxa downstream to a particular
#        rank, whilc this function only gets immediate names downstream.

#     Usage::

#         from pytaxize import itis
#         # Get full hierarchy
#         itis.hierarchy(tsn=180543)

#         # Get hierarchy upstream
#         itis.hierarchy(tsn=180543, "up")

#         # Get hierarchy downstream
#         itis.hierarchy(tsn=180543, "down")

#         # Many tsn's
#         itis.hierarchy(tsn=[180543,41074,36616])
#     """
#     tsn2 = convertsingle(tsn)
#     temp = []
#     if what == "full":
#         for i in range(len(tsn2)):
#             temp.append(getfullhierarchyfromtsn(tsn2[i]))
#     elif what == "up":
#         for i in range(len(tsn2)):
#             temp.append(gethierarchyupfromtsn(tsn2[i]))
#     else:
#         for i in range(len(tsn2)):
#             temp.append(gethierarchydownfromtsn(tsn2[i]))
#     return temp


# def getjurisdictionaloriginfromtsn(tsn, **kwargs):
#     """
#     Get jurisdictional origin from tsn

#     Usage::

#         from pytaxize import itis
#         itis.getjurisdictionaloriginfromtsn(180543)
#     """
#     out = Refactor(
#         itis_base + "getJurisdictionalOriginFromTSN",
#         payload={"tsn": tsn},
#         request="get",
#     ).json(**kwargs)
#     ns = {"ax21": "http://data.itis_service.itis.usgs.gov/xsd"}
#     toget = ["jurisdictionValue", "origin", "updateDate"]
#     return _itis_parse(toget, out, ns)


# def getjurisdictionoriginvalues(**kwargs):
#     """
#     Get jurisdiction origin values

#     Usage::

#         from pytaxize import itis
#         itis.getjurisdictionoriginvalues()
#     """
#     out = Refactor(
#         itis_base + "getJurisdictionalOriginValues", payload={}, request="get"
#     ).json(**kwargs)
#     ns = {"ax23": "http://metadata.itis_service.itis.usgs.gov/xsd"}
#     matches = ["jurisdiction", "origin"]
#     return _itisdf(out, ns, matches, matches, "ax23")


# def getjurisdictionvalues(**kwargs):
#     """
#     Get possible jurisdiction values

#     Usage::

#         from pytaxize import itis
#         itis.getjurisdictionvalues()
#     """
#     out = Refactor(itis_base + "getJurisdictionValues", payload={}, request="get").xml(
#         **kwargs
#     )
#     vals = [x.text for x in out.getchildren()[0].getchildren()]
#     return pd.DataFrame(vals, columns=["jurisdictionValues"])


# def getkingdomnamefromtsn(tsn, **kwargs):
#     """
#     Get kingdom names from tsn

#     Usage::

#         from pytaxize import itis
#         itis.getkingdomnamefromtsn(202385)
#     """
#     out = _itisGET("getKingdomNameFromTSN", {"tsn": tsn}, **kwargs)
#     out = Refactor(
#         itis_base + "getKingdomNameFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     ns = {"ax21": "http://data.itis_service.itis.usgs.gov/xsd"}
#     toget = ["kingdomId", "kingdomName", "tsn"]
#     return _itis_parse(toget, out, ns)


# def getkingdomnames(**kwargs):
#     """
#     Get all possible kingdom names

#     Usage::

#         from pytaxize import itis
#         itis.getkingdomnames()
#     """
#     out = Refactor(itis_base + "getKingdomNames", payload={}, request="get").xml(
#         **kwargs
#     )
#     ns = {"ax23": "http://metadata.itis_service.itis.usgs.gov/xsd"}
#     matches = ["kingdomId", "kingdomName", "tsn"]
#     return _itisdf(out, ns, matches, _tolower(matches), "ax23")


# def getlastchangedate(**kwargs):
#     """
#     Provides the date the ITIS database was last updated.

#     Usage::

#         from pytaxize import itis
#         itis.getlastchangedate()
#     """
#     out = Refactor(itis_base + "getLastChangeDate", payload={}, request="get").xml(
#         **kwargs
#     )
#     ns = {"ax23": "http://metadata.itis_service.itis.usgs.gov/xsd"}
#     nodes = out.xpath("//ax23:updateDate", namespaces=ns)
#     bb = nodes[0].text
#     dt = time.strptime(bb.split()[0], "%Y-%m-%d")
#     return dt


# def getlsidfromtsn(tsn, **kwargs):
#     """
#     Gets the unique LSID for the TSN, or an empty result if there is no match.

#     Usage::

#         from pytaxize import itis
#         # valid TSN
#         itis.getlsidfromtsn(155166)
#         # invalid TSN, returns nothing
#         itis.getlsidfromtsn(0)
#     """
#     out = _itisGET("getLSIDFromTSN", {"tsn": tsn}, **kwargs)
#     out = Refactor(
#         itis_base + "getLSIDFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     tt = out.getchildren()[0].text
#     if tt is None:
#         tt = "no match"
#     else:
#         pass
#     return tt


# def getothersourcesfromtsn(tsn, **kwargs):
#     """
#     Returns a list of the other sources used for the TSN.

#     Usage::

#         from pytaxize import itis
#         itis.getothersourcesfromtsn(182662)
#     """
#     out = Refactor(
#         itis_base + "getOtherSourcesFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     toget = [
#         "acquisitionDate",
#         "name",
#         "referredTsn",
#         "source",
#         "sourceType",
#         "updateDate",
#         "version",
#     ]
#     return _itis_parse_2dict(toget, out, ns21)


# def getparenttsnfromtsn(tsn, **kwargs):
#     """
#     Returns the parent TSN for the entered TSN.

#     Usage::

#         from pytaxize import itis
#         itis.getparenttsnfromtsn(202385)
#     """
#     out = Refactor(
#         itis_base + "getParentTSNFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     toget = ["parentTsn", "tsn"]
#     return _itis_parse(toget, out, ns21)


# def getpublicationsfromtsn(tsn, **kwargs):
#     """
#     Returns a list of the pulications used for the TSN.

#     Usage::

#         from pytaxize import itis
#         itis.getpublicationsfromtsn(70340)
#     """
#     out = Refactor(
#         itis_base + "getPublicationsFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     toget = [
#         "actualPubDate",
#         "isbn",
#         "issn",
#         "listedPubDate",
#         "pages",
#         "pubComment",
#         "pubName",
#         "pubPlace",
#         "publisher",
#         "referenceAuthor",
#         "name",
#         "refLanguage",
#         "referredTsn",
#         "title",
#         "updateDate",
#     ]
#     return _itis_parse(toget, out, ns21)


# def getranknames(**kwargs):
#     """
#     Provides a list of all the unique rank names contained in the database and
#     their kingdom and rank ID values.

#     Usage::

#         from pytaxize import itis
#         itis.getranknames()
#     """
#     out = Refactor(itis_base + "getRankNames", payload={}, request="get").json(**kwargs)
#     matches = ["kingdomName", "rankId", "rankName"]
#     return _itisdf(out, ns23, matches, _tolower(matches), "ax23")


# def getrecordfromlsid(lsid, **kwargs):
#     """
#     Gets the partial ITIS record for the TSN in the LSID, found by comparing the
#     TSN in the search key to the TSN field. Returns an empty result set if
#     there is no match or the TSN is invalid.

#     Usage::

#         from pytaxize import itis
#         itis.getrecordfromlsid("urn:lsid:itis.gov:itis_tsn:180543")
#     """
#     out = Refactor(
#         itis_base + "getRecordFromLSID", payload={"lsid": lsid}, request="get"
#     ).json(**kwargs)
#     toget = [
#         "authorship",
#         "genusPart",
#         "infragenericEpithet",
#         "infraspecificEpithet",
#         "lsid",
#         "nameComplete",
#         "nomenclaturalCode",
#         "rank",
#         "rankString",
#         "specificEpithet",
#         "uninomial",
#         "tsn",
#     ]
#     return _itis_parse(toget, out, ns21)


# def getreviewyearfromtsn(tsn, **kwargs):
#     """
#     Returns the review year for the TSN.

#     Usage::

#         from pytaxize import itis
#         itis.getreviewyearfromtsn(180541)
#     """
#     out = Refactor(
#         itis_base + "getReviewYearFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     toget = ["rankId", "reviewYear", "tsn"]
#     return _itis_parse(toget, out, ns21)


# def getscientificnamefromtsn(tsn, **kwargs):
#     """
#     Returns the scientific name for the TSN. Also returns the component parts
#     (names and indicators) of the scientific name.

#     Usage::

#         from pytaxize import itis
#         itis.getscientificnamefromtsn(531894)
#     """
#     out = Refactor(
#         itis_base + "getScientificNameFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     toget = [
#         "combinedName",
#         "unitInd1",
#         "unitInd3",
#         "unitName1",
#         "unitName2",
#         "unitName3",
#         "tsn",
#     ]
#     return _itis_parse(toget, out, ns21)


# def getsynonymnamesfromtsn(tsn, **kwargs):
#     '''
#     Returns a list of the synonyms (if any) for the TSN.

#     Usage::

#     itis.getsynonymnamesfromtsn(183671) # tsn not accepted
#     itis.getsynonymnamesfromtsn(526852) # tsn accepted
#     '''
#     out = _itisGET("getSynonymNamesFromTSN", {'tsn': tsn}, **kwargs)
#     if len(sapply(nodes, xmlValue)) == 0):
#         name = list("nomatch")
#     else:
#         name = sapply(nodes, xmlValue)
#     nodes = getNodeSet(out, "//ax21:tsn", namespaces=ns21)

#     if len(sapply(nodes, xmlValue)) == 1):
#         tsn = sapply(nodes, xmlValue)
#     else:
#       tsn = sapply(nodes, xmlValue)
#       tsn = tsn[-1]
#     data.frame(name=name, tsn=tsn, stringsAsFactors = FALSE)


# def gettaxonauthorshipfromtsn(tsn, **kwargs):
#     """
#     Returns the author information for the TSN.

#     Usage::

#         from pytaxize import itis
#         itis.gettaxonauthorshipfromtsn(183671)
#     """
#     out = Refactor(
#         itis_base + "getTaxonAuthorshipFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     toget = ["authorship", "updateDate", "tsn"]
#     return _itis_parse(toget, out, ns21)


# def gettaxonomicusagefromtsn(tsn, **kwargs):
#     """
#     Returns the usage information for the TSN.

#     Usage::

#         from pytaxize import itis
#         itis.gettaxonomicusagefromtsn(526852)
#     """
#     out = Refactor(
#         itis_base + "getTaxonomicUsageFromTSN", payload={"tsn": tsn}, request="get"
#     ).json(**kwargs)
#     toget = ["taxonUsageRating", "tsn"]
#     return _itis_parse(toget, out, ns21)


# def gettsnbyvernacularlanguage(language, **kwargs):
#     """
#     Get tsn by vernacular language not the international language code (character)

#     Usage::

#         from pytaxize import itis
#         itis.gettsnbyvernacularlanguage("french")
#     """
#     out = Refactor(
#         itis_base + "getTsnByVernacularLanguage",
#         payload={"language": language},
#         request="get",
#     ).json(**kwargs)
#     matches = ["commonName", "language", "tsn"]
#     return _itisdf(out, ns21, matches, _tolower(matches))


# def gettsnfromlsid(lsid, **kwargs):
#     """
#     Gets the TSN corresponding to the LSID, or an empty result if there is no match.

#     Usage::

#         from pytaxize import itis
#         itis.gettsnfromlsid(lsid="urn:lsid:itis.gov:itis_tsn:28726")
#         itis.gettsnfromlsid("urn:lsid:itis.gov:itis_tsn:0")
#     """
#     out = Refactor(
#         itis_base + "getTSNFromLSID", payload={"lsid": lsid}, request="get"
#     ).json(**kwargs)
#     tt = out.getchildren()[0].text
#     if tt is None:
#         tt = "no match"
#     else:
#         pass
#     return tt


# def getunacceptabilityreasonfromtsn(tsn, **kwargs):
#     """
#     Returns the unacceptability reason, if any, for the TSN.

#     Usage::

#         from pytaxize import itis
#         itis.getunacceptabilityreasonfromtsn(183671)
#     """
#     out = Refactor(
#         itis_base + "getUnacceptabilityReasonFromTSN",
#         payload={"tsn": tsn},
#         request="get",
#     ).json(**kwargs)
#     toget = ["tsn", "unacceptReason"]
#     return _itis_parse(toget, out, ns21)


# def getvernacularlanguages(**kwargs):
#     """
#     Provides a list of the unique languages used in the vernacular table.

#     Usage::

#         from pytaxize import itis
#         itis.getvernacularlanguages()
#     """
#     out = Refactor(itis_base + "getVernacularLanguages", payload={}, request="get").xml(
#         **kwargs
#     )
#     matches = ["languageNames"]
#     return _itisdf(out, ns23, matches, _tolower(matches), "ax23")


# def searchbycommonname(x, **kwargs):
#     """
#     Search for tsn by common name

#     Usage::

#         from pytaxize import itis
#         itis.searchbycommonname(x="american bullfrog")
#         itis.searchbycommonname("ferret-badger")
#         itis.searchbycommonname("polar bear")
#     """
#     out = Refactor(
#         itis_base + "searchByCommonName", payload={"srchKey": x}, request="get"
#     ).json(**kwargs)
#     matches = ["commonName", "language", "tsn"]
#     tmp = out.xpath("//ax21:commonNames", namespaces=ns21)
#     return _itisdf(tmp[0], ns21, matches, _tolower(matches))


# def searchbycommonnamebeginswith(x, **kwargs):
#     """
#     Search for tsn by common name beginning with

#     Usage::

#         from pytaxize import itis
#         itis.searchbycommonnamebeginswith("inch")
#     """
#     out = Refactor(
#         itis_base + "searchByCommonNameBeginsWith",
#         payload={"srchKey": x},
#         request="get",
#     ).json(**kwargs)
#     matches = ["commonName", "language", "tsn"]
#     tmp = out.xpath("//ax21:commonNames", namespaces=ns21)
#     return _itisdf(tmp[0], ns21, matches, _tolower(matches))


# def searchbycommonnameendswith(x, **kwargs):
#     """
#     Search for tsn by common name ending with

#     Usage::

#         from pytaxize import itis
#         itis.searchbycommonnameendswith("snake")
#     """
#     out = Refactor(
#         itis_base + "searchByCommonNameEndsWith", payload={"srchKey": x}, request="get"
#     ).json(**kwargs)
#     matches = ["commonName", "language", "tsn"]
#     tmp = out.xpath("//ax21:commonNames", namespaces=ns21)
#     return _itisdf(tmp[0], ns21, matches, _tolower(matches))


# def searchcommon(x, which="begin", **kwargs):
#     """
#     Searches common name and acts as thin wrapper around
#     `itis.searchbycommonnamebeginswith` and `itis.searchbycommonnameendswith`

#     Usage::

#         from pytaxize import itis
#         itis.searchcommon("inch")
#         itis.searchcommon("inch", which = "end")
#     """
#     if which == "begin":
#         return searchbycommonnamebeginswith(x, **kwargs)
#     else:
#         return searchbycommonnameendswith(x, **kwargs)


# def searchbyscientificname(x, **kwargs):
#     """
#     Search by scientific name

#     Usage::

#         from pytaxize import itis
#         itis.searchbyscientificname(x="Tardigrada")
#         itis.searchbyscientificname("Quercus douglasii")
#     """
#     out = Refactor(
#         itis_base + "searchByScientificName", payload={"srchKey": x}, request="get"
#     ).json(**kwargs)
#     matches = ["combinedName", "tsn"]
#     return _itisdf(out, ns21, matches, _tolower(matches))


# def searchforanymatch(x, **kwargs):
#     """
#     Search for any match

#     Usage::

#         from pytaxize import itis
#         itis.searchforanymatch(x=202385)
#         itis.searchforanymatch(x="dolphin")
#     """
#     out = Refactor(
#         itis_base + "searchForAnyMatch", payload={"srchKey": x}, request="get"
#     ).json(**kwargs)
#     # if isinstance(x, basestring):
#     tmp = out.getchildren()[0].getchildren()
#     output = []
#     for v in tmp:
#         tmp = v.getchildren()
#         for w in tmp:
#             output.append(
#                 dict(zip([gettag(e) for e in w.iter()], [e.text for e in w.iter()]))
#             )
#     return output


# def searchforanymatchpaged(x, pagesize, pagenum, ascend, **kwargs):
#     """
#     Search for any matched page for descending (logical)

#     Usage::

#         from pytaxize import itis
#         itis.searchforanymatchpaged(x=202385, pagesize=100, pagenum=1, ascend=False)
#         itis.searchforanymatchpaged("Zy", pagesize=100, pagenum=1, ascend=False)
#     """
#     args = {"srchKey": x, "pageSize": pagesize, "pageNum": pagenum, "ascend": ascend}
#     out = Refactor(
#         itis_base + "searchForAnyMatchPaged", payload=args, request="get"
#     ).json(**kwargs)
#     tmp = out.getchildren()[0].getchildren()
#     output = []
#     for v in tmp:
#         tmp = v.getchildren()
#         for w in tmp:
#             output.append(
#                 dict(zip([gettag(e) for e in w.iter()], [e.text for e in w.iter()]))
#             )
#     return output


## helper functions and variables
def convertsingle(x):
    if x.__class__.__name__ == "int":
        return [x]
    else:
        return x


ns21 = {"ax21": "http://data.itis_service.itis.usgs.gov/xsd"}
ns23 = {"ax23": "http://metadata.itis_service.itis.usgs.gov/xsd"}


def _parse2df(obj, ns):
    nodes = obj.xpath("//ax21:*", namespaces=ns)
    vals = [x.text for x in nodes]
    keys = [x.tag.split("}")[1] for x in nodes]
    df = [dict(zip(keys, vals))]
    return df


def _parse_nodes(obj):
    vals = [x.text for x in obj]
    keys = [x.tag.split("}")[1] for x in obj]
    return dict(zip(keys, vals))


def _parse_hier(obj, ns):
    nodes = obj.xpath("//ax21:hierarchyList", namespaces=ns)
    uu = []
    for i in range(len(nodes)):
        uu.append(
            dict(
                zip(
                    [
                        "tsn",
                        "author",
                        "parentName",
                        "parentTsn",
                        "rankName",
                        "taxonName",
                    ],
                    [x.text for x in nodes[i]],
                )
            )
        )
    return uu


def _itisdf(a, b, matches, colnames, pastens="ax21"):
    prefix = "//%s:" % pastens
    matches = [prefix + x for x in matches]
    output = []
    for m in matches:
        nodes = a.xpath(m, namespaces=b)
        output.append([x.text for x in nodes])
    if len(nodes) == 0:
        sys.exit("Please enter a valid search name")
    if not len(output[0]) == len(output[-1]):
        # for some reason, the list of tsn's sometimes begins with a
        # spurious None
        output[-1] = output[-1][1:]
    df = pd.DataFrame(list(zip(*output)), columns=colnames)[colnames[::-1]]
    return df


def _itisdict(a, b, matches, colnames, pastens="ax21"):
    prefix = "//%s:" % pastens
    matches = [prefix + x for x in matches]
    output = []
    for m in matches:
        nodes = a.xpath(m, namespaces=b)
        output.append([x.text for x in nodes])
    if len(nodes) == 0:
        sys.exit("Please enter a valid search name")
    return dict(zip(colnames, output))


def _itisextract(a, b, matches, colnames, pastens="ax21"):
    prefix = "//%s:" % pastens
    matches = [prefix + x for x in matches]
    output = []
    for m in matches:
        nodes = a.xpath(m, namespaces=b)
        output.append([x.text for x in nodes])
    return output


def _array2df(obj, colnames):
    if all([len(x) == 2 for x in obj]):
        df = pd.DataFrame(dict(zip(colnames, obj)))
    else:
        df = pd.DataFrame([dict(zip(colnames, obj))])
    return df


def _itis_parse(a, b, d):
    def xpathfunc(x, y, nsp):
        tmp = y.xpath("//ax21:" + x, namespaces=nsp)
        return [x.text for x in tmp]

    vals = [xpathfunc(x, b, d) for x in a]
    return dict(zip(_tolower(a), vals))
    # df = pd.DataFrame(dict(zip(_tolower(a), vals)))
    # return df


def _itis_parse_2dict(a, b, d):
    def xpathfunc(x, y, nsp):
        tmp = y.xpath("//ax21:" + x, namespaces=nsp)
        return [x.text for x in tmp]

    vals = [xpathfunc(x, b, d) for x in a]
    return dict(zip(a, vals))


def _get_text(y):
    vals = [x.text for x in y]
    keys = [x.tag.split("}")[1] for x in y]
    return dict(zip(keys, vals))


def _tolower(y):
    return [x.lower() for x in y]


def gettag(y):
    return y.tag.split("}")[1]


def _df(x, as_dataframe=False):
    if as_dataframe and pd:
        if isinstance(x, dict):
            x = [x]
        df = pd.DataFrame.from_records(x)
        return df
    else:
        return x


if __name__ == "__main__":
    import doctest

    doctest.testmod()
