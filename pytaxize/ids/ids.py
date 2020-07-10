import warnings
import sys
from ..col import search
from pytaxize.ncbi import ncbi
from pytaxize.itis import terms


class NoResultException(Exception):
    pass


class Ids(object):
    """
    ids: A class for taxonomic identifiers

    Usage::

        from pytaxize import Ids

        x = Ids('Poa annua')
        x
        x.name
        x.ncbi()
        x.ids
        x.db_ids
        
        # more than one result
        x = Ids(name="Echinacea")
        x.ncbi()
        x.ids
        x.ids["Echinacea"]

        # more than one name supplied
        x = Ids(name=['Helianthus annuus', 'Poa annua', 'Echinacea'])
        x
        x.ncbi()
        x
        x.ids
        x.ids["Helianthus annuus"]
        x.ids["Poa annua"]
        x.ids["Echinacea"]

        # extract just ids
        out = x.extract_ids()
        out["Echinacea"]

        # ITIS
        x = Ids("Helianthus annuus")
        x.itis(type="scientific")
        x.extract_ids()
    """

    def __init__(self, name):
        if isinstance(name, str):
            name = [name]
        self.name = name
        self.ids = {}
        self.db_ids = None

    def __repr__(self):
        x = """<%s>\n""" % type(self).__name__
        y = """  names: %s""" % ",".join(self.name[:10])
        # z = """  ids: %s""" % ",".join(self.extract_ids())
        return x + y

    def ncbi(self):
        out = []
        for i in range(len(self.name)):
            fname = self.name[i]
            res = ncbi.search(sci_com=fname)
            if len(res[fname]) == 0:
                warnings.warn("No results for taxon '" + fname + "'")
                result = [_make_id(None, fname, None, "ncbi")]
            else:
                id = [x["TaxId"] for x in res[fname]]
                if len(id) == 1:
                    z = res[fname][0]
                    result = [_make_id(id[0], fname, z["Rank"], "ncbi")]
                if len(id) > 1:
                    result = [
                        _make_id(w["TaxId"], w["ScientificName"], w["Rank"], "ncbi")
                        for w in res[fname]
                    ]
            out.append(result)
        self.db_ids = "ncbi"
        self.ids = dict(zip(self.name, out))

    # FIXME: ITIS doesn't give back ranks, ideally need ranks
    def itis(self, type="scientific"):
        out = []
        for i in range(len(self.name)):
            fname = self.name[i]
            res = terms(x=self.name, what=type)
            if len(res) == 0:
                warnings.warn("No results for taxon '" + fname + "'")
                result = [_make_id(None, fname, None, "itis")]
            else:
                id = [x["tsn"] for x in res]
                if len(id) == 1:
                    z = res[0]
                    # rank_taken = z["Rank"]
                    result = [_make_id(id[0], fname, "species", "itis")]
                if len(id) > 1:
                    result = [
                        _make_id(w["tsn"], w["scientificName"], "species", "itis")
                        for w in res
                    ]
            out.append(result)
        self.db_ids = "itis"
        self.ids = dict(zip(self.name, out))

    def db(self, db, **kwargs):
        if db == "ncbi":
            self.ncbi()
        elif db == "itis":
            self.itis(**kwargs)
        else:
            raise Exception("'db' must be either ncbi or itis")

    def extract_ids(self):
        x = self.ids
        if len(x) > 0:
            x = {k: [w["id"] for w in v] for (k, v) in x.items()}
        return x


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
    "itis": {
        "species": "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=%s",
        "other": "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=%s",
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
