## IDs (object structures?)
List of ids is available below:

### Consumable IDs
Consumable IDs have been added by [Koolaidjones](https://github.com/koolaidjones/FUT-Consumables-Resource-IDs). They are updated through 2017, so some IDs may be slightly off. [The full table is availalbe at this Google Drive link.](https://docs.google.com/spreadsheets/d/1mzfX_quYxVhQ_kkmugO3gQtHwPSQnKTLVeDHiinI1jA/edit?usp=sharing)

### League IDs
Leagues are found through the property fut.leagues.
<details>
<summary>League ID Lookup Table</summary><p>
<!-- alternative placement of p shown above -->

| ID    | League                                  |
|-------|-----------------------------------------|
| 1     |  'Alka Superliga'                       |
| 4     |  'Belgium Pro League'                   |
| 7     |  'Liga do Brasil'                       |
| 10    |  'Eredivisie'                           |
| 13    |  'Premier League'                       |
| 14    |  'EFL Championship'                     |
| 16    |  'Ligue 1 Conforama'                    |
| 17    |  'Domino’s Ligue 2'                     |
| 19    |  'Bundesliga'                           |
| 20    |  'Bundesliga 2'                         |
| 31    |  'Calcio A'                             |
| 32    |  'Calcio B'                             |
| 39    |  'Major League Soccer'                  |
| 41    |  'Eliteserien'                          |
| 50    |  'Scottish Premiership'                 |
| 51    |  'Scotland League'                      |
| 53    |  'LaLiga Santander'                     |
| 54    |  'LaLiga 1 I 2 I 3'                     |
| 56    |  'Allsvenskan'                          |
| 57    |  'Colombia Apertura'                    |
| 58    |  'Colombia Clausura'                    |
| 60    |  'EFL League One'                       |
| 61    |  'EFL League Two'                       |
| 63    |  'Hellas Liga'                          |
| 65    |  'SSE Airtricity League'                |
| 66    |  'Ekstraklasa'                          |
| 67    |  'Russian Football Premier League'      |
| 68    |  'Süper Lig'                            |
| 76    |  'Rest of World'                        |
| 78    |  "Men's National"                       |
| 80    |  'Österreichische   Fußball-Bundesliga' |
| 83    |  'K LEAGUE Classic'                     |
| 84    |  'Mexican Clausura'                     |
| 85    |  'Mexican Apertura'                     |
| 152   |  'Torneo de Primera'                    |
| 153   |  'Torneo de Primera'                    |
| 156   |  'Chile Apertura'                       |
| 157   |  'Chile Clausura'                       |
| 189   |  'Raiffeisen Super League'              |
| 308   |  'Liga NOS'                             |
| 319   |  'Česká Liga'                           |
| 322   |  'Finnliiga'                            |
| 332   |  'Ukrayina Liha'                        |
| 335   |  'Campeonato Scotiabank'                |
| 336   |  'Liga Dimayor'                         |
| 341   |  'LIGA Bancomer MX'                     |
| 347   |  'South African FL'                     |
| 349   |  'Meiji Yasuda J1 League'               |
| 350   |  'Dawry Jameel'                         |
| 351   |  'Hyundai A-League'                     |
| 353   |  'Primera División'                     |
| 371   |  'Scotland League'                      |
| 382   |  'Free Agents'                          |
| 383   |  'Created Players League'               |
| 384   |  'Creation Centre League'               |
| 390   |  'MLS Cup'                              |
| 993   |  'Asia Qualifier'                       |
| 1003  |  'Copa Latinoamericana'                 |
| 1004  |  'Colombia Apertura'                    |
| 1005  |  'Colombia Finalización'                |
| 1006  |  'Chile Apertura'                       |
| 1007  |  'Chile Clausura'                       |
| 1008  |  'Argentina Apertura'                   |
| 1009  |  'Argentina Clausura'                   |
| 2002  |  'Nacional B'                           |
| 2012  |  'China Top League'                     |
| 2025  |  'Liga do Brasil B'                     |
| 2028  |  'World League'                         |
| 2076  |  '3. Liga'                              |
| 2096  |  'Special Teams'                        |
| 2118  |  'Icons'                                |
| 2136  |  "Women's National"                     |
| 2138  |  'International Clubs'                  |
| 2150  |  'REWARDS'                              |
| 10001 |  'Denmark League 2'                     |
| 10004 |  'Belgium League 2'                     |
| 10007 |  'Liga do Brasil 1'                     |
| 10010 |  'Holland League 2'                     |
| 10017 |  'France League 3'                      |
| 10020 |  'Germany League 3'                     |
| 10032 |  'Italy League 3'                       |
| 10041 |  'Norway League 2'                      |
| 10050 |  'Scotland League 2'                    |
| 10054 |  'Spain League 3'                       |
| 10056 |  'Sweden League 2'                      |
| 10061 |  'England League 5'                     |
| 10065 |  'Ireland League 2'                     |
| 10066 |  'Poland League 2'                      |
| 10067 |  'Russia League 2'                      |
| 10076 |  'Rest of World 2'                      |
| 10080 |  'Austria League 2'                     |
| 10083 |  'Korea League 2'                       |
| 10189 |  'Switzerland League 2'                 |
| 10308 |  'Portugal League 2'                    |
| 10335 |  'Chile League 2'                       |
| 10336 |  'Colombia League 2'                    |
| 10341 |  'Mexico League 2'                      |
| 10350 |  'Saudi League 2'                       |
| 10353 |  'Argentina League 2'                   |

</p></details>



### Player IDs
The player IDs are found through the property fut.players. [A full table is available at this Google Drive link.](https://docs.google.com/spreadsheets/d/1ufH7aLh6oUh4q_M4bRP-vpbt6YFclrfeNAlkE7z01iU/edit?usp=sharing)


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


### PlayStyle IDs
PlayStyle IDs are found through the property fut.playstyles.
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

### Nation IDs
Nation IDs are found through the property fut.nations.
<details>
<summary>Nation ID Lookup Table</summary><p>
<!-- alternative placement of p shown above -->


| ID                            | Nation                    |
|-------------------------------|---------------------------|
| 1                             |  'Albania',               |
| 2                             |  'Andorra',               |
| 3                             |  'Armenia',               |
| 4                             |  'Austria',               |
| 5                             |  'Azerbaijan',            |
| 6                             |  'Belarus',               |
| 7                             |  'Belgium',               |
| 8                             |  'Bosnia Herzegovina',    |
| 9                             |  'Bulgaria',              |
| 10                            |  'Croatia',               |
| 11                            |  'Cyprus',                |
| 12                            |  'Czech Republic',        |
| 13                            |  'Denmark',               |
| 14                            |  'England',               |
| 15                            |  'Montenegro',            |
| 16                            |  'Faroe Islands',         |
| 17                            |  'Finland',               |
| 18                            |  'France',                |
| 19                            |  'FYR Macedonia',         |
| 20                            |  'Georgia',               |
| 21                            |  'Germany',               |
| 22                            |  'Greece',                |
| 23                            |  'Hungary',               |
| 24                            |  'Iceland',               |
| 25                            |  'Republic of Ireland',   |
| 26                            |  'Israel',                |
| 27                            |  'Italy',                 |
| 28                            |  'Latvia',                |
| 29                            |  'Liechtenstein',         |
| 30                            |  'Lithuania',             |
| 31                            |  'Luxemburg',             |
| 32                            |  'Malta',                 |
| 33                            |  'Moldova',               |
| 34                            |  'Netherlands',           |
| 35                            |  'Northern Ireland',      |
| 36                            |  'Norway',                |
| 37                            |  'Poland',                |
| 38                            |  'Portugal',              |
| 39                            |  'Romania',               |
| 40                            |  'Russia',                |
| 41                            |  'San Marino',            |
| 42                            |  'Scotland',              |
| 43                            |  'Slovakia',              |
| 44                            |  'Slovenia',              |
| 45                            |  'Spain',                 |
| 46                            |  'Sweden',                |
| 47                            |  'Switzerland',           |
| 48                            |  'Turkey',                |
| 49                            |  'Ukraine',               |
| 50                            |  'Wales',                 |
| 51                            |  'Serbia',                |
| 52                            |  'Argentina',             |
| 53                            |  'Bolivia',               |
| 54                            |  'Brazil',                |
| 55                            |  'Chile',                 |
| 56                            |  'Colombia',              |
| 57                            |  'Ecuador',               |
| 58                            |  'Paraguay',              |
| 59                            |  'Peru',                  |
| 60                            |  'Uruguay',               |
| 61                            |  'Venezuela',             |
| 62                            |  'Anguilla',              |
| 63                            |  'Antigua & Barbuda',     |
| 64                            |  'Aruba',                 |
| 65                            |  'Bahamas',               |
| 66                            |  'Barbados',              |
| 67                            |  'Belize',                |
| 68                            |  'Bermuda',               |
| 69                            |  'British Virgin Isles',  |
| 70                            |  'Canada',                |
| 71                            |  'Cayman Islands',        |
| 72                            |  'Costa Rica',            |
| 73                            |  'Cuba',                  |
| 74                            |  'Dominica',              |
| 75                            |  'International',         |
| 76                            |  'El Salvador',           |
| 77                            |  'Grenada',               |
| 78                            |  'Guatemala',             |
| 79                            |  'Guyana',                |
| 80                            |  'Haiti',                 |
| 81                            |  'Honduras',              |
| 82                            |  'Jamaica',               |
| 83                            |  'Mexico',                |
| 84                            |  'Montserrat',            |
| 85                            |  'Netherlands Antilles',  |
| 86                            |  'Nicaragua',             |
| 87                            |  'Panama',                |
| 88                            |  'Puerto Rico',           |
| 89                            |  'St Kitts Nevis',        |
| 90                            |  'St Lucia',              |
| 91                            |  'St Vincent Grenadine',  |
| 92                            |  'Suriname',              |
| 93                            |  'Trinidad & Tobago',     |
| 94                            |  'Turks & Caicos',        |
| 95                            |  'United States',         |
| 96                            |  'US Virgin Islands',     |
| 97                            |  'Algeria',               |
| 98                            |  'Angola',                |
| 99                            |  'Benin',                 |
| 100                           |  'Botswana',              |
| 101                           |  'Burkina Faso',          |
| 102                           |  'Burundi',               |
| 103                           |  'Cameroon',              |
| 104                           |  'Cape Verde Islands',    |
| 105                           |  'CAR',                   |
| 106                           |  'Chad',                  |
| 107                           |  'Congo',                 |
| 108                           |  'Ivory Coast',           |
| 109                           |  'Djibouti',              |
| 110                           |  'DR Congo',              |
| 111                           |  'Egypt',                 |
| 112                           |  'Equatorial Guinea',     |
| 113                           |  'Eritrea',               |
| 114                           |  'Ethiopia',              |
| 115                           |  'Gabon',                 |
| 116                           |  'Gambia',                |
| 117                           |  'Ghana',                 |
| 118                           |  'Guinea',                |
| 119                           |  'Guinea Bissau',         |
| 120                           |  'Kenya',                 |
| 121                           |  'Lesotho',               |
| 122                           |  'Liberia',               |
| 123                           |  'Libya',                 |
| 124                           |  'Madagascar',            |
| 125                           |  'Malawi',                |
| 126                           |  'Mali',                  |
| 127                           |  'Mauritania',            |
| 128                           |  'Mauritius',             |
| 129                           |  'Morocco',               |
| 130                           |  'Mozambique',            |
| 131                           |  'Namibia',               |
| 132                           |  'Niger',                 |
| 133                           |  'Nigeria',               |
| 134                           |  'Rwanda',                |
| 135                           |  'São Tomé & Príncipe',   |
| 136                           |  'Senegal',               |
| 137                           |  'Seychelles',            |
| 138                           |  'Sierra Leone',          |
| 139                           |  'Somalia',               |
| 140                           |  'South Africa',          |
| 141                           |  'Sudan',                 |
| 142                           |  'Swaziland',             |
| 143                           |  'Tanzania',              |
| 144                           |  'Togo',                  |
| 145                           |  'Tunisia',               |
| 146                           |  'Uganda',                |
| 147                           |  'Zambia',                |
| 148                           |  'Zimbabwe',              |
| 149                           |  'Afghanistan',           |
| 150                           |  'Bahrain',               |
| 151                           |  'Bangladesh',            |
| 152                           |  'Bhutan',                |
| 153                           |  'Brunei Darussalam',     |
| 154                           |  'Cambodia',              |
| 155                           |  'China PR',              |
| 156                           |  'Chinese Taipei',        |
| 157                           |  'Guam',                  |
| 158                           |  'Hong Kong',             |
| 159                           |  'India',                 |
| 160                           |  'Indonesia',             |
| 161                           |  'Iran',                  |
| 162                           |  'Iraq',                  |
| 163                           |  'Japan',                 |
| 164                           |  'Jordan',                |
| 165                           |  'Kazakhstan',            |
| 166                           |  'Korea DPR',             |
| 167                           |  'Korea Republic',        |
| 168                           |  'Kuwait',                |
| 169                           |  'Kyrgyzstan',            |
| 170                           |  'Laos',                  |
| 171                           |  'Lebanon',               |
| 172                           |  'Macau',                 |
| 173                           |  'Malaysia',              |
| 174                           |  'Maldives',              |
| 175                           |  'Mongolia',              |
| 176                           |  'Myanmar',               |
| 177                           |  'Nepal',                 |
| 178                           |  'Oman',                  |
| 179                           |  'Pakistan',              |
| 180                           |  'Palestinian Authority', |
| 181                           |  'Philippines',           |
| 182                           |  'Qatar',                 |
| 183                           |  'Saudi Arabia',          |
| 184                           |  'Singapore',             |
| 185                           |  'Sri Lanka',             |
| 186                           |  'Syria',                 |
| 187                           |  'Tajikistan',            |
| 188                           |  'Thailand',              |
| 189                           |  'Turkmenistan',          |
| 190                           |  'United Arab Emirates',  |
| 191                           |  'Uzbekistan',            |
| 192                           |  'Vietnam',               |
| 193                           |  'Yemen',                 |
| 194                           |  'American Samoa',        |
| 195                           |  'Australia',             |
| 196                           |  'Cook Islands',          |
| 197                           |  'Fiji',                  |
| 198                           |  'New Zealand',           |
| 199                           |  'Papua New Guinea',      |
| 200                           |  'Samoa',                 |
| 201                           |  'Solomon Islands',       |
| 202                           |  'Tahiti',                |
| 203                           |  'Tonga',                 |
| 204                           |  'Vanuatu',               |
| 205                           |  'Gibraltar',             |
| 206                           |  'Greenland',             |
| 207                           |  'Dominican Republic',    |
| 208                           |  'Estonia',               |
| 209                           |  'Created Players',       |
| 210                           |  'Free Agents',           |
| 211                           |  'Rest of World',         |
| 212                           |  'Timor-Leste',           |
| 213                           |  'Chinese Taipei',        |
| 214                           |  'Comoros',               |
| 215                           |  'New Caledonia',         |
| 219                           |  'Kosovo'                 |

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

### Stadium IDs
Stadiums IDs are found through the property fut.stadiums.
<details>
<summary>Stadium ID Lookup Table</summary><p>
<!-- alternative placement of p shown above -->

| ID  | Stadium                                 |
|-----|-----------------------------------------|
| 1   | 'Old Trafford'                          |
| 2   | 'Santiago Bernabéu'                     |
| 4   | 'Stade Gerland'                         |
| 5   | 'San Siro'                              |
| 6   | 'Camp Nou'                              |
| 8   | 'Stadio Delle Alpi'                     |
| 9   | 'Signal Iduna Park'                     |
| 10  | 'Estadio Mestalla'                      |
| 13  | 'Anfield'                               |
| 14  | 'Parc des Princes'                      |
| 15  | 'Amsterdam ArenA'                       |
| 16  | 'Stade Felix Bollaert'                  |
| 17  | 'Constant Vanden Stock'                 |
| 25  | 'Closed Square Style'                   |
| 26  | 'Forest Park Stadium'                   |
| 28  | 'Stamford Bridge'                       |
| 29  | 'Orange Vélodrome'                      |
| 30  | 'Veltins Arena'                         |
| 32  | 'Crown Lane'                            |
| 33  | 'Union Park Stadium'                    |
| 34  | 'Town Park'                             |
| 35  | 'Euro Park'                             |
| 37  | 'Div 3 Euro Style'                      |
| 38  | 'Urban Training'                        |
| 39  | 'Rural Training'                        |
| 41  | 'Volksparkstadion'                      |
| 42  | 'Estadio Vicente Calderón'              |
| 100 | "St. James' Park"                       |
| 102 | 'José Alvalade'                         |
| 104 | 'Estadio Azteca'                        |
| 107 | 'Estádio da Luz'                        |
| 108 | 'Seoul Sang-am Stadium'                 |
| 110 | 'Daegu Stadium'                         |
| 111 | 'Estádio do Dragão'                     |
| 112 | 'Fratton Park'                          |
| 113 | "St. Mary's Stadium"                    |
| 115 | 'Villa Park'                            |
| 116 | 'White Hart Lane'                       |
| 124 | 'Small Olympic'                         |
| 127 | 'Large Olympic'                         |
| 129 | 'Large Square'                          |
| 133 | 'Mercedes-Benz Arena'                   |
| 134 | 'HDI Arena'                             |
| 135 | 'Olympiastadion'                        |
| 137 | 'Allianz Arena'                         |
| 138 | 'Commerzbank Arena'                     |
| 147 | 'Stadion Europa'                        |
| 149 | 'Al Jayeed Stadium'                     |
| 153 | 'Aloha Park'                            |
| 155 | 'Wembley Stadium'                       |
| 345 | 'King Abdullah Sports City'             |
| 156 | 'Emirates Stadium'                      |
| 157 | 'Stadio Olimpico'                       |
| 158 | 'Estadio de las Artes'                  |
| 161 | 'StubHub Center'                        |
| 163 | 'Jalisco'                               |
| 165 | 'Stade de Suisse'                       |
| 172 | 'StadiumName_172_FIWC-Stadium_FullChar' |
| 174 | 'Stadio Comunale'                       |
| 175 | 'Arena del Centenario'                  |
| 176 | 'Waldstadion'                           |
| 177 | 'La Canchita'                           |
| 178 | 'Stadion Neder'                         |
| 179 | 'Stade Municipal'                       |
| 180 | 'Ivy Lane'                              |
| 181 | 'El Grandioso'                          |
| 182 | 'Stadion 23. Maj'                       |
| 183 | 'Estadio El Medio'                      |
| 184 | 'North America'                         |
| 185 | 'South America'                         |
| 186 | 'Southern Europe'                       |
| 187 | 'Eastern Europe'                        |
| 188 | 'Central Europe'                        |
| 189 | 'United Kingdom'                        |
| 190 | 'Asia'                                  |
| 192 | 'El Libertador'                         |
| 193 | 'Stadio Classico'                       |
| 194 | 'Eastpoint Arena'                       |
| 195 | 'Stadion Olympik'                       |
| 196 | 'Stadion Hanguk'                        |
| 197 | 'O Dromo'                               |
| 211 | 'Estadio Chamartin'                     |
| 212 | 'Estadio Presidente G.Lopes'            |
| 213 | 'Green Point Stadium'                   |
| 214 | 'Durban Stadium'                        |
| 215 | 'Ellis Park Stadium'                    |
| 216 | 'Soccer City Stadium'                   |
| 217 | 'Free State Stadium'                    |
| 218 | 'Nelson Mandela Bay Stadium'            |
| 219 | 'Mbombela Stadium'                      |
| 220 | 'Peter Mokaba Stadium'                  |
| 221 | 'Royal Bafokeng Stadium'                |
| 222 | 'Loftus Versfeld Stadium'               |
| 223 | 'Friður Stadium'                        |
| 224 | 'Satta Stadium'                         |
| 225 | 'Akaaroa Stadium'                       |
| 226 | 'Hasiti Arena'                          |
| 227 | 'Salam Stadium'                         |
| 228 | 'Court Lane'                            |
| 229 | "Arena D'Oro"                           |
| 233 | 'Peuan Arena'                           |
| 234 | 'Pyonghwa Stadium'                      |
| 235 | 'Udugu Stadium'                         |
| 236 | 'El Coloso'                             |
| 238 | 'Africa'                                |
| 246 | 'Etihad Stadium'                        |
| 247 | 'Allianz Stadium'                       |
| 248 | 'BC Place Stadium'                      |
| 249 | 'Molton Road'                           |
| 250 | 'Oceanic Arena'                         |
| 253 | 'Olympic Stadium'                       |
| 254 | 'Municipal Stadium Poznan'              |
| 255 | 'National Stadium Warsaw'               |
| 256 | 'Arena Gdansk'                          |
| 257 | 'Municipal Stadium Wroclaw'             |
| 258 | 'Metalist Stadium'                      |
| 259 | 'Arena Lviv'                            |
| 260 | 'Donbass Arena'                         |
| 261 | 'Sanderson Park'                        |
| 262 | 'King Fahd Stadium'                     |
| 264 | 'La Bombonera'                          |
| 265 | 'Goodison Park'                         |
| 267 | 'Arena Amazonia'                        |
| 268 | 'Arena da Baixada'                      |
| 269 | 'Arena de Sao Paulo'                    |
| 270 | 'Arena Fonte Nova'                      |
| 271 | 'Arena Pantanal'                        |
| 272 | 'Arena Pernambuco'                      |
| 273 | 'Estadio Beira-Rio'                     |
| 274 | 'Estadio Castelao'                      |
| 275 | 'Estadio das Dunas'                     |
| 276 | 'Estadio do Maracana'                   |
| 277 | 'Estadio Mineirao'                      |
| 278 | 'Estadio Nacional'                      |
| 279 | 'Baba Yetu Stadium'                     |
| 282 | 'Stade du 13 Octobre'                   |
| 285 | 'Stade du Lukanga'                      |
| 286 | 'Estadio de las Cascadas'               |
| 287 | 'El Grandioso de las Pampas'            |
| 288 | 'Singeom Stadium'                       |
| 289 | 'Shibusaka Stadium'                     |
| 290 | 'Gold Lake Stadium'                     |
| 291 | 'Stadio San Dalla Pace'                 |
| 316 | 'Training Centre'                       |
| 325 | 'Boleyn Ground'                         |
| 326 | 'Stadium of Light'                      |
| 327 | 'The Hawthorns'                         |
| 329 | 'Carrow Road'                           |
| 330 | 'Selhurst Park'                         |
| 331 | 'Stoke City FC Stadium'                 |
| 332 | 'KCOM Stadium'                          |
| 333 | 'Liberty Stadium'                       |
| 335 | 'King Power Stadium'                    |
| 336 | 'Turf Moor'                             |
| 337 | 'Loftus Road'                           |
| 340 | 'The Amex Stadium'                      |
| 341 | 'CenturyLink Field'                     |
| 343 | 'BORUSSIA-PARK'                         |
| 344 | 'El Monumental'                         |
| 345 | 'King Abdullah Sports City'             |
| 347 | 'Vicarage Road'                         |
| 348 | 'Vitality Stadium'                      |
| 349 | 'Riverside Stadium'                     |
| 353 | 'Training Ground'                       |
| 354 | 'Suita City Football Stadium'           |
| 355 | 'London Stadium'                        |
| 358 | 'EA SPORTS FIFA Stadium'                |
| 364 | 'Wanda Metropolitano'                   |
| 372 | 'Luzhniki Stadium'                      |
| 373 | 'Saint Petersburg Stadium'              |
| 374 | 'Kazan Arena'                           |
| 375 | 'Samara Arena'                          |
| 376 | 'Fisht Stadium'                         |
| 377 | 'Nizhny Novgorod Stadium'               |
| 378 | 'Spartak Stadium'                       |
| 379 | 'Rostov Arena'                          |
| 380 | 'Ekaterinburg Arena'                    |
| 381 | 'Mordovia Arena'                        |
| 382 | 'Volgograd Arena'                       |
| 383 | 'Kaliningrad Stadium'                   |
| 384 | 'Kirklees Stadium'                      |

</p></details>


### Team IDs
The team IDs are found through the property fut.teams. [A full table is available at this Google Drive link.](https://docs.google.com/spreadsheets/d/1_KdX2lYJOYyhdFkEYhyT8QZuCyznMVNtuBAJo4prHWs/edit?usp=sharing)


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
