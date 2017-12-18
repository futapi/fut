## Introduction

### Functionality

The fut library can perform 28 basic [REST](https://spring.io/understanding/REST) functions on your Fifa Ultimate Team. It also includes 6 properties that provide access to various FUT databases (nations, leagues, teams, stadiums, balls, players, playStyles).

---

### The FUT Web App Structure

The basic layout of the FUT Web App is below. There are 5 primary categories: Squads, Squad Building Challenge, Transfers, Store, and Club. You can perform several actions in each category with the methods available in the fut library, but not all actions in the Web App have yet been mapped out. **Click on a category below** to learn more about the methods currently available in the fut library.

[<img src="https://i.imgur.com/uvsXykU.png" alt="FUT Squads" style="height: 100px;"/>](http://futmarket.readthedocs.io/en/latest/squads/)

[<img src="https://i.imgur.com/qHZ7jMZ.png" alt="FUT SBS" style="height: 100px;"/>](http://futmarket.readthedocs.io/en/latest/squadBuildingChallenges/)

[<img src="https://i.imgur.com/yavAJma.png" alt="FUT Transfers" style="height: 100px;"/>](http://futmarket.readthedocs.io/en/latest/transfers/)

[<img src="https://i.imgur.com/oQpJmDZ.png" alt="FUT Store" style="height: 100px;"/>](https://github.com/TrevorMcCormick/futmarket/blob/master/store.md)

[<img src="https://i.imgur.com/m8WVY9X.png" alt="FUT Club" style="height: 100px;"/>](https://github.com/TrevorMcCormick/futmarket/blob/master/club.md)

---

### Other FUT databases

The fut library has the following databases inside of it. Click on the link next to each property below to view its contents.  

* **players** [Contents (*on Google Drive bc it is 18K rows*)](https://docs.google.com/spreadsheets/d/1ufH7aLh6oUh4q_M4bRP-vpbt6YFclrfeNAlkE7z01iU/edit?usp=sharing)  

* **playStyles**  [Contents](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#playstyle-ids)  

* **nations**  [Contents](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#nation-ids)  

* **leagues**  [Contents](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#league-ids)  

* **teams**  [Contents (*on Google Drive bc it is 900+ rows*)](https://docs.google.com/spreadsheets/d/1_KdX2lYJOYyhdFkEYhyT8QZuCyznMVNtuBAJo4prHWs/edit?usp=sharing)  

* **stadiums** [Contents](https://github.com/TrevorMcCormick/futmarket/blob/master/lookuptables.md#stadium-ids)  


A database for consumables (contracts, healing, fitness, training, position changes, chemistry styles, managers) has not been included in the library, but [a cookbook recipe to obtain detailed consumables information (catalogued by koolaidjones) can be found here.](https://github.com/TrevorMcCormick/futmarket/blob/master/cookbook.md#retrieve-non-player-cards).
