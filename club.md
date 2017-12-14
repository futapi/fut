## Club
### Current State
Below is the current state of functionality within the **Club** category. 

Eight method exist in the Club category. 

<img src="https://i.imgur.com/vnSVPZE.png" alt="Club" style="height: 100px;"/>

---

### fut.club()

fut.club() returns a list of dictionaries that include the information for players in your club. 
[A description of the returned dict of player info is linked here.](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#player-info-dict)

There are many arguments available to filter your club search request:
<details>
<summary>Club Arguments Table</summary><p>
<!-- alternative placement of p shown above -->


| argument    | type    | description                                                        |
|-------------|---------|--------------------------------------------------------------------|
| ctype       | str     | card type (player, development, training) (default: player)        |
| defId       | int     | unique card id. one asset id can have many card ids (TOTW example) |
| start       | int     | start page on WebApp (*needs clarification*)                       |
| count       | int     | number of cards to return on one page (default 91)                 |
| level       | str     | card level (bronze, silver, gold)                                  |
| category    | str     | card category (fitness, health, etc.)                              |
| assetId     | int     | unique player id                                                   |
| league      | int     | leagueId (available in fut.leagues)                                |
| club        | int     | clubId (available in fut.teams)                                    |
| position    | str     | player preferred position abbreviation                             |
| zone        | ?       |                                                                    |
| nationality | int     | nationalityId (available in fut.nations)                           |
| rare        | boolean | default False                                                      |
| playStyle   | id      | playStyleId (available in fut.playStyles)                          |


</p></details>  
  
*Example*: 
```python
>>> fut.club()
[{'assetId': 230621,
  'assists': 1,
  'attributeList': [{u'index': 0, u'value': 88},
   {u'index': 1, u'value': 78},
   {u'index': 2, u'value': 72},
   {u'index': 3, u'value': 88},
   {u'index': 4, u'value': 46},
   {u'index': 5, u'value': 78}],
  .....}]
``` 
