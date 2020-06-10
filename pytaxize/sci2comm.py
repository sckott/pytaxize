import os
import requests
import json
from pytaxize.refactor import Refactor
from pytaxize.ids import Ids


def sci2comm(sci=None, id=None, db="ncbi", **kwargs):
    """
  Get common names from scientific names.

  :param: sci (str) One or more scientific names or partial names. optional
  :param: id (str/int) One or more taxonomic identifiers. optional
  :param: db (str) Data source, default: "ncbi". NCBI only supported right
  now, other sources to come.
  :param: **kwargs Curl options passed on to `requests.get`

  :return: dict, keys are supplied scientific names, and values
  are common names

  Remember to set your Entrez API key as `ENTREZ_KEY`

  Usage::
    
    import pytaxize

    pytaxize.sci2comm(sci='Helianthus annuus')
    pytaxize.sci2comm(sci='Puma concolor')
    pytaxize.sci2comm(sci=['Helianthus annuus', 'Poa annua'])
    pytaxize.sci2comm('Gadus morhua')
    pytaxize.sci2comm('Pomatomus saltatrix')
    pytaxize.sci2comm('Loxodonta africana')

    pytaxize.sci2comm('foo bar')
  """
    x = Ids(sci)
    out = x.ncbi()
    if len(out) > 1:
        res = [_ncbi_common_names(w["id"], **kwargs) for w in out]
    else:
        res = _ncbi_common_names(out[0]["id"], **kwargs)
    if isinstance(sci, str):
        sci = [sci]
    return dict(zip(sci, res))


def _ncbi_common_names(x, **kwargs):
    key = os.environ.get("ENTREZ_KEY")
    if key is None:
        raise Exception("ENTREZ_KEY is not defined")

    query = {"db": "taxonomy", "ID": x, "api_key": key}
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    res = Refactor(url, query, "get").xml(**kwargs)
    z = res.xpath("//TaxaSet/Taxon/OtherNames/GenbankCommonName")
    return [w.text for w in z]
