pytaxize
=======

This is a port of the R package `taxize`, found at [ropensci/taxize](https://github.com/ropensci/taxize).  There is a lot going on in the R version of this library, so it will take a while to get all the same functionality over here. 

Why?  A significant advantage of a Python version of `taxize` will be for those that are pythonistas at heart. Also, you could use `pytaxize` in a web app, whereas you could with `taxize` (e.g., in a Shiny app), but it wouldn't scale, be very fast, etc.

### Installation

```
sudo pip install git+git://github.com/sckott/pytaxize.git#egg=pytaxize
```

```python
# python or ipython, etc.
import pytaxize
```

### Usage

#### Vascan search

```python
pytaxize.vascan_search(q = ["Helianthus annuus"])
```

```python
{u'apiVersion': u'0.1',
 u'results': [{u'matches': [{u'canonicalName': u'Helianthus annuus',
     u'distribution': [{u'establishmentMeans': u'introduced',
       u'locality': u'NS',
       u'locationID': u'ISO 3166-2:CA-NS',
       u'occurrenceStatus': u'introduced'},
      {u'establishmentMeans': u'',
       u'locality': u'PE',
       u'locationID': u'ISO 3166-2:CA-PE',
       u'occurrenceStatus': u'excluded'},
      {u'establishmentMeans': u'',
       u'locality': u'NT',
       u'locationID': u'ISO 3166-2:CA-NT',
       u'occurrenceStatus': u'doubtful'},
      {u'establishmentMeans': u'introduced',

...cutoff
```

### Scrape taxonomic names

```python
out = pytaxize.scrapenames(url = 'http://www.mapress.com/zootaxa/2012/f/z03372p265f.pdf')
out['data'].head()
```

```python
 identifiedName  offsetEnd  offsetStart       scientificName       verbatim
0       Waxiella         14            7             Waxiella       Waxiella
1    W. africana        395          385    Waxiella africana    W. africana
2      W. egbara        581          573      Waxiella egbara      W. egbara
3  W. erithraeus        771          759  Waxiella erithraeus  W. erithraeus
4       W. gwaai        951          944       Waxiella gwaai       W. gwaai
```

### ITIS low level functions

```python
pytaxize.getacceptednamesfromtsn('208527')

'208527'
```

```python
pytaxize.getcommentdetailfromtsn(tsn=180543)

                                             comment  \
0  Status: CITES - Appendix I as U. arctos (Mexic...
1  Comments: Reviewed by Erdbrink (1953), Couturi...

                    commentator commid               commtime  updatedate
0  Wilson & Reeder, eds. (2005)  18556  2007-08-20 15:06:38.0  2014-02-03
1  Wilson & Reeder, eds. (2005)  18557  2007-08-20 15:06:38.0  2014-02-03
```

```python
pytaxize.gethierarchyupfromtsn(tsn = 36485)

  author  parentName parentTsn rankName taxonName    tsn
0   Raf.  Asteraceae     35420    Genus  Agoseris  36485
```

### Catalogue of Life

```python
pytaxize.col_children(name=["Apis"])
```

```python
[        id                name     rank
 0  6971712  Apis andreniformis  Species
 1  6971713         Apis cerana  Species
 2  6971714        Apis dorsata  Species
 3  6971715         Apis florea  Species
 4  6971716  Apis koschevnikovi  Species
 5  6845885      Apis mellifera  Species
 6  6971717    Apis nigrocincta  Species]
```

#### uBio

```python
pytaxize.ubio_search(searchName = 'elephant', sci = 1, vern = 0)
```

```python
 namebankID                nameString            fullNameString packageID  \
0    6938660  Q2VyeWxvbiBlbGVwaGFudA==  Q2VyeWxvbiBlbGVwaGFudA==        80

   packageName basionymunit rankID rankName
0  Cerylonidae      6938660     24  species
```

#### Parse names

Parse names using GBIF's parser API

```python
pytaxize.gbif_parse(scientificname=['Arrhenatherum elatius var. elatius', 
	             'Secale cereale subsp. cereale', 'Secale cereale ssp. cereale','Vanessa atalanta (Linnaeus, 1758)'])
```

```python
  authorsParsed bracketAuthorship bracketYear                  canonicalName  \
0          True               NaN         NaN  Arrhenatherum elatius elatius
1          True               NaN         NaN         Secale cereale cereale
2          True               NaN         NaN         Secale cereale cereale
3          True          Linnaeus        1758               Vanessa atalanta

                canonicalNameComplete             canonicalNameWithMarker  \
0  Arrhenatherum elatius var. elatius  Arrhenatherum elatius var. elatius
1       Secale cereale subsp. cereale       Secale cereale subsp. cereale
2       Secale cereale subsp. cereale       Secale cereale subsp. cereale
3   Vanessa atalanta (Linnaeus, 1758)                    Vanessa atalanta

    genusOrAbove infraSpecificEpithet rankMarker  \
0  Arrhenatherum              elatius       var.
1         Secale              cereale     subsp.
2         Secale              cereale     subsp.
3        Vanessa                  NaN        NaN

                       scientificName specificEpithet        type
0  Arrhenatherum elatius var. elatius         elatius  WELLFORMED
1       Secale cereale subsp. cereale         cereale  WELLFORMED
2         Secale cereale ssp. cereale         cereale     SCINAME
3   Vanessa atalanta (Linnaeus, 1758)        atalanta  WELLFORMED
```

### Get random vector of taxon names

_not working yet..._

### License

This code is released under the MIT license; please see LICENSE for more details.

### To do

* __Tests:__ Some tests have been written, make sure there are proper tests set up.
* Make compatible with Python 2 and 3
* Most functions in the R library `taxize` are still not here yet...
