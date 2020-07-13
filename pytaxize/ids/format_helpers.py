def _make_id(id_, name, rank, type_):
    uri = None
    if id_ is not None:
        uri = _make_id_uri(rank, type_, id_)

    return {"id": id_, "name": name, "rank": rank, "uri": uri}


id_uris = {
    "col": {
        "species": "http://www.catalogueoflife.org/col/details/species/id/%s",
        "other": "http://www.catalogueoflife.org/col/browse/tree/id/%s",
    },
    "ncbi": {
        "species": "https://www.ncbi.nlm.nih.gov/taxonomy/%s",
        "other": "https://www.ncbi.nlm.nih.gov/taxonomy/%s",
    },
    "itis": {
        "species": "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=%s",
        "other": "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=%s",
    },
    "gbif": {
        "species": "https://api.gbif.org/v1/species/suggest?q=%s&rank=%s",
        "other": "https://api.gbif.org/v1/species/suggest?q=%s&rank=%s",
    },
    "eol": {
        "species": "https://eol.org/api/search/1.0.json?q=%s&exact=true",
        "other": "https://eol.org/api/search/1.0.json?q=%s&exact=true",
    }
}


def _make_id_uri(rank, which, x):
    if rank is not None:
        result = id_uris[which]["species"]
        if rank.lower() != "species":
            result = id_uris[which]["other"]

        app = x
        if which == "gbif":
            app = (x, rank)

        return result % app
    else:
        return None
