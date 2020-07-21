pytaxize
========

|pypi| |travis| |coverage| |black|

This is a port of the R package `taxize <https://github.com/ropensci/taxize>`__.  There is a lot going on in the R version of this library, so it will take a while to get all the same functionality over here.

Why?  A significant advantage of a Python version of `taxize` will be for those that are pythonistas at heart. Also, you could use `pytaxize` in a web app, whereas you could with `taxize` (e.g., in a Shiny app), but it wouldn't scale, be very fast, etc.

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

ITIS
====

.. code-block:: python
    
    from pytaxize import itis
    itis.accepted_names(504239)

    {'acceptedName': 'Dasiphora fruticosa',
       'acceptedTsn': '836659',
       'author': '(L.) Rydb.'}

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
    x[0][0:2]

.. code-block:: python

    [{'id': '7a4a38c5095963949d6d6ec917d471de',
      'name': 'Apis andreniformis',
      'rank': 'Species'},
     {'id': '39610a4ceff7e5244e334a3fbc5e47e5',
      'name': 'Apis cerana',
      'rank': 'Species'}]

Modules
=======

.. toctree::
   :caption: Modules
   :hidden:

   modules/intro
   modules/ids
   modules/children
   modules/classification
   modules/scicomm
   modules/ncbi
   modules/itis
   modules/gn
   modules/col
   modules/other

:doc:`modules/intro`
    Introduction to pygbif modules.

:doc:`modules/ids`
    The Ids class

:doc:`modules/children`
    The Children class

:doc:`modules/classification`
    The Classification class

:doc:`modules/scicomm`
    Scientific to common names, and vice versa

:doc:`modules/ncbi`
    The ncbi module: NCBI methods

:doc:`modules/itis`
    The itis module: ITIS methods

:doc:`modules/gn`
    The gn module: methods for Global Names Index and Resolver

:doc:`modules/col`
    The col module: Catalogue of Life methods

:doc:`modules/other`
    Variety of other methods


All the rest
============

.. toctree::
   :caption: All the rest
   :hidden:

   changelog_link
   contributors
   contributing
   conduct
   license

:doc:`changelog_link`
    See what has changed in recent pygbif versions.

:doc:`contributors`
    pygbif contributors.

:doc:`contributing`
    Learn how to contribute to the pygbif project.

:doc:`conduct`
    Expected behavior in this community. By participating in this project you agree to abide by its terms.

:doc:`license`
    The pygbif license.

Indices and tables
------------------

* :ref:`genindex`

.. |pypi| image:: https://img.shields.io/pypi/v/pytaxize.svg
   :target: https://pypi.python.org/pypi/pytaxize

.. |travis| image:: https://travis-ci.org/sckott/pytaxize.svg?branch=master
   :target: https://travis-ci.org/sckott/pytaxize

.. |coverage| image:: https://codecov.io/gh/sckott/pytaxize/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/sckott/pytaxize

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
