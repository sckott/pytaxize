import sys
import requests
import json
import time
import os

try:
    import pandas as pd
except ImportError:
    warnings.warn("Pandas library not installed, dataframes disabled")
    pd = None


class NoResultException(Exception):
    pass


def taxo_datasources(as_dataframe=False):
    """
    Get data sources for Taxosaurus. Retrieve data sources used in
    Global Names Index, see http://taxosaurus.org/ for information.

    Usage::
    
        # all data sources
        import pytaxize
        pytaxize.taxo_datasources()

        # Output a dict
        pytaxize.taxo_datasources(False)
    """
    url = "http://taxosaurus.org/sources/"
    out = requests.get(url)
    out.raise_for_status()
    out = out.json()["sources"]
    if as_dataframe:
        data = []
        for i in range(len(out)):
            data.append([out[i]["sourceId"], out[i]["name"]])
        df = pd.DataFrame(data, columns=["id", "name"])
        return df
    else:
        return out


def taxo_resolve(query, source=None, code=None, http="get"):
    """
    Uses Taxosaurus to resolve scientific names

    :param query: List of taxonomic names
    :param source: (optional) Source to pull from
    :param code: (optional) the abbreviation for one of the nomenclature codes
        (ICZN: International Code of Zoological Nomenclature; ICN: International
        Code of Nomenclature for algae, fungi, and plants; ICNB: International
        Code of Nomenclature of Bacteria)
    :param http: (optional) The HTTP method to use, one of "get" or "post".
        Default="get"
    
    Usage::
    
        import pytaxize
        pytaxize.taxo_resolve(query='Helianthus annus')
        pytaxize.gnr_resolve(['Helianthus annus','Poa annua'])
    """
    url = "http://taxosaurus.org/submit"
    payload = {}
    if isinstance(query, list):
        if len(query) > 300 and http == "get":
            http = "post"
        else:
            query = "\n".join(query)
            payload["query"] = query
    else:
        payload["query"] = query

    if http == "get":
        out = requests.get(url, params=payload)
        token_url = out.url
    else:
        payload["source"] = source
        payload["code"] = code
        if query.__class__.__name__ != "list":
            out = requests.post(url, params=payload)
            token_url = out.url
        else:
            with open("names_list.txt", "w") as f:
                for name in query:
                    f.write(name + "\n")
            f.close()
            out = requests.post(
                url, params=payload, files={"file": open("names_list.txt", "rb")}
            )
            token_url = out.url
            os.remove("names_list.txt")

    out = requests.get(token_url)
    out.raise_for_status()
    result_json = out.json()

    while result_json["status"] == "found":
        time.sleep(10)
        out = requests.get(token_url)
        out.raise_for_status()
        result_json = out.json()
    data = []
    for each_result in result_json["names"]:
        data.append(each_result["matches"] if "matches" in each_result else [])
    if data == [[]]:
        sys.exit("No matching results to the query")
    return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()
