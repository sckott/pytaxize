pytaxize
=======

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