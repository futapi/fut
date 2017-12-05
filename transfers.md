
## Transfers
### Current State
Below is the current state of functionality within the **Transfers** category. All methods within the Transfers category are stable. 

<img src="https://i.imgur.com/YVVgg21.png" alt="Squads" style="height: 100px;"/>

The Transfers category contains many functions. We'll go through them in three sections: Search, Transfer List, and Transfer Targets.

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

### fut.tradeStatus(tradeId)

fut.tradeStatus() takes one argument (tradeId) and returns a list containing a condensed dictionary for each tradeId. [The returned dictionary is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#trade-status-dict)

*Example*: 
```python
>>> fut.tradeStatus(16575379694)
[{'tradeId': 16575379694, 
'buyNowPrice': 1800, 
'tradeState': 'closed', 
...}]
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

