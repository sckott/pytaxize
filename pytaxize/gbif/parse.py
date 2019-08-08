import pandas as pd
import json
from pytaxize.refactor import Refactor

def parse(name):
    '''
    Parse taxon names using the GBIF name parser.

    :param name: A character vector of scientific names.
      Returns a DataFrame containing fields extracted from parsed
      taxon names. Fields returned are the union of fields extracted from
      all species names in scientificname

    Author John Baumgartner (johnbb@student.unimelb.edu.au)

    References http://dev.gbif.org/wiki/display/POR/Webservice+API,
    http://tools.gbif.org/nameparser/api.do

    Usage::

        import pytaxize
        pytaxize.gbif_parse(name=['x Agropogon littoralis'])
    '''
    name = list(name)
    url = "http://api.gbif.org/v0.9/parser/name"
    headers = {'content-type': 'application/json'}
    tt = Refactor(url, payload={}, request='post').json(data=json.dumps(name), headers=headers)
    res = pd.DataFrame(tt)
    return res
