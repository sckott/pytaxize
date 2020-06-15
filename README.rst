pytaxize
========

|pypi|  |docs| |travis| |coverage| |black|

This is a port of the R package `taxize <https://github.com/ropensci/taxize>`__.  There is a lot going on in the R version of this library, so it will take a while to get all the same functionality over here.

Why?  A significant advantage of a Python version of `taxize` will be for those that are pythonistas at heart. Also, you could use `pytaxize` in a web app, whereas you could with `taxize` (e.g., in a Shiny app), but it wouldn't scale, be very fast, etc.

python 2/3
==========

pytaxize is only developed in and tested with Python 3

Installation
============

Stable from pypi

.. code-block:: console

    pip install pytaxize

Development version

.. code-block:: console

    sudo pip install git+git://github.com/sckott/pytaxize.git#egg=pytaxize


Taxonomic Ids
=============

I've started working on a class interface for taxonomic IDs, which will have a bunch of extension methods to do various things with taxon ids. What's available right now is just getting COL ids.

.. code-block:: python
    
    from pytaxize import Ids
    res = Ids('Poa annua')
    res.ncbi()
    res.ids

.. code-block:: python

    {'Poa annua': [{'id': '93036',
       'name': 'Poa annua',
       'rank': 'species',
       'uri': 'https://www.ncbi.nlm.nih.gov/taxonomy/93036'}]}

Vascan search
=============

.. code-block:: python
  
    import pytaxize
    pytaxize.vascan_search(q = ["Helianthus annuus"])

.. code-block:: python

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

Scrape taxonomic names
======================

.. code-block:: python

    out = pytaxize.scrapenames(url = 'http://www.mapress.com/zootaxa/2012/f/z03372p265f.pdf')
    out['data'][0:3]

.. code-block:: python

    [{'verbatim': '(Hemiptera:',
      'scientificName': 'Hemiptera',
      'offsetStart': 222,
      'offsetEnd': 233},
     {'verbatim': 'Sternorrhyncha:',
      'scientificName': 'Sternorrhyncha',
      'offsetStart': 234,
      'offsetEnd': 249},
     {'verbatim': 'Coccoidea:',
      'scientificName': 'Coccoidea',
      'offsetStart': 250,
      'offsetEnd': 260}]

ITIS low level functions
========================

.. code-block:: python
    
    from pytaxize import itis
    itis.accepted_names(504239)

    {'acceptedName': 'Dasiphora fruticosa',
       'acceptedTsn': '836659',
       'author': '(L.) Rydb.'}

.. code-block:: python

    itis.comment_detail(tsn=180543)

    [{'commentDetail': 'Status: CITES - Appendix I as U. arctos (Mexico, Bhutan, China, and Mongolia populations) and U. a. isabellinus; otherwise Appendix II. U. S. ESA - Endangered as U. arctos pruinosus, as U. arctos in Mexico, and as U. a. arctos in Italy. Threatened as U. a. ho...',
      'commentId': '18556',
      'commentTimeStamp': '2007-08-20 15:06:38.0',
      'commentator': 'Wilson & Reeder, eds. (2005)',
      'updateDate': '2014-02-03'},
     {'commentDetail': "Comments: Reviewed by Erdbrink (1953), Couturier (1954), Rausch (1963a), Kurtén (1973), Hall (1984) and Pasitschniak-Arts (1993). Ognev (1931) and Allen (1938) recognized U. pruinosus as distinct; not followed by Ellerman and Morrison-Scott (1951), Gao (1987), and Stroganov (1962). Lönnberg (1923b) believed that differences between pruinosus and arctos warranted subgeneric distinction as (Mylarctos) pruinosus; however, this was not supported by Pocock's (1932b) thorough revision. Synonyms allocated a...",
      'commentId': '18557',
      'commentTimeStamp': '2007-08-20 15:06:38.0',
      'commentator': 'Wilson & Reeder, eds. (2005)',
      'updateDate': '2014-02-03'}]

.. code-block:: python

    itis.hierarchy_up(tsn = 36485)

    {'author': 'Raf.',
     'parentName': 'Asteraceae',
     'parentTsn': '35420',
     'rankName': 'Genus',
     'taxonName': 'Agoseris',
     'tsn': '36485'}

Catalogue of Life
=================

.. code-block:: python
  
    from pytaxize import col
    x = col.children(name=["Apis"])
    x[0][0:3]

.. code-block:: python

    [{'id': '7a4a38c5095963949d6d6ec917d471de',
      'name': 'Apis andreniformis',
      'rank': 'Species'},
     {'id': '39610a4ceff7e5244e334a3fbc5e47e5',
      'name': 'Apis cerana',
      'rank': 'Species'},
     {'id': 'e1d4cbf3872c6c310b7a1c17ddd00ebc',
      'name': 'Apis dorsata',
      'rank': 'Species'}]

Parse names
===========

Parse names using GBIF's parser API

.. code-block:: python
    
    from pytaxize import gbif
    gbif.parse(name=['Arrhenatherum elatius var. elatius',
    	 'Secale cereale subsp. cereale', 'Secale cereale ssp. cereale',
       'Vanessa atalanta (Linnaeus, 1758)'])

.. code-block:: python

    [{'scientificName': 'Arrhenatherum elatius var. elatius',
      'type': 'SCIENTIFIC',
      'genusOrAbove': 'Arrhenatherum',
      'specificEpithet': 'elatius',
      'infraSpecificEpithet': 'elatius',
      'parsed': True,
      'parsedPartially': False,
      'canonicalName': 'Arrhenatherum elatius elatius',
      'canonicalNameWithMarker': 'Arrhenatherum elatius var. elatius',
      'canonicalNameComplete': 'Arrhenatherum elatius var. elatius',
      'rankMarker': 'var.'},
     {'scientificName': 'Secale cereale subsp. cereale',
      'type': 'SCIENTIFIC',
      ...

Contributors
============

* `Scott Chamberlain <https://github.com/sckott>`__
* `Colin Talbert <https://github.com/ColinTalbert>`__
* `akshayah3 <https://github.com/akshayah3>`__
* `panks <https://github.com/panks>`__
* `Yanghao Li <https://github.com/lyttonhao>`__
* `Ben Morris <https://github.com/bendmorris>`__
* `Bishakh Ghosh <https://github.com/ghoshbishakh>`__
* `Yoav Ram <https://github.com/yoavram>`__

Meta
====

* Please note that this project is released with a `Contributor Code of Conduct <https://github.com/sckott/pytaxize/blob/master/CONDUCT.md>`__. By participating in this project you agree to abide by its terms.
* License: MIT; see `LICENSE file <https://github.com/sckott/pytaxize/blob/master/LICENSE>`__

.. |pypi| image:: https://img.shields.io/pypi/v/pytaxize.svg
   :target: https://pypi.python.org/pypi/pytaxize

.. |docs| image:: https://readthedocs.org/projects/pytaxize/badge/?version=latest
   :target: http://pytaxize.rtfd.org/

.. |travis| image:: https://travis-ci.org/sckott/pytaxize.svg?branch=master
   :target: https://travis-ci.org/sckott/pytaxize

.. |coverage| image:: https://codecov.io/gh/sckott/pytaxize/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/sckott/pytaxize

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
