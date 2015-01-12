pytaxize
=======

This is a port of the R package `taxize`, found at [ropensci/taxize](https://github.com/ropensci/taxize).  There is a lot going on in the R version of this library, so it will take a while to get all the same functionality over here. 

Why?  A significant advantage of a Python version of `taxize` will be for those that are pythonistas at heart. Also, you could use `pytaxize` in a web app, whereas you could with `taxize` (e.g., in a Shiny app), but it wouldn't scale, be very fast, etc.

### Installation

```
sudo pip install git+git://github.com/sckott/pytaxize.git#egg=pytaxize
```

### Run code

```python
import pytaxize
pytaxize.gbif_parse(scientificname=['Arrhenatherum elatius var. elatius', 
	             'Secale cereale subsp. cereale', 'Secale cereale ssp. cereale',
	             'Vanessa atalanta (Linnaeus, 1758)'])
```

This code is released under the MIT license; please see LICENSE for more details.

### To do

* __Tests:__ Some tests have been written, make sure there are proper tests set up.
* Make compatible with Python 2 and 3
* Most functions in the R library `taxize` are still not here yet...
