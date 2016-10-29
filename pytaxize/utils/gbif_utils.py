gbif_base_url = 'http://api.gbif.org/v1/species'

def gbif_name_backbone(name, rank = None, kingdom = None, phylum = None,
  clazz = None, order = None, family = None, genus = None, strict = False,
  start = None, limit = 500, **kwargs):

  url = gbif_base_url + '/match'
  args = {'name': name, 'rank': rank, 'kingdom': kingdom,
          'phylum': phylum, 'class': clazz, 'order': order, 'family': family,
          'genus': genus, 'strict': strict, 'verbose': True, 'offset': start,
          'limit': limit}
  return Refactor(url, payload=args, request='get').json()

def gbif_name_lookup(query = None, rank = None, higherTaxonKey = None, status = None,
  nameType = None, datasetKey = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c',
  limit = 500, start = None, **kwargs):

  url = gbif_base_url + '/search'
  args = {'q': query, 'rank': rank, 'higherTaxonKey': higherTaxonKey,
          'status': status, 'nameType': nameType, 'datasetKey': datasetKey,
          'limit': limit, 'offset': start}
  return Refactor(url, payload=args, request='get').json()
