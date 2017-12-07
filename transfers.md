
## Transfers
### Current State
Below is the current state of functionality within the **Transfers** category. All methods within the Transfers category are stable. 

<img src="https://i.imgur.com/YVVgg21.png" alt="Squads" style="height: 100px;"/>

The Transfers category contains many functions. We'll go through them in three sections: Search, Transfer List, and Transfer Targets.

---

## Search

There are two functions in the search category: search() and searchDefinition(). 

### fut.search()

fut.search() returns a list of dictionaries that include the information for players on the transfer market. These are returned in ascending order of seconds until expiration. just like the Web App and the console experience. [A description of the returned dict of player info is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict)  

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

### fut.searchDefinition()

fut.searchDefinition() returns a list of dictionaries that include the information for specific varations of player cards by assetId. These are returned in descending order of rating. [A description of the returned dict of player info is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict)  

*Example*: 
```python
>>> # Get variations for Mats Hummels
>>> fut.searchDefinition(178603)
[{'tradeId': None,
'buyNowPrice': None,
'tradeState': None
...}]
``` 
These are returned in descending order of rating. Card IDs are typically distinguished by the value of the *rarecard* field. [A table of card IDs are here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md)  

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
>>> fut.tradeStatus(16575379694)
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
>>> fut.sendToTradepile(117860780888)
True

>>> # Card I don't own
>>> fut.sendToTradepile(1)
False

>> # Card I own where untradeable == True
>> fut.sendToTradepile(118360247419)
{'Access-Control-Expose-Headers': 'Retry-After', 'Content-Length': '20', 'X-UnzippedLength': '0', 'Content-Encoding': 'gzip', 'Server': 'Jetty(8.0.0.M2)'}
403
...}
```

### fut.tradepileDelete()

fut.tradepileDelete() takes one argument (item_id). The item_id argument is the `id` field in [player info dictionaries.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict) A successful delete will return `True`. An unsuccessful delete will return `fut.exceptions.Conflict`if the item you're trying to delete is in an active tradestate. You will receive a `410` error if you do not own the item you're trying to delete. 

*Examples*: 
```python
>>> # Card in the tradepile that is not active
>>> fut.tradepileDelete(16575379694)
True

>>> # Card in the tradepile that is active.
>>> fut.tradepileDelete(16705837956)
fut.exceptions.Conflict

>> # Card I don't own
>> fut.tradepileDelete(1)
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

---

## Watch List

### fut.watchlist()

fut.watchlist() returns a list of dictionaries that include the transfer information for players you've bid on on the transfer market. [A description of the returned dict of transfer info is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#transfer-info-dict)  

*Example*: 
```python
>>> fut.tradepile()
[{'tradeId': 16656454826,
'buyNowPrice': 5900000,
'tradeState': 'active'...
``` 

### fut.sendToWatchlist()

fut.sendToWatchlist() takes one argument (trade_id). The trade_id argument is the `tradeId` field in the [transfer info dictionary.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#transfer-info-dict) A successful send will return an empty dictionary (*needs to be fixed to return something*). An unsuccessful send will return `fut.exceptions.Conflict`if the card has expired from the transfer market, or `fut.exceptions.PermissionDenied: 461` if the `id` you've provided is not valid. 

*Examples*: 
```python
>>> # Active card on transfer market
>>> fut.sendToTradepile(117860780888)
{}

>> # Card that has expired or closed from transfer market
>> fut.sendToTradepile(118360247419)
fut.exceptions.Conflict

>>> # Ineligible card
>>> fut.sendToWatchlist(2)
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
