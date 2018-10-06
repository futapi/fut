## Squad Building Challenge
Below is the current state of functionality within the **Squad Building Challenge** category. In the [core.py file](https://github.com/futapi/fut/blob/master/fut/core.py), three more methods exist (sbsSetChallenges , sbsSquad , and sendToSbs) but do not currently work.

There is one working method in this category that GETs Squad Building Challenge info.

<img src="https://i.imgur.com/hKWXzQ2.png" alt="Squads" height = "100px"/>

---

### fut.sbsSets()

fut.sbsSets() returns a dictionary of a list of dictionaries of Squad Building Challenge categories, each containing active challenges with descriptions and other info.


```python
>>> ## General function
>>> fut.sbsSets()
{u'categories': [{u'categoryId': 8,
   u'name': u'BLACK FRIDAY',
   u'priority': 1,
   u'sets': [{u'awards': [{u'count': 1,
  .....}
>>> ## What can we pull out of the dictionary?
>>> fut.sbsSets().keys()
[u'categories']
>>> ## What are my SB challenge categories called and how many challenges are within them?
>>> for c in fut.sbsSets()['categories']:
>>> 	print c['name'], len(c['sets'])
ICONS 14
LEAGUES 6
ADVANCED 3
LIVE 4
UPGRADES 3
BASIC 3
>>> ## Give me IDs and names of all the challenges in the BASIC category
>>> # Make a generator-- this can only be used once so re-run the line below each time you use the generator
>>> basic_sbs = (s for s in fut.sbsSets()['categories'] if s['name'] == 'BASIC')
>>> for s in icons_sets:                                                         
    	for c in s['sets']:
        	print c['setId'], c['description']
1 Let's Get Started
2 League and Nation Basics
10 Let's Keep Going
```
