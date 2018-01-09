## Squads
Below is the current state of functionality within the **Squads** category.

One method exists to return the players on your active squad, without managers or other items. Squad management and TOTW are not included yet in the fut library.

<img src="https://i.imgur.com/UcEzzTd.png" alt="Squads" style="height: 100px;"/>

---

### fut.squad()
> arguments: (self, squad_id=0, persona_id=None)  

fut.squad() returns a list of dictionaries, each containing information about one player in your active squad. [The **player info dict** is linked here.](#player_info_dict)

*Example*:
```python
>>> len(fut.squad())
23
>>> fut.squad()
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
