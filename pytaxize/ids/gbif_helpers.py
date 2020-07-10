from .api_urls import get_gbif_id_search_url
from ..refactor import Refactor


def process_single_species_with_gbif(name, key):
    base_url = get_gbif_id_search_url(name)
    response = safe_request(base_url)
    extracted_ids = list(map(lambda x: {"id": x.get(key, None)}, response))
    extracted_ids = list(filter(lambda x: x["id"] is not None, extracted_ids))
    return extracted_ids


def safe_request(base_url):
    try:
        return Refactor(base_url, request="get").json()["results"]
    except Exception as e:
        return {}
