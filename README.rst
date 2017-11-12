===
fut
===

.. image:: https://img.shields.io/pypi/v/fut.svg
    :target: https://pypi.python.org/pypi/fut

.. image:: https://img.shields.io/pypi/l/fut.svg
    :target: https://pypi.python.org/pypi/fut

.. image:: https://img.shields.io/pypi/pyversions/fut.svg
    :target: https://pypi.python.org/pypi/fut

.. image:: https://travis-ci.org/futapi/fut.png?branch=master
    :target: https://travis-ci.org/futapi/fut

.. image:: https://codecov.io/github/futapi/fut/coverage.svg?branch=master
    :target: https://codecov.io/github/futapi/fut
    :alt: codecov.io

.. image:: https://api.codacy.com/project/badge/Grade/f599808fba2447c98253cf44cca86a1b
    :target: https://www.codacy.com/app/oczkers/fut?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=oczkers/fut&amp;utm_campaign=Badge_Grade

.. image:: https://cdn.worldvectorlogo.com/logos/slack.svg
    :height: 20px
    :target: https://futapi.slack.com

fut is a simple library for managing Fifa Ultimate Team.
It is written entirely in Python.

`Click here to get Slack invitation <https://gentle-everglades-93932.herokuapp.com>`_



Documentation
=============

Documentation will be available soon at http://fut.readthedocs.org/.

Players database: https://www.easports.com/uk/fifa/ultimate-team/fut/database

Players database (json): https://www.easports.com/fifa/ultimate-team/web-app/content/B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/items/web/players_meta.json

Consumables database provided by koolaidjones: https://github.com/koolaidjones/FUT-Consumables-Resource-IDs

.. image:: https://cdn.worldvectorlogo.com/logos/slack.svg
    :height: 100px
    :target: https://futapi.slack.com

`Click here to get Slack invitation <https://gentle-everglades-93932.herokuapp.com>`_


PHP ported version by InkedCurtis
---------------------------------

If You prefer php language, there is ported version made by InkedCurtis: https://github.com/InkedCurtis/FUT-API


AutoBuyer GUI
-------------

If You're looking for "user friendly" autobuyer take a look at hunterjm's project (dead probably):
https://github.com/hunterjm/futgui/releases



Usage
=====

Login
-----

Optional parameters:

