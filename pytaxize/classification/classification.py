import sys
import warnings

from pytaxize.itis import hierarchy_full
from pytaxize.ncbi import hierarchy


class Classification(object):
    """
    Classification: Retrieve taxonomic hierarchy for taxonomic IDs

    Usage::

        from pytaxize import Classification

        # ITIS
        ## one id
        x = Classification(99208)
        x
        x.ids
        res = x.itis()
        res[99208]

        ## many ids - with one invalid id
        x = Classification([99208, 129313, 9999999])
        x
        x.ids
        res = x.itis()
        res[99208]
        res[129313]
        res[9999999]

        # NCBI
        x = Classification(9606)
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
            res = hierarchy_full(id)
            if res[0] is None:
                warnings.warn("No results for taxon '" + str(id) + "'")
                res = {}
            out.append(res)
        out = dict(zip(self.ids, out))
        return out

    def ncbi(self):
        res = hierarchy(self.ids)
        # out = []
        # for i in range(len(self.ids)):
        #     id = self.ids[i]
        # if res[0] is None:
        #     warnings.warn("No results for taxon '" + str(id) + "'")
        #     res = {}
        # out.append(res)
        # out = dict(zip(self.ids, out))
        return res
