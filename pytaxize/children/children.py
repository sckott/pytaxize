import warnings
import sys
from pytaxize.itis import hierarchy_down


class NoResultException(Exception):
    pass


class Children(object):
    """
    Children: Retrieve taxonomic children

    Usage::

        from pytaxize import Children
        
        # ITIS
        ## one id
        x = Children(179913)
        x
        x.ids
        x.itis()
        
        ## many ids - with one invalid id
        x = Children([179913, 174321, 9999999])
        x
        x.ids
        res = x.itis()
        res[179913]
        res[174321]
        res[9999999]

        # NCBI
        x = Children()
        x
        x.ids
        x.ncbi()
    """

    def __init__(self, ids):
        if isinstance(ids, int):
            ids = [ids]
        self.ids = ids

    def __repr__(self):
        x = """<%s>\n""" % type(self).__name__
        y = """  ids: %s""" % ",".join([str(w) for w in self.ids[:10]])
        return x + y

    def itis(self):
        out = []
        for i in range(len(self.ids)):
            id = self.ids[i]
            res = hierarchy_down(id)
            if res[0] is None:
                warnings.warn("No results for taxon '" + str(id) + "'")
                res = {}
            out.append(res)
        out = dict(zip(self.ids, out))
        return out
