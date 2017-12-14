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

### fut.clubStaff()

fut.clubStaff() returns a dictionary of a list of dictionaries that includes the bonuses you receive from specific staff in your club. 
[This will be documented later, but here is a helpful guide to Fifa 18 Staff cards.](https://www.fifauteam.com/fifa-18-staff-cards-guide/)  

*Example*: 
```python
>>> fut.clubStaff()
{'bonus': [{'type': 'dribbling', 'value': 10},
  {'type': 'fitness', 'value': 5},
  {'type': 'gkDiving', 'value': 15},
  {'type': 'contract', 'value': 3},
  {'type': 'managerTalk', 'value': 0},
  {'type': 'physioArm', 'value': 5},
  {'type': 'physioFoot', 'value': 15},
  {'type': 'physioHip', 'value': 5}]}
``` 



