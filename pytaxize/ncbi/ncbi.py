import os
import requests
import datetime
from lxml import etree
import re
import json
import pkg_resources
from pytaxize.refactor import Refactor
from pytaxize.utils import *


def search(name, modifier=None, rank_query=None):
    """
    Search NCBI's taxonomic data - get NCBI taxonomic IDs

    :param name: The string to search for
    :param modifier: The string to search for
    :param rank_query: The string to search for

    Remember to set your Entrez API key as `ENTREZ_KEY`

    :return: dict, named with values given to `name`, 
    where each value in the dict is a list of NCBI taxonomic
    identifiers

    Usage::

        from pytaxize import ncbi

        ncbi.search(name = "Apis")

        # Many names
        ncbi.search(name=["Apis", "Puma concolor", "Pinus"])

        # Example with more than 1 result
        ncbi.search(name='Pinus')

        # common names
        ncbi.search(name = 'bear')

        # rank query
        ncbi.search(name = "Pinus", rank_query = "genus")
        ncbi.search(name = "Pinus", rank_query = "subgenus")
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
        tt = entrez("esearch", args)
        stuff = tt.xpath("IdList/Id")
        ids = [int(z.text) for z in stuff]
        if len(ids) > 1:
            ids = ",".join(map(str, ids))
        args = {"db": "taxonomy", "ID": ids, "api_key": key}
        res = entrez("esummary", args)
        return res

    name = str2list(name)
    temp = []
    for i in range(len(name)):
        temp.append(func(name[i]))
    return lists2dict(temp, name)


# def entrez(path = "esearch", args):
#     url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/%s.fcgi"
#     tt = Refactor(url, args, request = 'get').xml()
#     return tt

if __name__ == "__main__":
    import doctest

    doctest.testmod()
