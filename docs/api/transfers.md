
## Transfers
Below is the current state of functionality within the **Transfers** category. All methods within the Transfers category are stable.

<img src="https://i.imgur.com/YVVgg21.png" alt="Squads" style="height: 100px;"/>

The Transfers category contains many functions. We'll go through them in three sections: Search, Transfer List, and Transfer Targets.

---

## Search

There are two functions in the search category: search() and searchDefinition().

### fut.search()

fut.search() returns a list of dictionaries that include the information for players on the transfer market. These are returned in ascending order of seconds until expiration. just like the Web App and the console experience. [A description of the returned dict of player info is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict)  

There are many arguments available to filter your search request:
<details>
<summary>Search Arguments Table</summary><p>
<!-- alternative placement of p shown above -->


| argument    | type    | description                                                  |
|-------------|---------|--------------------------------------------------------------|
| ctype       | str     | card type (player, development, training)                    |
| level       | str     | card level (bronze, silver, gold)                            |
| category    | str     | card category (fitness, health, etc.)                        |
| assetId     | int     | unique player id                                             |
| defId       | int     | each assetId can have multiple defIds (ex. TOTW player card) |
| min_price   | int     | minimum currentBid                                           |
| max_price   | int     | maximum currentBid                                           |
| min_buy     | int     | minimum buyNow                                               |
| max_buy     | int     | maximum buyNow                                               |
| league      | int     | leagueId (available in fut.leagues)                          |
| club        | int     | clubId (available in fut.teams)                              |
| position    | str     | player preferred position abbreviation                       |
| nationality | int     | nationalityId (available in fut.nations)                     |
| rare        | boolean | TRUE if rare card                                            |
| playStyle   | int     | playStyleId (available in fut.playStyles)                    |
| start       | int     | page to start on (indexed at 0) through the web app.         |
| page_size   | str     | cards to show on one page (range between 16-50)              |


</p></details>  

*Example*:
```python
>>> fut.search(ctype='player', level = 'gold')
[{'assetId': 230621,
  'assists': 0,
  'attributeList': [{u'index': 0, u'value': 88},
   {u'index': 1, u'value': 78},
   {u'index': 2, u'value': 72},
   {u'index': 3, u'value': 88},
   {u'index': 4, u'value': 46},
   {u'index': 5, u'value': 78}],
  'bidState': None,
  'buyNowPrice': None,
  .....}]
```


### fut.searchDefinition()

fut.searchDefinition() takes one argument (*it actually takes 3 but you only need one*), `assetId`, and it returns a list of dictionaries that include the information for specific varations of player cards by assetId. [A description of the returned dict of player info is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict)  

