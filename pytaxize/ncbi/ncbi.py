import os
import requests
import datetime
from lxml import etree
import re
import json
import pkg_resources
from pytaxize.refactor import Refactor
from pytaxize.utils import *


def search(sci_com, modifier=None, rank_query=None):
    """
    Search NCBI's taxonomic data - get NCBI taxonomic IDs

    :param sci_com: list of common or scientific names
    :param modifier: A modifier to the `sci_com` given. Options include:
        Organism, Scientific Name, Common Name, All Names, Division,
        Filter, Lineage, GC, MGC, Name Tokens, Next Level, PGC, Properties,
        Rank, Subtree, Synonym, Text Word. These are not checked, so make
        sure they are entered correctly, as is.
    :param rank_query: A taxonomic rank name to modify the query sent to NCBI.
        Though note that some data sources use atypical ranks, so inspect the
        data itself for options. Optional.

    :note: Remember to set your Entrez API key as `ENTREZ_KEY`

    :return: dict, named with values given to `sci_com`,
        where each value in the dict is a list of NCBI taxonomic
        identifiers

    Usage::

        from pytaxize import ncbi

        ncbi.search(sci_com = "Apis")

        # Many names
        ncbi.search(sci_com=["Apis", "Puma concolor", "Pinus"])

        # Example with more than 1 result
        ncbi.search(sci_com='Satyrium')
        ncbi.search(sci_com=['Satyrium', 'Pinus'])

        # common names
        ncbi.search(sci_com = 'bear')
    """

    key = os.environ.get("ENTREZ_KEY")
    if key is None:
        raise Exception("ENTREZ_KEY is not defined")

    def func(name):
        name = re.sub(" ", "+", name)
        if modifier is not None:
            name = name + "[%s]" % modifier
        term = name
        if rank_query is not None:
            term = term + " AND %s[Rank]" % rank_query
        args = {"db": "taxonomy", "term": term, "api_key": key}
        tt = _entrez("esearch", args)
        stuff = tt.xpath("//IdList/Id")
        ids = [int(z.text) for z in stuff]
        if len(ids) > 1:
            ids = ",".join(map(str, ids))
        args = {"db": "taxonomy", "ID": ids, "api_key": key}
        res = _entrez("esummary", args)
        # docsums = res.xpath("//DocSum")[0].getchildren()
        docsums = res.xpath("//DocSum")
        out = []
        for x in range(len(docsums)):
            keys = [w.values()[0] for w in docsums[x][1:]]
            vals = [w.text for w in docsums[x][1:]]
            out.append(dict(zip(keys, vals)))
        return out

    sci_com = str2list(sci_com)
    temp = []
    for i in range(len(sci_com)):
        temp.append(func(sci_com[i]))
    return lists2dict(temp, sci_com)


def hierarchy(ids):
    """
    Get a full taxonomic hierarchy from NCBI

    :param ids: one or more NCBI taxonomy ids

    :note: Remember to set your Entrez API key as `ENTREZ_KEY`

    :return: dict, named with ids given to `ids`,
        where each value in the dict is a list of taxa, each
        a dict with the fields ``ScientificName``, ``Rank``, and ``TaxId``

    Usage::

        from pytaxize import ncbi
        ncbi.hierarchy(ids=9606)
        ncbi.hierarchy(ids=[9606,55062,4231])
    """
    toget = ["ScientificName", "Rank", "TaxId"]
    key = os.environ.get("ENTREZ_KEY")
    if key is None:
        raise Exception("ENTREZ_KEY is not defined")
    if not isinstance(ids, list):
        ids = [ids]
    idz = ",".join([str(x) for x in ids])
    args = {"db": "taxonomy", "ID": idz, "api_key": key}
    res = _entrez("efetch", args)
    taxa = res.xpath("//TaxaSet/Taxon")
    out = []
    for x in range(len(taxa)):
        nodes = taxa[x].xpath(".//LineageEx/Taxon")
        tmp = [
            dict(zip(toget, [node.xpath(w)[0].text for w in toget])) for node in nodes
        ]
        tmp.append(dict(zip(toget, [taxa[x].xpath(w)[0].text for w in toget])))
        out.append(tmp)
    return dict(zip(ids, out))


def _entrez(path="esearch", args={}):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/%s.fcgi" % path
    tt = Refactor(url, args, request="get").xml()
    return tt


if __name__ == "__main__":
    import doctest

    doctest.testmod()
