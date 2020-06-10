import sys
import requests
import json
import time
from pytaxize.refactor import Refactor
import os


class NoResultException(Exception):
    pass


def datasources():
    """
    Get data sources for the Global Names Resolver.

    Retrieve data sources used in Global Names Index, see
       http://gni.globalnames.org/ for information.

    Usage::

        # all data sources
        from pytaxize import gn
        gn.gnr.datasources()
    """
    url = "https://resolver.globalnames.org/data_sources.json"
    data = Refactor(url, payload={}, request="get").json()
    return data


def resolve(
    names="Homo sapiens",
    source=None,
    format="json",
    resolve_once="false",
    with_context="false",
    best_match_only="false",
    header_only="false",
    preferred_data_sources="false",
    http="get",
):
    """
    Uses the Global Names Resolver to resolve scientific names

    :param names: List of taxonomic names
    :param source: Source to pull from, one of x, y, z
    :param format: One of json or xml
    :param resolve_once: Logical, true or false
    :param with_context: Return context with taxonomic names
    :param best_match_only: Logical, if true (default) return the best match only
    :param header_only: Return header only, logical
    :param preferred_data_sources: Return only preferred data sources.
    :param http: The HTTP method to use, one of "get" or "post". Default="get"

    Usage::

        from pytaxize import gn
        gn.resolve('Helianthus annus')
        gn.resolve(['Helianthus annus','Poa annua'])
    """
    if names.__class__.__name__ != "list":
        return _gnr_resolve(
            names,
            source,
            format,
            resolve_once,
            with_context,
            best_match_only,
            header_only,
            preferred_data_sources,
            http,
        )

    maxlen = 1000
    # splitting list to smaller lists of size <= 1000
    names_sublists = [names[x : x + maxlen] for x in range(0, len(names), maxlen)]
    data = []
    for sublist in names_sublists:
        data.extend(
            _gnr_resolve(
                sublist,
                source,
                format,
                resolve_once,
                with_context,
                best_match_only,
                header_only,
                preferred_data_sources,
                http,
            )
        )
    if data == [[]]:
        sys.exit("No matching results to the query")

    return data


def _gnr_resolve(
    names="Homo sapiens",
    source=None,
    format="json",
    resolve_once="false",
    with_context="false",
    best_match_only="false",
    header_only="false",
    preferred_data_sources="false",
    http="get",
):

    url = "https://resolver.globalnames.org/name_resolvers"
    payload = {
        "data_source_ids": source,
        "format": format,
        "resolve_once": resolve_once,
        "with_context": with_context,
        "best_match_only": best_match_only,
        "header_only": header_only,
        "preferred_data_sources": preferred_data_sources,
    }
    if names.__class__.__name__ == "list":
        if len(names) > 300 and http == "get":
            http = "post"
        else:
            names = "|".join(names)
            payload["names"] = names
    else:
        payload["names"] = names
    if http == "get":
        result_json = Refactor(url, payload, request="get").json()
    else:
        if names.__class__.__name__ != "list":
            result_json = Refactor(url, payload, request="post").json()
        else:
            with open("names_list.txt", "w") as f:
                for name in names:
                    f.write(name + "\n")
            f.close()
            result_json = Refactor(url, payload, request="post").json(
                files={"file": open("names_list.txt", "rb")}
            )
            while result_json["status"] == "working":
                result_url = result_json["url"]
                time.sleep(10)
                result_json = Refactor(result_url, payload={}, request="get").json()

            os.remove("names_list.txt")

    data = []
    for each_result in result_json["data"]:
        data.append(each_result["results"] if "results" in each_result else [])

    return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()
