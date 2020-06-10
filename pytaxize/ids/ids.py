import warnings
import sys
from ..col import search
from pytaxize.ncbi import ncbi
from ..gbif.gbif_utils import *


class NoResultException(Exception):
    pass


class Ids(object):
    """
    ids: A class for taxonomic identifiers

    Usage::

        from pytaxize import Ids

        res = Ids('Poa annua')
        res
        res.ncbi()
        # res.col() # not done yet

        res = Ids(name="Echinacea")
        res.ncbi()
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return """<%s :%s>""" % (type(self).__name__, self.name)

    def ncbi(self, verbose=True):
        """
        Get NCBI taxonomic identifiers

        Usage::

            from pytaxize import Ids
            Ids.ncbi(name = 'Poa annua')
        """
        out = []
        for i in range(len([self.name])):
            fname = [self.name][i]
            res = ncbi.search(sci_com=fname)
            if len(res[fname]) == 0:
                warnings.warn("No results for taxon '" + fname + "'")
                result = _make_id(None, fname, None, "ncbi")
            else:
                id = [x["TaxId"] for x in res[fname]]
                if len(id) == 1:
                    z = res[fname][0]
                    rank_taken = z["Rank"]
                    result = _make_id(id[0], fname, z["Rank"], "ncbi")
                if len(id) > 1:
                    result = [ _make_id(w["TaxId"], w["ScientificName"], w["Rank"], "ncbi") for w in res[fname] ]
            out.append(result)
        return out
    # def col(self, verbose=True):
    #     """
    #     Get Catalogue of Life taxonomic identifiers

    #     Usage::

    #         pytaxize.col(name = ['Poa annua'])
    #     """

    #     def fun(name, verbose):
    #         id = rank_taken = None
    #         res = col.search(name=[name])

    #         if len(res[0]) == 0:
    #             raise NoResultException("Retrieving data for taxon '" + name + "'")
    #             id = None
    #         else:
    #             res = [
    #                 dict((k, x[k]) for k in ("id", "name", "rank", "name_status"))
    #                 for x in res[0]
    #             ]
    #             id = [x["id"] for x in res]

    #         # not found on col
    #         if len(id) == 0:
    #             raise NoResultException(
    #                 "Not found. Consider checking the spelling or alternate classification"
    #             )
    #             id = None

    #         # more than one found on col -> user input
    #         if len(id) > 1:
    #             if ask:
    #                 print("\nMore than one eolid found for taxon '" + name + "'\n")
    #                 print(res)
    #                 take = input("\n Enter rownumber of taxon:\n\n")

    #                 if len(str(take)) == 0:
    #                     take = "notake"
    #                 else:
    #                     pass
    #                 if int(take) in range(len(res)):
    #                     take = int(take)
    #                     print("Input accepted, took eolid '" + id[take] + "'.\n")
    #                     id = id[take]
    #                     rank_taken = res[take]["rank"]
    #                 else:
    #                     id = None
    #                     print("\nReturned 'none'!\n\n")
    #             else:
    #                 id = "none"
    #         return {
    #             "id": id,
    #             "rank": rank_taken,
    #             "uri": _make_id_uri(rank_taken, "col", id),
    #         }

    #     out = []
    #     for i in range(len([self.name])):
    #         out.append(fun([self.name][i], verbose))

    #     return out

def _make_id(id, name, rank, type):
    if id is None:
        uri = None
    else:
        uri = _make_id_uri(rank, type, id)
    return {
        "id": id,
        "name": name,
        "rank": rank,
        "uri": uri,
    }

def _converter(x):
    if x.__class__.__name__ == "str":
        return [x]
    else:
        return x


def _flatten(x):
    return [item for sublist in x for item in sublist]

id_uris = {
    "col": {
        "species": "http://www.catalogueoflife.org/col/details/species/id/%s",
        "other": "http://www.catalogueoflife.org/col/browse/tree/id/%s",
    },
    "ncbi": {
        "species": "https://www.ncbi.nlm.nih.gov/taxonomy/%s",
        "other": "https://www.ncbi.nlm.nih.gov/taxonomy/%s",
    },
}

def _make_id_uri(rank, which, x):
    if rank is not None:
        if rank.lower() == "species":
            return id_uris[which]["species"] % x
        else:
            return id_uris[which]["other"] % x
    else:
        return None
