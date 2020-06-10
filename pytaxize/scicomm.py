import os
import requests
import json
from multipledispatch import dispatch
from pytaxize.refactor import Refactor
from pytaxize.ids import Ids

@dispatch((str, list))
def sci2comm(x, db="ncbi"):
    """
    Get common names from scientific names.

    :param x: (str|list(str)|Ids) One or more scientific names or partial names,
        or an `Ids` object
    :param db: (str) Data source, default: "ncbi". NCBI only supported right
        now, other sources to come.
    :param \*\*kwargs: Curl options passed on to `requests.get`

    :return: dict, keys are supplied scientific names, and values
        are common names

    Remember to set your Entrez API key as `ENTREZ_KEY`

    Usage::
      
      from pytaxize import scicomm
      
      # from names (str or list of str's)
      scicomm.sci2comm('Helianthus annuus')
      scicomm.sci2comm('Puma concolor')
      scicomm.sci2comm(['Helianthus annuus', 'Poa annua'])
      scicomm.sci2comm('Gadus morhua')
      scicomm.sci2comm('Pomatomus saltatrix')
      scicomm.sci2comm('Loxodonta africana')
    
      ## no results
      ### not a real name
      scicomm.sci2comm('foo bar')
      ### good name, many id results, but no common names
      scicomm.sci2comm("Echinacea")

      # from an Ids object
      from pytaxize import Ids
      x = Ids('Helianthus annuus')
      x.ncbi()
      scicomm.sci2comm(x)
    """
    z = Ids(x)
    z.ncbi()
    out = z.ids
    res = [_ncbi_common_names(z["id"]) for w in out.values() for z in w]
    if isinstance(x, str):
        x = [x]
    return dict(zip(x, res))

@dispatch(Ids)
def sci2comm(x, db="ncbi"):
    out = x.ids
    res = [_ncbi_common_names(z["id"]) for w in out.values() for z in w]
    return dict(zip(x.name, res))

def _ncbi_common_names(x, **kwargs):
    if x is None:
      return []
    key = os.environ.get("ENTREZ_KEY")
    if key is None:
        raise Exception("ENTREZ_KEY is not defined")

    query = {"db": "taxonomy", "ID": x, "api_key": key}
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    res = Refactor(url, query, "get").xml(**kwargs)
    z = res.xpath("//TaxaSet/Taxon/OtherNames/GenbankCommonName")
    return [w.text for w in z]