- code: [string] email/sms code for two-step verification (make sure to use string if your code starts with 0).
- platform: [pc/ps3/ps4/xbox/xbox360] pc default.
- emualte: [and/ios] use this feature to avoid webapp errors (BE WARE IT'S HIGH RISK).
- debug: [True/False] enables debug.
- cookies: [filename] saves cookies after every request and load it from given file when restaring app (just like browser).
- proxies: [dict] http/socks proxies in requests's format http://docs.python-requests.org/en/master/user/advanced/#proxies

.. code-block:: python

    >>> import fut
    >>> session = fut.Core('email', 'password', 'secret answer')

Be sure to set :code:`platform=` to your platform and :code:`sms=True` if you use SMS for 2 Factor Authentication.

Search
------

Optional parameters:

- min_price: [int] Minimal price.
- max_price: [int] Maximum price.
- min_buy: [int] Minimal buy now price.
- max_buy: [int] Maximum buy now price.
- level: ['bronze'/'silver'/gold'] Card level.
- start: [int] Start page number.
- category: ['fitness'/'?'] Card category.
- assetId: [int] assetId.
- defId: [int] defId.
- league: [int] League id.
- club: [int] Club id.
- position: [int?/str?] Position.
- zone: ['attacker'/'?'] zone.
- nationality: [int] Nation id.
- rare: [boolean] True for searching special cards.
- playStyle: [str?] playStyle.
- page_size: [int] Amount of cards on single page (changing this might be risky).

.. code-block:: python

    >>> items = session.searchAuctions('development')

Bid
---

Optional parameters:

- FAST: [boolean] True for skipping trade status & credits check.

.. code-block:: python

    >>> session.bid(items[0]['trade_id'], 600)

Sell
----

Optional parameters:

- buy_now: [int] Buy now price.
- duration: [int] Auction duration in seconds (3600 default).

.. code-block:: python

    >>>     session.sell(item['item_id'], 150)
Before selling a newly-bought item, you have to send it to the tradpile. :code:`session.sendToTradepile(item_id)`

Quick sell
----------

single item:

.. code-block:: python

    >>> item_id = 123456789
    >>> session.quickSell(item_id)

multiple items:

.. code-block:: python

    >>> item_id = [123456789, 987654321]
    >>> session.quickSell(item_id)

Piles (Watchlist / Tradepile / Unassigned / Squad / Club)
---------------------------------------------------------


.. code-block:: python

    >>> items = session.tradepile()
    >>> items = session.unassigned()
    >>> items = session.squad()
    >>> items = session.club(count=10, level=10, type=1, start=0)
    >>> items = session.clubConsumablesDetails()
    >>> session.sendToTradepile(item_id)                         # add card to tradepile
    >>> session.sendToClub(trade_id, item_id)                    # add card to club
    >>> session.sendToWatchlist(trade_id)                        # add card to watchlist
    >>> session.tradepileDelete(trade_id)                        # removes item from tradepile
    >>> session.watchlistDelete(trade_id)                        # removes item from watch list (you can pass single str/ing or list/tuple of ids - like in quickSell)

    >>> session.tradepile_size  # tradepile size (slots)
    80
    >> len(session.tradepile())  # tradepile fulfilment (number of cards in tradepile)
    20
    >>> session.watchlist_size  # watchlist size (slots)
    30
    >> len(session.watchlist())  # watchlist fulfilment (number of cards in watchlist)
    10

Credits
-------

It's cached on every request so if you want the most accurate info call fut.keppalive()

.. code-block:: python

    >>> session.credits
    600

Relist
------

Relists all expired cards in tradepile.

.. code-block:: python

    >>> session.relist()  # relist all expired cards in tradepile

Apply consumable
----------------

Apply consumable on player.

- item_id: [int] Player's item_id.
- resource_id: [int] Consumable's resource_id.

.. code-block:: python

    >>> session.applyConsumable(item_id, resource_id)

Card stats and definiction IDs
------------------------------

Returns stats and definition IDs for each card variation.

.. code-block:: python

    >>> session.searchDefinition(asset_id, start=0, count=35)

Keepalive
---------

Sends keepalive ping and returns current credits amount (you have to make at least one request every ~10 minutes to avoid session expire/logout).

.. code-block:: python

    >>> session.keepalive()
    650

Logout
------

Logs out nicely (like clicking on logout button).

.. code-block:: python

    >>> session.logout()


Database
--------

Database if fully cached at first invocation so there won't by any additional requests:

.. code-block:: python

    >>> fut.nations
    >>> fut.leagues
    >>> fut.teams
    >>> fut.stadiums
    >>> fut.players
    >>> fut.playstyles

You can access database even without login:

.. code-block:: python

    >>> import fut
    >>> nations = fut.core.nations()
    >>> leagues = fut.core.leagues()
    >>> teams = fut.core.teams()
    >>> stadiums = fut.core.stadiums()
    >>> players = fut.core.players()
    >>> playestyles = fut.core.playstyles()


Convert Team/League/Nation/Player id to name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> nations[1]
    ... 'Albania'
    >>> leagues[1]
    ... 'Alka Superliga'
    >>> teams[1]
    ... 'Arsenal'
    >>> stadiums[1]
    ... 'Old Trafford'
    >>> players[1]
    ... {'rating': 88, 'lastname': 'Seaman', 'id': 1, 'firstname': 'David', 'nationality': 14, 'surname': None}
    >>> playstyles[250]
    ... 'BASIC'


Item object (dict) structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> for item in items:
    ...     trade_id = item['tradeId']
    ...     buy_now_price = item['buyNowPrice']
    ...     trade_state = item['tradeState']
    ...     bid_state = item['bidState']
    ...     starting_bid = i['startingBid']
    ...     item_id = i['id']
    ...     timestamp = i['timestamp']  # auction start
    ...     rating = i['rating']
    ...     asset_id = i['assetId']
    ...     resource_id = i['resourceId']
    ...     item_state = i['itemState']
    ...     rareflag = i['rareflag']
    ...     formation = i['formation']
    ...     injury_type = i['injuryType']
    ...     suspension = i['suspension']
    ...     contract = i['contract']
    ...     playStyle = i['playStyle']  # used only for players
    ...     discardValue = i['discardValue']
    ...     itemType = i['itemType']
    ...     owners = i['owners']
    ...     offers = i['offers']
    ...     current_bid = i['currentBid']
    ...     expires = i['expires']  # seconds left


to be continued ;-)



Problems
--------

Getting "requests.exceptions.SSLError:....'utas.mob.v4.fut.ea.com' doesn't match 'utas.mobapp.fut.ea.com'"?
^^^^
This is a new error, but here's a temporary fix to try:

1. Re-download the api from github
2. Go into fut/urls.py
3. On line 7, change :code:`auth_url = rc['authURL']` to :code:`auth_url = 'utas.mobapp.fut.ea.com'`
4. Run `python setup.py install`
5. Try your script again
6. **Please report in the Slack channel whether or not this worked!!**


Bans
^^^^

To avoid getting ban take a look at our little discussion/guide thread:
https://github.com/oczkers/fut/issues/259

Generally speaking, you should send no more than 500 requests per hour and 5000 requests per day. Be somewhat human. If you encounter a captcha, try to answer/solve it as soon as possible.

Somehow i've sent card to full tradepile and it disappeared
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make space in tradepile and just call one command to restore it:

.. code-block:: python

    session.sendToTradepile(-1, id)


I've got card with None tradeId so cannot move/trade it
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make space in tradepile and just call one command to restore it:

.. code-block:: python

    session.sendToTradepile(-1, id)


PermissionDenied exceptions raises when trying to sell cards directly from watchlist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The solution is to send the items to Tradepile and offer from there.


CLI examples
------------

.. code-block:: bash

    not yet
    ...



License
-------

GNU GPLv3
