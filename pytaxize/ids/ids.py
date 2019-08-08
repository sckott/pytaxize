import sys
from ..col import search
from ..gbif.gbif_utils import *

class NoResultException(Exception):
    pass

class Ids(object):
    '''
    ids: A class for taxonomic identifiers

    Usage::

      from pytaxize import Ids

      res = Ids('Poa annua', db='col')
      res.get_colid()
    '''
    def __init__(self, name, db):
        # super(ids, self).__init__()
        self.db = db
        self.name = name

    def __repr__(self):
      return """<%s %s:%s>""" % (type(self).__name__, self.db, self.name)

    def get_colid(self, ask = True, verbose = True):
      '''
      Get Catalogue of Life taxonomic identifiers

      Usage::

        pytaxize.get_colid(sciname=['Poa annua'])
      '''
      def fun(sciname, ask, verbose):
        id = rank_taken = None
        res = col_search(name=[sciname])

        if(len(res[0]) == 0):
          raise NoResultException("Retrieving data for taxon '" + sciname + "'")
          id = None
        else:
          res = [ dict((k, x[k]) for k in ('id', 'name', 'rank', 'name_status')) for x in res[0] ]
          id = [ x['id'] for x in res ]

        # not found on col
        if(len(id) == 0):
          raise NoResultException("Not found. Consider checking the spelling or alternate classification")
          id = None

        # more than one found on col -> user input
        if(len(id) > 1):
            if(ask):
                print("\nMore than one eolid found for taxon '" + sciname + "'\n")
                print(res)
                take = input("\n Enter rownumber of taxon:\n\n")

                if(len(str(take)) == 0):
                    take = 'notake'
                else:
                    pass
                if(int(take) in range(len(res))):
                    take = int(take)
                    print("Input accepted, took eolid '" + id[take] + "'.\n")
                    id = id[take]
                    rank_taken = res[take]['rank']
                else:
                    id = None
                    print("\nReturned 'none'!\n\n")
            else:
                id = 'none'
        return {'id': id, 'rank': rank_taken, 'uri': make_id_uri(rank_taken, 'col', id)}

      out = []
      for i in range(len([self.name])):
        out.append(fun([self.name][i], ask, verbose))

      return out

def converter(x):
    if(x.__class__.__name__ == 'str'):
        return [x]
    else:
        return x

def flatten(x):
  return [item for sublist in x for item in sublist]

id_uris = {
  'col': {
    'species': 'http://www.catalogueoflife.org/col/details/species/id/%s',
    'other': 'http://www.catalogueoflife.org/col/browse/tree/id/%s'
  }
}

def make_id_uri(rank, which, x):
  if (rank is not None):
    if (rank.lower() == "species"):
      return id_uris[which]['species'] % x
    else:
      return id_uris[which]['other'] % x
  else:
    return None
