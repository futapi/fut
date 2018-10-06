## Club
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

### fut.clubConsumables()

fut.clubConsumables() returns a list of dictionaries that includes the consumable cards and their details in your club.
[A table of all 2017 consumable IDs and information is available here. *2018 IDs have not yet been confirmed.*](https://docs.google.com/spreadsheets/d/1mzfX_quYxVhQ_kkmugO3gQtHwPSQnKTLVeDHiinI1jA/edit?usp=sharing)  

*Example*:
```python
>>> fut.clubConsumables()
[{'bidState': None,
  'bronze': 15,
  'buyNowPrice': None,
  'cardassetid': 7,
  'consumables': None,
  'consumablesContractManager': None,
  'consumablesContractPlayer': None,
  ...}]
```


### fut.quickSell

fut.quickSell() discards an item (`id`) in your club for its `discardValue`. It returns `True` on a successful quickSell and returns `UnknownError: b''` for an unsuccessful quickSell. Untradeable cards can be discarded even though their `discardValue` is 0.


*Example*:
```python
>>> # Card I own where untradeable == False
>>> fut.quickSell(item_id = 118917563073)
True

>>> # Card I do not own
>>> fut.quickSell(item_id = 2)
UnknownError: b''

```

### fut.applyConsumable

fut.applyConsumable() takestwo arguemtns: a consumableId (`resourceId`) that you own, and a player item_id (`id`) that you own. It doesn't return anything for a successful consumable application, but it returns `UnknownError: b''` for an unsuccessful request. *There is currently not a method to apply a team consumable.*

*Example*:
```python
>>> # Card and Consumable I own
>>> fut.applyConsumable(item_id = 119175722619, resource_id = 5001003)

>>> # Card and Consumable I do not own
>>> fut.applyConsumable(item_id = 119175722619, resource_id = 2)
UnknownError: b''
```

### fut.keepalive()

fut.keepalive() is a simple function that returns your coin count. It is also a useful API call that tells the Fifa Web App that your session is still active.

*Example*:
```python
>>> # Return my coin count
>>> fut.keepalive()
1002231023 #just kidding!
15598
```
### fut.messages()

fut.messages() returns any active messages if you have them. I don't have any examples of this but any messages that include new Kits would be in here.

### fut.objectives()

fut.objectives() returns a list of dictionaries containing your daily and weekly objectives.

*Example*:
```python
>>> fut.objectives()
{'coinsAutoClaimed': 0,
 'dailyObjectives': [{'currentProgress': 0,
   'description': 'Get on the pitch today and play a game in Online Seasons mode',
   'difficulty': 3,
   'expiryTime': 1513414800
   ...}],
 'dailyRewardsAutoClaimed': False,
 'itemsAutoClaimed': 0,
 'packsAutoClaimed': 0,
 'weeklyObjectives': [{'currentProgress': 0,
   'description': 'Win three or more Squad Battles matches this week to earn the FUTmas Elf kit [Untradeable]',
   'difficulty': 39,
   'expiryTime': 1513965600
   ...}],
  'weeklyRewardsAutoClaimed': False}
>>> # Let's say I want to see the names of all of my daily objectives
>>> for i in fut.objectives().get('dailyObjectives'):
>>>     print(i['name'])
Becoming Seasoned
Buy a Midfielder
Use your Head
Four the Bundesliga
Get Fit
```
