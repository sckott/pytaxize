import json
import warnings
from pytaxize.refactor import Refactor

try:
    import pandas as pd
except ImportError:
    warnings.warn("Pandas library not installed, dataframes disabled")
    pd = None


def parse(name, as_dataframe=False):
    """
    Parse taxon names using the GBIF name parser.

    :param name: A character vector of scientific names.
        Returns a DataFrame containing fields extracted from parsed
        taxon names. Fields returned are the union of fields extracted from
        all species names in scientificname
    :param as_dataframe: (optional) Type: boolean. Return as pandas data frame?
        default: False

    Author John Baumgartner (johnbb@student.unimelb.edu.au)

    References http://dev.gbif.org/wiki/display/POR/Webservice+API,
    http://tools.gbif.org/nameparser/api.do

    Usage::

        from pytaxize import gbif
        gbif.parse(name=['x Agropogon littoralis'])
        names = ['x Agropogon littoralis', 'Helianthus annuus texanus']
        gbif.parse(names)
        gbif.parse(names, as_dataframe=True)
    """
    name = list(name)
    url = "https://api.gbif.org/v0.9/parser/name"
    headers = {"content-type": "application/json"}
    tt = Refactor(url, payload={}, request="post").json(
        data=json.dumps(name), headers=headers
    )
    if as_dataframe:
        tt = pd.DataFrame(tt)
    return tt
