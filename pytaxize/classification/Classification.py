
import warnings
import sys
from pytaxize.itis import hierarchy_full


class NoResultException(Exception):
    pass


class Classification(object):
    """
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
        return list(map(hierarchy_full,self.ids))



