pytaxize
========

|pypi| |docs| |travis| |coverage| |black|

This is a port of the R package `taxize <https://github.com/ropensci/taxize>`__.  There is a lot going on in the R version of this library, so it will take a while to get all the same functionality over here.

Why?  A significant advantage of a Python version of `taxize` will be for those that are pythonistas at heart. Also, you could use `pytaxize` in a web app, whereas you could with `taxize` (e.g., in a Shiny app), but it wouldn't scale, be very fast, etc.

Installation
============

.. code-block:: console

    sudo pip install git+git://github.com/sckott/pytaxize.git#egg=pytaxize

python or ipython, etc.

.. code-block:: python

    import pytaxize

Modules
=======

.. toctree::
   :caption: Modules
   :hidden:

   modules/intro
   modules/ids
   modules/ncbi
   modules/itis
   modules/gn
   modules/gbif
   modules/col
   modules/other

:doc:`modules/intro`
    Introduction to pygbif modules.

:doc:`modules/ids`
    The Ids class

:doc:`modules/ncbi`
    The ncbi module: NCBI methods

:doc:`modules/itis`
    The itis module: ITIS methods

:doc:`modules/gn`
    The gn module: methods for Global Names Index and Resolver

:doc:`modules/gbif`
    The gbif module: GBIF methods

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

.. |docs| image:: https://readthedocs.org/projects/pytaxize/badge/?version=latest
   :target: http://pytaxize.rtfd.org/

.. |travis| image:: https://travis-ci.org/sckott/pytaxize.svg?branch=master
   :target: https://travis-ci.org/sckott/pytaxize

.. |coverage| image:: https://coveralls.io/repos/sckott/pytaxize/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/sckott/pytaxize?branch=master

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
