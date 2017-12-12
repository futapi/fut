### Player IDs
The player IDs are found through the property fut.players. [A full table is available at this Google Drive link.](https://docs.google.com/spreadsheets/d/1ufH7aLh6oUh4q_M4bRP-vpbt6YFclrfeNAlkE7z01iU/edit?usp=sharing)

### PlayStyle IDs

<details>
<summary>PlayStyle ID Lookup Table</summary><p>
<!-- alternative placement of p shown above -->


| ID  | Description   |
|-----|---------------|
| 250 | 'BASIC'       |
| 251 |  'SNIPER'     |
| 252 |  'FINISHER'   |
| 253 |  'DEADEYE'    |
| 254 |  'MARKSMAN'   |
| 255 |  'HAWK'       |
| 256 |  'ARTIST'     |
| 257 |  'ARCHITECT'  |
| 258 |  'POWERHOUSE' |
| 259 |  'MAESTRO'    |
| 260 |  'ENGINE'     |
| 261 |  'SENTINEL'   |
| 262 |  'GUARDIAN'   |
| 263 |  'GLADIATOR'  |
| 264 |  'BACKBONE'   |
| 265 |  'ANCHOR'     |
| 266 |  'HUNTER'     |
| 267 |  'CATALYST'   |
| 268 |  'SHADOW'     |
| 269 |  'WALL'       |
| 270 |  'SHIELD'     |
| 271 |  'CAT'        |
| 272 |  'GLOVE'      |
| 273 |  'GK BASIC'   |

  </p></details>
 
### Player Info Dict  
The player info dict is returned by many functions. Below is an example with a helpful table of return types.
<details>
<summary>Player Info Dict Code Example</summary><p>
<!-- alternative placement of p shown above -->

```python
>>> #Get first player in my club
>>> fut.club()[0]
[{'assetId': 230621,
  'assists': 0,
  .......}]
```
</p></details>

<details>
<summary>Player Info Dict Lookup Table</summary><p>
<!-- alternative placement of p shown above -->

| field             | type    | description                               |
|-------------------|---------|-------------------------------------------|
| assetId           | int     | unique asset id                           |
| assists           | int     | career assists                            |
| attributeList     | dict    | five primary stats                        |
| bidState          | str     | state of bid                              |
| buyNowPrice       | int     | coins to buy now                          |
| cardType          | int     | <font color="red">unsure</font>           |
| cardsubtypeid     | int     | <font color="red">unsure</font>           |
| contract          | int     | 0-99 games                                |
| count             | ?       | None                                      |
| currentBid        | int     | coins of currentBid (0 if no bids)        |
| discardValue      | int     | coins recieved from quick sell            |
| expires           | int     | seconds until expires from transfer market|
| fitness           | int     | 0-99 fitness                              |
| formation         | str     | current team formation                    |
| id                | int     | unique card id. one asset id can have many card ids (TOTW example) |
| injuryGames       | int     | games until current injury expires        |
| injuryType        | str     | current injury type                       |
| itemState         | str     | what you can do with the current item     |
| itemType          | str     | player, development, training             |
| lastSalePrice     | int     | coins last sold for on transfer market    |
| leagueId          | int     | use fut.leagues() to get dictionary       |
| lifetimeAssists   | int     | career assists again                      |
| lifetimeStats     | dict    | all career stats                          |
| loyaltyBonus      | int     | <font color="red">unsure</font>           |
| morale            | int     | 0-99 ... not sure what this does          |
| nation            | int     | use fut.nations() to get dictionary       |
| offers            | int     | number of bids in transfer market         |
| owners            | int     | number of historical owners               |
| pile              | int     | <font color="red">unsure</font>           |
| playStyle         | int     | use fut.playStyles() to get dictionary    |
| position          | str     | preferred player position                 |
| rareflag          | int     | rare card                                 |
| rating            | int     | 0-99                                      |
| resourceGameYear  | int     | 2018                                      |
| resourceId        | int     | same as assetid                           |
| sellerEstablished | int     | <font color="red">unsure</font>           |
| sellerId          | int     | current seller on transfer market (empty) |
| sellerName        | str     | current seller on transfer market (empty) |
| startingBid       | int     | coins of the first bid on transfer market |
| statsList         | dict    | same as lifetimeStats                     |
| suspension        | int     | red card suspension games remaining       |
| teamid            | int     | use fut.teams() to get dictionary         |
| timestamp         | int     | epoch time that you acquired the item     |
| tradeId           | int     | unique tradeId on transfer market         |
| tradeState        | str     | current State on transfer market          |
| training          | int     | <font color="red">unsure</font>           |
| untradeable       | boolean | listable on the transfer market           |
| untradeableCount  | ?       | <font color="red">unsure</font>           |
| watched           | boolean | currently in watchlist                    |
| year              | int     | 2018                                      |

  </p></details>
  
### Transfer Info Dict  
The transfer info dict is returned by the tradepile and watchlist functions. Below is an example with a helpful table of return types.
<details>
<summary>Transfer Info Dict Code Example</summary><p>
<!-- alternative placement of p shown above -->

```python
>>> #Get first player in my transfers
>>> fut.tradepile()[0]
{'tradeId': 16575379694, 'buyNowPrice': 1800, 'tradeState': 'closed'....}
```
</p></details>

<details>
<summary>Transfer Info Dict Lookup Table</summary><p>
<!-- alternative placement of p shown above -->

| field              | type        | description |
|--------------------|-------------|-------------|
| tradeId            | int         | NA          |
| buNowPrice         | int         | NA          |
| tradeState         | str         | NA          |
| bidState           | str         | NA          |
| startingBid        | int         | NA          |
| id                 | int         | NA          |
| offers             | int         | NA          |
| currentBid         | int         | NA          |
| expires            | int         | NA          |
| sellerEstablished  | int         | NA          |
| sellerId           | int         | NA          |
| sellerName         | str         | NA          |
| watched            | boolean     | NA          |
| resourceId         | int         | NA          |
| discardValue       | int         | NA          |
| timestamp          | int         | NA          |
| rating             | int         | NA          |
| assetId            | int         | NA          |
| itemState          | str         | NA          |
| rareflag           | int         | NA          |
| formation          | str         | NA          |
| leagueId           | int         | NA          |
| injuryType         | str         | NA          |
| injuryGames        | int         | NA          |
| lastSalePrice      | int         | NA          |
| fitness            | int         | NA          |
| training           | int         | NA          |
| suspension         | int         | NA          |
| contract           | int         | NA          |
| position           | str         | NA          |
| playStyle          | int         | NA          |
| itemType           | str         | NA          |
| cardType           | it          | NA          |
| cardsubtypeid      | int         | NA          |
| owners             | int         | NA          |
| untradeable        | boolean     | NA          |
| morale             | int         | NA          |
| statsList          | list        | NA          |
| lifetimeStats      | list        | NA          |
| attributeList      | list(dicts) | NA          |
| teamid             | int         | NA          |
| assists            | int         | NA          |
| lifetimeAssitss    | int         | NA          |
| loyaltyBonus       | int         | NA          |
| pile               | int         | NA          |
| nation             | int         | NA          |
| year               | int         | NA          |
| resourceGameYear   | int         | NA          |
| marketDataMinPrice | int         | NA          |
| marketDataMaxPrice | int         | NA          |
| loans              | int         | NA          |

  </p></details>
  
### Trade Status Dict
The trade status dict returns basic info about a tradeId. 
<details>
<summary>Trade Status Dict Code Example</summary><p>
<!-- alternative placement of p shown above -->

```python
>>> fut.tradeStatus(16575379694)
[{'tradeId': 16575379694, 
'buyNowPrice': 1800, 
'tradeState': 'closed', 
...}]
```
</p></details>

<details>
<summary>Trade Status Dict Lookup Table</summary><p>
<!-- alternative placement of p shown above -->

| field              | type        | description |
|--------------------|-------------|-------------|
| tradeId            | int         | NA          |
| buNowPrice         | int         | NA          |
| tradeState         | str         | NA          |
| bidState           | str         | NA          |
| startingBid        | int         | NA          |
| id                 | int         | NA          |
| offers             | int         | NA          |
| currentBid         | int         | NA          |
| expires            | int         | NA          |
| sellerEstablished  | int         | NA          |
| sellerId           | int         | NA          |
| sellerName         | str         | NA          |
| watched            | boolean     | NA          |
| resourceId         | int         | NA          |
| discardValue       | int         | NA          |

  </p></details>

### Rare Cards
There are currently 41 confirmed types of rare cards.

<details>
<summary>Rare Card Lookup Table</summary><p>
<!-- alternative placement of p shown above -->

| Description  | ID |
|--------------|----|
| NONE         | 0  |
| RARE         | 1  |
| LOCK         | 2  |
| TOTW         | 3  |
| PURPLE       | 4  |
| TOTY         | 5  |
| RB           | 6  |
| GREEN        | 7  |
| ORANGE       | 8  |
| PINK         | 9  |
| TEAL         | 10 |
| TOTS         | 11 |
| LEGEND       | 12 |
| WC           | 13 |
| UNICEF       | 14 |
| OLDIMOTM     | 15 |
| FUTTY        | 16 |
| STORYMODE    | 17 |
| CHAMPION     | 18 |
| CMOTM        | 19 |
| IMOTM        | 20 |
| OTW          | 21 |
| HALLOWEEN    | 22 |
| MOVEMBER     | 23 |
| SBC          | 24 |
| SBCP         | 25 |
| PROMOA       | 26 |
| PROMOB       | 27 |
| AWARD        | 28 |
| BDAY         | 30 |
| UNITED       | 31 |
| FUTMAS       | 32 |
| RTRC         | 33 |
| PTGS         | 34 |
| FOF          | 35 |
| MARQUEE      | 36 |
| CHAMPIONSHIP | 37 |
| EUMOTM       | 38 |
| TOTT         | 39 |
| RRC          | 40 |
| RRR          | 41 |

  </p></details>
