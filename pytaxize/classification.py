import sys
import col

class Classification(object):
    '''
    Retrieve the taxonomic hierarchy for a given taxon ID.

    >>> import pytaxize
    >>>
    >>> pytaxize.Classification('Poa annua', db='col')
    '''

    def _classification(x, db=None, return_id=True, **kwargs):
      '''
      :param x: character; taxons to query.
      :param db: character; database to query. either ncbi, itis,
         eol, col, tropicos, gbif, or nbn.
      :param id: character; identifiers, returned by get_tsn, get_uid, get_eolid,
         get_colid, get_tpsid, get_gbifid.
      :param **kwargs: Curl options passed on to \linkhttr]{GET
      :param ...: Other arguments passed to get_tsn, get_uid, get_eolid,
         get_colid, get_tpsid, get_gbifid.
      :param start: The first record to return. If omitted, the results are returned
         from the first record (start=0). This is useful if the total number of
         results is larger than the maximum number of results returned by a single
         Web service query (currently the maximum number of results returned by a
         single query is 500 for terse queries and 50 for full queries).
      :param checklist: character; The year of the checklist to query, if you want a specific
         year's checklist instead of the lastest as default (numeric).
      :param key: Your API key; loads from .Rprofile.
      :param return_id: (logical) If TRUE (default), return the taxon id as well as the name
      and rank of taxa in the lineage returned.
      '''
      nstop(db)
      if db == 'col':
        id = process_ids(x, get_colid, ...)
        out = setNames(_classification_colid(id, return_id=return_id, ...), x)
      else:
        raise TypeError("The provided db value was not recognised")

      return out

    def _classification_colid(id, start=None, checklist=None, return_id=True, ...):
      def fun(x):
          if x == None:
            out = NA
          else:
            url = "http://www.catalogueoflife.org/col/webservice"
            if checklist != None:
              cc = match.arg(checklist, choices = c(2012, 2011, 2010, 2009, 2008, 2007))
              if cc %in% c(2012, 2011, 2010)):
                url = gsub("col", paste("annual-checklist/", cc, sep = ""), url)
              else:
                url = "http://webservice.catalogueoflife.org/annual-checklist/year/search.php"
                url = gsub("year", cc, url)

          args = [id = x, response = "full", start = start]
          out = getForm(url, .params = args)
          tt = xmlParse(out)

          out = data.frame(name = xpathSApply(tt, "//classification//name", xmlValue),
                            rank = xpathSApply(tt, "//classification//rank", xmlValue),
                            id  = xpathSApply(tt, "//classification//id", xmlValue),
                            stringsAsFactors = FALSE)
          # add querried taxon
          out = rbind(out, c(xpathSApply(tt, "//result/name", xmlValue),
                              xpathSApply(tt, "//result/rank", xmlValue),
                              xpathSApply(tt, "//result/id", xmlValue)))
          # Optionally return id of lineage
          if (!return_id) out = out[, c('name', 'rank')]
          return(out)

        out = lapply(id, fun)
        names(out) = id
        return structure(out, class='classification', db='col')

def nstop(x, db):
  if x == None:
    raise TypeError('Must specify %s!' % db)

def process_ids(input, fxn, ...):
  g = tryCatch(as.numeric(as.character(input)), warning=function(e) e)
  if(is(g,"numeric")){
    id = input
    class(id) = "tsn"
  } else {
    id = eval(fxn)(input, ...)
  }
  return id
