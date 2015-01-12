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

### Get random vector of taxon names

```python

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

### License

This code is released under the MIT license; please see LICENSE for more details.

### To do

* __Tests:__ Some tests have been written, make sure there are proper tests set up.
* Make compatible with Python 2 and 3
* Most functions in the R library `taxize` are still not here yet...
