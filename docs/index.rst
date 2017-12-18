.. fut documentation master file, created by
   sphinx-quickstart on Thu Jan 16 00:01:22 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fut's documentation!
===============================

Release v\ |version|. (:ref:`Installation <install>`)
[![](https://img.shields.io/pypi/v/fut.svg?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://img.shields.io/pypi/l/fut.svg?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://img.shields.io/pypi/pyversions/fut.svg?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://travis-ci.org/futapi/fut.png?branch=master?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://codecov.io/github/futapi/fut/coverage.svg?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://api.codacy.com/project/badge/Grade/f599808fba2447c98253cf44cca86a1b?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://readthedocs.org/projects/pip/badge/?version=latest)](http://fut.readthedocs.io/en/latest/)

[<img src="https://cdn.worldvectorlogo.com/logos/slack.svg" alt="slack" width="70" height="50">](https://gentle-everglades-93932.herokuapp.com)

fut is a simple Python library for managing Fifa Ultimate Team. The library enables programmatic access to the official [FUT Web App and FIFA Companion App](https://www.easports.com/fifa/ultimate-team/web-app/). If you prefer php language, there is ported version made by InkedCurtis available here: https://github.com/InkedCurtis/FUT-API.

The fut library can perform 28 basic [REST](https://spring.io/understanding/REST) functions on your Fifa Ultimate Team. It also includes 6 properties that provide access to various FUT databases (nations, leagues, teams, stadiums, balls, players, playStyles).


Feature Support
---------------

- Multi platform (pc, ps3, xbox, ios, android)
- Searching auctions with filters
- Biding
- Selling
- Quick selling
- Full control of watchlist, tradepile and unassigned cards
- Buying and opening packs
- Filling & submiting Squad Battle Chalenges (not tested yet)
- Updating credits variable on every request
- Simple keepalive function just to extend session life
- Requesting any card info without login
- Calculating baseID
- Python 2.6-3.6, PyPy


User Guide
----------

This is basic part of the documentation, it's about installation and importing.

.. toctree::
   :maxdepth: 2

   user/introduction


.. API Documentation
.. -----------------
..
.. If you are looking for information on a specific function, class or method,
.. this part of the documentation is for you.
..
.. .. toctree::
..    :maxdepth: 1
..
..    api


Contributor Guide
-----------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 1

   dev/authors
