import sys

class Ids(object):
	'''
	ids: A class for taxonomic identifiers

	a = Ids('Poa annua', db='col')
	a.
	'''
	def __init__(self, db):
		super(ids, self).__init__()
		self.db = db

		get_colid(names, ...)

	def classification(self):
		print "shit"


def get_colid(sciname, ask = True, verbose = True):
  '''
  pytaxize.get_colid(sciname='Poa annua')
  '''
  def fun(sciname, ask, verbose):
    # mssg(verbose, "\nRetrieving data for taxon '", sciname, "'\n")
    df = col_search(name=sciname)[[1]]
    
    if(nrow(df)==0):
      # mssg(verbose, "Not found. Consider checking the spelling or alternate classification")
      id = NA
    else:
      df = df[,c('id','name','rank','status','acc_name')]
      names(df)[1] = 'colid'
      id = df$colid
    
    # not found on eol
    if(len(id) == 0):
      # mssg(verbose, "Not found. Consider checking the spelling or alternate classification")
      id = NA
    # more than one found on eol -> user input
    if(len(id) > 1):
      if(ask):
        rownames(df) = 1:nrow(df)
        # prompt
        message("\n\n")
        message("\nMore than one eolid found for taxon '", sciname, "'!\n
            Enter rownumber of taxon (other inputs will return 'NA'):\n")      
        print(df)
        take = scan(n = 1, quiet = TRUE, what = 'raw')
        
        if(len(take) == 0):
          take = 'notake'
        if(take %in% seq_len(nrow(df))):
          take = as.numeric(take)
          message("Input accepted, took eolid '", as.character(df$colid[take]), "'.\n")
          id = as.character(df$colid[take])
        else:
          id = NA
          mssg(verbose, "\nReturned 'NA'!\n\n")
        else:
          id = NA
    return id

  out = []
  for i in xrange(len(sciname)):
  	out.append(fun(sciname[i], ask, verbose))
  
  return out

def mssg(v): 
	if(v) message(...)