*Example*:
```python
>>> # Get variations for Mats Hummels
>>> fut.searchDefinition(item_id=178603)
[{'tradeId': None,
'buyNowPrice': None,
'tradeState': None
...}]
```
These are returned in descending order of rating. Card IDs are distinguished by the value of the *rarecard* field. [A table of card IDs are here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#rare-cards)  

---

## Transfer List

### fut.tradepile()

fut.tradepile() returns a list of dictionaries that include the transfer information for players you've listed on the transfer market. [A description of the returned dict of transfer info is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#transfer-info-dict)  

*Example*:
```python
>>> fut.tradepile()
[{'tradeId': 16575379694,
'buyNowPrice': 1800,
'tradeState': 'closed'...}]
```

### fut.tradeStatus()

fut.tradeStatus() takes one argument (trade_id) and returns a list containing a condensed dictionary for each tradeId. [The returned dictionary is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#trade-status-dict)

*Example*:
```python
>>> fut.tradeStatus(trade_id=16575379694)
[{'tradeId': 16575379694,
'buyNowPrice': 1800,
'tradeState': 'closed',
...}]
```

### fut.sendToTradepile()

fut.sendToTradepile() takes one argument (item_id) and has an optional argument (safe) that checks the length of your tradepile to make sure you have room to store another item. The item_id argument is the `id` field in [player info dictionaries.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict) A successful send will return `True`. An unsuccessful send will return `False`if you do not own the item you're trying to send to the tradepile, or `403` if the item you're trying to send is untradeable.

*Examples*:
```python
>>> # Card I own where untradeable == False
>>> fut.sendToTradepile(item_id=117860780888)
True

>>> # Card I don't own
>>> fut.sendToTradepile(item_id=1)
False

>> # Card I own where untradeable == True
>> fut.sendToTradepile(item_id=118360247419)
{'Access-Control-Expose-Headers': 'Retry-After', 'Content-Length': '20', 'X-UnzippedLength': '0', 'Content-Encoding': 'gzip', 'Server': 'Jetty(8.0.0.M2)'}
403
...}
```

### fut.tradepileDelete()

fut.tradepileDelete() takes one argument (item_id). The item_id argument is the `id` field in [player info dictionaries.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict) A successful delete will return `True`. An unsuccessful delete will return `fut.exceptions.Conflict`if the item you're trying to delete is in an active tradestate. You will receive a `410` error if you do not own the item you're trying to delete.

*Examples*:
```python
>>> # Card in the tradepile that is not active
>>> fut.tradepileDelete(item_id=16575379694)
True

>>> # Card in the tradepile that is active.
>>> fut.tradepileDelete(item_id=16705837956)
fut.exceptions.Conflict

>> # Card I don't own
>> fut.tradepileDelete(item_id=1)
{'Content-Length': '20', 'X-UnzippedLength': '0', 'Content-Encoding': 'gzip', 'Access-Control-Expose-Headers': 'Retry-After', 'Server': 'Jetty(8.0.0.M2)'}
410
...}
```

### fut.tradepileClear()

fut.tradepileClear() takes zero arguments. It clears the `sold` items from your tradepile. It does not return anything for a successful clear, but it does return a `410` error if you don't have any `sold` items to clear from your tradepile.

```python
>>> # Check number of cards in tradepile
>>> len(fut.tradepile())
3
>>> fut.tradepileClear()
>>> len(fut.tradepile())
2

>>> # Already cleared sold cards. Trying to clear again...
>>> fut.tradepileClear()
{'Content-Length': '20', 'X-UnzippedLength': '0', 'Content-Encoding': 'gzip', 'Access-Control-Expose-Headers': 'Retry-After', 'Server': 'Jetty(8.0.0.M2)'}
410
```

### fut.relist()

fut.relist() takes zero arguments. It relists the cards in your tradepile with the previous transfer parameters (`startingBid`, `buyNow`, `duration`). The function returns a dictionary with one key: `tradeIdList`. This contains a list of the tradeIds that were succesfully relisted.

```python
>>> fut.relist()
{'tradeIdList': [16575379694]}
```

### fut.sell()  

fut.sell() takes five arguments:
* `item_id` (int): the `id` field in [player info dictionaries](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict)
* `bid` (int): the amount of coins you're willing to place the specific item/player up for starting bid (*`marketDataMinPrice`<`bid` <`marketDataMaxPrice`*)
* `buy_now` (int): the amount of coins you're willing to place the specific item/player up to buy now (*this must be higher than the starting bid*)
* `duration` (int): the amount of seconds (default 3600) to place the item/player up for transfer. (*this must be in intervals available through the web app*)
* `fast` (boolean): (default False) check the trade status of the item before listing on the transfer market

A successful listing will return the tradeId for your item.

```python
>>> # Successful listing of an item I own listed within parameters
>>> fut.sell(item_id=119119825851, bid=1000, buy_now=100000, duration=3600)
16895235756

>>> # Unsuccessful listing of an item because I don't own it
>>> fut.sell(item_id=2, bid=1000, buy_now=10000)
PermissionDenied: 461

>>> # Unsuccessful listing of an item because it is listed below marketDataMinPrice
>>> fut.sell(item_id=119119825851, bid=200, buy_now=10000)
PermissionDenied: 461

>>> # Unsuccessful listing of an item because it is listed at a bad duration
>>> fut.sell(item_id=119119825851, bid=1000, buy_now=100000, duration=3599)
PermissionDenied: 460

```


---

## Watch List

### fut.watchlist()

fut.watchlist() returns a list of dictionaries that include the transfer information for players you've bid on on the transfer market. [A description of the returned dict of transfer info is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#transfer-info-dict)  

*Example*:
```python
>>> fut.watchlist()
[{'tradeId': 16656454826,
'buyNowPrice': 5900000,
'tradeState': 'active'...
```

### fut.sendToWatchlist()

fut.sendToWatchlist() takes one argument (trade_id). The trade_id argument is the `tradeId` field in the [transfer info dictionary.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#transfer-info-dict) A successful send will return an empty dictionary (*needs to be fixed to return something*). An unsuccessful send will return `fut.exceptions.Conflict`if the card has expired from the transfer market, or `fut.exceptions.PermissionDenied: 461` if the `id` you've provided is not valid.

*Examples*:
```python
>>> # Active card on transfer market
>>> fut.sendToWatchlist(trade_id=117860780888)
{}

>> # Card that has expired or closed from transfer market
>> fut.sendToWatchlist(trade_id=118360247419)
fut.exceptions.Conflict

>>> # Ineligible card
>>> fut.sendToWatchlist(trade_id=2)
fut.exceptions.PermissionDenied: 461
```

### fut.watchlistDelete()

fut.watchlistDelete() takes one argument (trade_id). The trade_id argument is the `tradeid` field in the [transfer info dictionary.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#transfer-info-dict) A successful delete will return `True`. An unsuccessful delete will still return `True` (*needs to be updated*).

*Examples*:
```python
>>> # Card in my watchlist
>>> fut.watchlistDelete(16746617493)
True

>>> # Card not in my watchlist
>>> fut.tradepileDelete(1)
True
```
### fut.bid()  

fut.bid() takes three arguments:
* `trade_id` (int): the `tradeId` field in [transfer info dictionaries](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#transfer-info-dict)
* `bid` (int): the amount of coins you're willing to bid on the specific item/player (*must be higher than `currentBid` and `startingBid` but there is no maximum value*)
* `fast` (boolean): (default False) checks tradeStatus of item and your current coint count. this runs about 5x faster in the example for me below.

A successful bid will return True, and this player/item will be available in your watchlist. An unsucessful bid could happen for a couple of reasons: either the transfer listing has expired or someone has outbid you.

```python
>>> # Successful bid
>>> fut.sell(trade_id=16894052507, bid=150)
True

>>> # Unsuccessful bid because I bid less than the minimum amount
>>> fut.sell(trade_id=16894052507, bid=100)
False

>>> # Unsuccessful bid because the item expired or someone outbid me
>>> fut.sell(trade_id=16894049525, bid=200)
False

>>> # Checking how fast the fast-bid really is
>>> # fast=True
>>> start_time = time.time()
>>> fut.bid(trade_id=16894205969, bid=150, fast=True)
True
>>> elapsed_time = time.time() - start_time
>>> print(elapsed_time)
0.5593163967132568
>>> # fast=False
>>> start_time = time.time()
>>> fut.bid(trade_id=16894232971, bid=150, fast=False)
>>> elapsed_time = time.time() - start_time
>>> print(elapsed_time)
2.7050693035125732

```
### fut.unassigned()  

fut.unassigned() takes zero arguments. It provides player or item info for the `unassigned` items in your watchlist. These are typically items for which you paid the `buyNow` price. It returns the [player info dictionary.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict)

```python
>>> # Unassigned items
>>> fut.unassigned()
[{'assetId': 230621,
  'assists': 0,
  'attributeList': [{u'index': 0, u'value': 88}
  ...]}
 >>> # Nothing unassigned
 >>> fut.unassigned()
 []
```

### fut.sendToClub()

fut.sendToClub() takes one argument, `item_id`. The item_id argument is the `id` field in [player info dictionaries.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict) A successful send will return `True`, and an unsuccessful send will return `False`.

```python
>>> # Item I own and want to send to my club
>>> fut.sendToClub(item_id=119293105688)
True

>>> # Item I do not own
>>> fut.sendToClub(item_id=2)
False
```
