## Cookbook

### Retrieve Non-Player Cards
The non-player cards are updated as of Fifa 2017 and are hosted as a csv on github.
The function below uses the `pandas` library to provide a table of the non-player cards.
<details>
<summary>Retrieve Non-Player Cards</summary><p>
<!-- alternative placement of p shown above -->

```python
## Gets non-player card types
>>> import pandas as pd
>>> def nonPlayers():
      url = 'https://raw.githubusercontent.com/TrevorMcCormick/futmarket/master/cardInfo.csv'
      return(pd.read_csv(url))
>>> nonPlayers().head()
   amount  assetid  subtypeid  pile  rareflag  rating  weightrare  year  \
0       0        7        201     7         0      50           0  2017   
1       0        7        201     7         0      65           0  2017   
2       0        7        201     7         0      80           0  2017   
3       0        7        201     7         1      60         100  2017   
4       0        7        201     7         1      70         100  2017   
   resourceid  bronze  silver  gold   class  category   level      type  
0     5001001       8       2     1  Player  Contract  Bronze  Non-Rare  
1     5001002      10      10     8  Player  Contract  Silver  Non-Rare  
2     5001003      15      11    13  Player  Contract    Gold  Non-Rare  
3     5001004      15       6     3  Player  Contract  Bronze      Rare  
4     5001005      20      24    18  Player  Contract  Silver      Rare
```
</p></details>
