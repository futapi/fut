fut
=====

.. image:: https://travis-ci.org/oczkers/fut.png?branch=master
        :target: https://travis-ci.org/oczkers/fut

fut is a simple library for managing Fifa Ultimate Team.
It is written entirely in Python.



Documentation
-------------
Documentation will be available soon at http://fut.readthedocs.org/.

Players database: https://www.easports.com/uk/fifa/ultimate-team/fut/database

Players database (json): http://cdn.content.easports.com/fifa/fltOnlineAssets/8D941B48-51BB-4B87-960A-06A61A62EBC0/2015/fut/items/web/players.json



Usage
-----

Login
`````````````
Optional parameters:

- CODE: [string] email/sms code for two-step verification (make sure to use string if your codes starts with 0).
- PLATFORM: [pc/ps3/xbox/and/ios] pc default.
- EMULATE: [and/ios] use this feature to avoid webapp errors (BE WARE IT'S HIGH RISK).
- DEBUG: [True/False] enables debug.
- COOKIES: [filename] saves cookies after every request and load it from given file when restaring app (just like browser).

.. code-block:: python

    >>> import fut
    >>> fut = fut.Core('email', 'password', 'secret answer')

Search
`````````````
Optional parameters:

- LEVEL: ['?'/'?'/gold'] Card level.
- CATEGORY: ['fitness'/'?'] Card category.
- MIN_PRICE: [int] Minimal price.
- MAX_PRICE: [int] Maximum price.
- MIN_BUY: [int] Minimal buy now price.
- MAX_BUY: [int] Maximum buy now price.
- START: [int] Start page number.
- PAGE_SIZE: [int] Amount of cards on single page (changing this might be risky).

.. code-block:: python

    >>> items = fut.searchAuctions('development')

Bid
`````````````

.. code-block:: python

    >>> fut.bid(items[0]['trade_id'], 600)

Sell
`````````````
Optional parameters:

- BUY_NOW: [int] Buy now price.
- DURATION: [int] Auction duration in seconds (3600 default).

.. code-block:: python

    >>>     fut.sell(item['item_id'], 150)

Quick sell
`````````````
single item:
.. code-block:: python

    >>> item_id = 123456789
    >>> fut.quickSell(item_id)

multiple items:
.. code-block:: python

    >>> item_id = [123456789, 987654321]
    >>> fut.quickSell(item_id)

Piles (Watchlist / Tradepile / Unassigned / Squad)
`````````````

.. code-block:: python

    >>> items = fut.tradepile()
    >>> items = fut.unassigned()
    >>> items = fut.squad()
    >>> fut.sendToTradepile(trade_id, item_id)               # add card to tradepile
    >>> fut.sendToClub(trade_id, item_id)                    # add card to club
    >>> fut.sendToWatchlist(trade_id)                        # add card to watchlist
    >>> fut.tradepileDelete(trade_id)                        # removes item from tradepile
    >>> fut.watchlistDelete(trade_id)                        # removes item from watch list (you can pass single str/ing or list/tuple of ids - like in quickSell)

    >>> fut.tradepile_size  # tradepile size (slots)
    80
    >> len(fut.tradepile())  # tradepile fulfilment (number of cards in tradepile)
    20
    >>> fut.watchlist_size  # watchlist size (slots)
    30
    >> len(fut.watchlist())  # watchlist fulfilment (number of cards in watchlist)
    10

Credits
`````````````
It's updated automatically on every request.

.. code-block:: python

    >>> fut.credits
    600

Relist
`````````````
Relists all expired cards in tradepile.

.. code-block:: python

    >>> fut.relist()  # relist all expired cards in tradepile

Card stats and definiction IDs
`````````````
Returns stats and definition IDs for each card variation.

.. code-block:: python

    >>> fut.searchDefinition(asset_id, start=0, count=35)

Keepalive
`````````````
Send keepalive ping (you have to make at least one request every ~10 minutes to avoid session expire/logout).

.. code-block:: python

    >>> fut.keepalive()

Logout
`````````````
"""Logs out nicely (like clicking on logout button)."""
.. code-block:: python
    >>> fut.logout()



Item object (dict) structure
`````````````

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


CLI examples
------------
.. code-block:: bash

    not yet
    ...


License
-------

GNU GPLv3
