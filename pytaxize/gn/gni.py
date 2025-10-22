import sys
import requests
import json
from pytaxize.refactor import Refactor


class NoResultException(Exception):
    pass


def parse(names):
    """
    Uses the Global Names Index to parse scientific names

    :param names: List of scientific names.

    Usage::

        from pytaxize import gn
        gn.gni.parse(names = ['Cyanistes caeruleus','Helianthus annuus'])
    """
    url = "http://gni.globalnames.org/parsers.json"
    names = "|".join(names)
    params = {"names": names}
    out = Refactor(url, payload=params, request="get").json()
    return out


def search(search_term="ani*", per_page=30, page=1):
    """
    Search for names against the Global names index

    :param search_term: Search term
    :param per_page: Items to return per page
    :param page: Page to return

    Usage::

        from pytaxize import gn
        gn.gni.search(search_term = 'ani*')
    """
    url = "http://gni.globalnames.org/name_strings.json"
    params = {"search_term": search_term, "per_page": per_page, "page": page}
    out = Refactor(url, payload=params, request="get").json()
    return out


def details(id=17802847, all_records=1):
    """
    Usage::

        from pytaxize import gn
        gn.gni.details(id = 17802847)
    """
    url = "http://gni.globalnames.org/name_strings/"
    mylist = [url, str(id), ".json"]
    url2 = "".join(mylist)
    params = {"all_records": all_records}
    out = Refactor(url2, payload=params, request="get").json()
    try:
        return out
    except ValueError:
        raise NoResultException("GNI didn't return a result (id: %s)" % id)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
