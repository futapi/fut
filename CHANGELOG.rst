.. :changelog:

Changelog
---------


0.3.6 (2017-11-12)
^^^^^^^^^^^^^^^^^^

* add sbsSetChallenges (thanks to dan-gamble #330)
* readme polish (thanks to syndac)
* add tradepileClear
* add sbsSquad
* add sendToSbs
* add clubConsumables
* correct version param in pinevents
* save token between logins (maybe cookies are not needed?)

0.3.5 (2017-10-26)
^^^^^^^^^^^^^^^^^^

* various pinEvents improvements
* remove default buy now price for sell method to avoid mistakes
* add buyPack
* add objectives
* add duplicates list
* add level param to club method
* correct tradeStatus params
* check tradeStatus after selling item like webapp do
* add marketDataMaxPrice & marketDataMinPrice to item data parser

0.3.4 (2017-10-18)
^^^^^^^^^^^^^^^^^^

* disable debug info

0.3.3 (2017-10-18)
^^^^^^^^^^^^^^^^^^

* correct pin values (#314)

0.3.2 (2017-10-18)
^^^^^^^^^^^^^^^^^^

* fix syntax error

0.3.1 (2017-10-18)
^^^^^^^^^^^^^^^^^^

* pinEvents: random timestamp with delay & option request before sending data
* add sbsSets
* correct few details (page_size, sleep times etc.) - community work :-)
* rename searchAuctions to search (You can still use searchAuctions)
* fix python2 compatibility (#296)
* correct _ value - all credits go to ricklhp7
* fix sendToWatchlist (jsarasti patch #303)
* proper currentBid check logic (jsarasti patch #303)
* fix squad method (#300)
* fix database (players, nations, leagues, teams, stadiums)
* add balls method (database)
* rewrite searchDefinition (jsarasti work #304)

0.3.0 (2017-10-12)
^^^^^^^^^^^^^^^^^^

* initial release for fifa 18
* bump useragent
* add ability to login via sms code or totp authenticator (fully automatic)
* pinEvents

0.2.19 (2017-09-21)
^^^^^^^^^^^^^^^^^^^

* searchAuctions: add ability to search rare (special) cards #280
* fix addition request to send code (#285)

0.2.18 (2017-05-25)
^^^^^^^^^^^^^^^^^^^

* do not force log in when not necessary (thanks to xAranaktu #264)
* add missing params, update logic in login (thanks to xAranaktu #266)
* reenable postion parsing & add missing keys in item_data parser (fix #265)
* unify item_data keys for players & consumables
* add playstyles & stadiums
* add missing param sku_a (thanks to rafaelget #259)

0.2.17 (2017-05-20)
^^^^^^^^^^^^^^^^^^^

* fix #262 searchAuctions && piles returns empty list when no results found
* fix wrong fut version in referer on login (thanks to xAranaktu #263)
* init usermassinfo functionality (thanks to xAranaktu #263)
* add tradingEnabled check on login (thanks to xAranaktu #263)

0.2.16 (2017-05-17)
^^^^^^^^^^^^^^^^^^^

* fix applyConsumable
* add brokeringSku param for tradepile (thanks to pulkitsharma #259)

0.2.15 (2017-05-04)
^^^^^^^^^^^^^^^^^^^

* huge performance improvement on database load (skip encoding guess)
* fix baseId version calculation
* core: add clubConsumablesDetails
* core: add applyConsumable

0.2.14 (2017-04-29)
^^^^^^^^^^^^^^^^^^^

* fix player parser

0.2.13 (2017-04-28)
^^^^^^^^^^^^^^^^^^^

* fix cardInfo for not a player
* cache database

0.2.12 (2017-04-28)
^^^^^^^^^^^^^^^^^^^

* proper #255 fix - from now we're going to read whole players db on login

0.2.10 (2017-04-24)
^^^^^^^^^^^^^^^^^^^

* fix baseId calculation (#255)

0.2.9 (2017-03-07)
^^^^^^^^^^^^^^^^^^

* proper #250, #251 fix (thanks to bas85)

0.2.8 (2017-03-06)
^^^^^^^^^^^^^^^^^^

* fix login problems, need confirmation (#250)
* bump fifa version in urls & user-agent etc.
* temporary disabled emulate feature, need more info and work (#250)

0.2.7 (2017-01-17)
^^^^^^^^^^^^^^^^^^

* fix missing import (#244)

0.2.6 (2017-01-10)
^^^^^^^^^^^^^^^^^^

* add (minimum request) delay param (#233)
* add fast param to bid method
* use Unauthorized expcetion (fix #232)

0.2.5 (2016-12-28)
^^^^^^^^^^^^^^^^^^

* add timeout (#226)

0.2.4 (2016-12-15)
^^^^^^^^^^^^^^^^^^

* proper(?) page_size and start values correction (thanks to rafaelget #220)
* fix fut_home url (thanks to Fanatico1981 #219)

0.2.3 (2016-11-20)
^^^^^^^^^^^^^^^^^^

* correct page_size value #216

0.2.2 (2016-10-31)
^^^^^^^^^^^^^^^^^^

* add bans wave warning

0.2.1 (2016-10-03)
^^^^^^^^^^^^^^^^^^

* fix tradepile/watchlist when consumable in pile (#194)
* fix card info url & bump default year in leagues/teams
* fix credits resetting to 0 on search (thanks to hunterjm #198)

0.2.0 (2016-09-26)
^^^^^^^^^^^^^^^^^^

* fifa 17 & dump versions (thanks to rafaelget #192)

0.1.10 (2016-04-30)
^^^^^^^^^^^^^^^^^^^

* fix python 3 compatibility #183
* bump client version for and/ios (fix #190 thanks to rafaelget)
* bump user-agent and flash version

0.1.9 (2015-12-11)
^^^^^^^^^^^^^^^^^^

* bump client version for and/ios
* bump user-agent * flash version

0.1.8 (2015-12-09)
^^^^^^^^^^^^^^^^^^

* core: fix #172, fix #176 crash when skuAccessList is empty

0.1.7 (2015-11-30)
^^^^^^^^^^^^^^^^^^

* core: fix baseId calculation (thanks to hunterjm #174)

0.1.6 (2015-11-19)
^^^^^^^^^^^^^^^^^^

* core: store credits after every call instead of making an additional call out

0.1.5 (2015-11-15)
^^^^^^^^^^^^^^^^^^

* core: fix club (thanks to hunterjm #169)

0.1.4 (2015-10-29)
^^^^^^^^^^^^^^^^^^

* core: fix itemParse (thanks to hunterjm #163)

0.1.3 (2015-10-28)
^^^^^^^^^^^^^^^^^^

* core: bump clientversion for android/ios emulation
* core: add tradeStatus (thanks to hunterjm #161)
* exceptions: add code, reason, string to FutError

0.1.2 (2015-09-28)
^^^^^^^^^^^^^^^^^^

* core: fix baseId calculation
* support app authentication (#147)

0.1.1 (2015-09-19)
^^^^^^^^^^^^^^^^^^

* fix for ps/xbox

0.1.0 (2015-09-17)
^^^^^^^^^^^^^^^^^^

* fifa 16
* core: update credits only on demand
* config: update user-agent (chrome 45 @ win10)

0.0.24 (2015-02-11)
^^^^^^^^^^^^^^^^^^^

* core: fix #135 type conversion in quickSell & watchlistDelete
* core: rename parameter squad_num to squad_id

0.0.23 (2015-02-09)
^^^^^^^^^^^^^^^^^^^

* urls: fix #131
* Captcha exception got img & token parameter
* core: add logout
* core: quickSell & watchlistDelete accepts now int/str or tuple/list with multiple ids
* urls: enable ssl for all urls
* core & urls: add timestamp dynamically (just right before every request)

0.0.22 (2014-12-28)
^^^^^^^^^^^^^^^^^^^

* setup: fix manifest
* core: save session if code is not provided but required


0.0.21 (2014-12-13)
^^^^^^^^^^^^^^^^^^^

* two-step verification
* fix cookies parameter not working (#99)
* core: use LWPCookieJar instead of pickle
* core: fix logging in __sendToPile__


0.0.20 (2014-10-19)
^^^^^^^^^^^^^^^^^^^

* fix typo


0.0.19 (2014-10-19)
^^^^^^^^^^^^^^^^^^^

* core: update old fut14 urls
* core: add cookies feature (save cookies after every request and load it when restaring app like browser)
* core: add saveSession, searchDefinition
* core: log sendToPile action


0.0.18 (2014-10-01)
^^^^^^^^^^^^^^^^^^^

* core: add methods to list and delete available messages (thanks to jamslater)
* core: rework base id from resource id calculation, use new constant (thanks to jamslater)
* core: update android * ios clientVersion (9->11)


0.0.17 (2014-09-22)
^^^^^^^^^^^^^^^^^^^

* rename project (fut14->fut)
* fut15 (drop support for fifa 14)


0.0.16 (2014-08-31)
^^^^^^^^^^^^^^^^^^^

* #76 fix buying (thanks to arthurnn)


0.0.15 (2014-08-29)
^^^^^^^^^^^^^^^^^^^

* add new exceptions: doLoginFail, MaxSessions, Captcha
* add changelog
* NullHandler is default logging handler
* core: bump clientVersion (8->9)


0.0.14 (2014-07-06)
^^^^^^^^^^^^^^^^^^^

* core: relist returns number of delted/sold if clean parameter was set
* add new exception FeatureDisabled
* core: add emulate
* core: add stats
* core: add clubInfo


0.0.13 (2014-04-19)
^^^^^^^^^^^^^^^^^^^

* core: add sendToWatchlist


0.0.12 (2014-02-23)
^^^^^^^^^^^^^^^^^^^

* exceptions: add Unauthorized & MultipleSession
* fix quicksell


0.0.11 (2014-02-15)
^^^^^^^^^^^^^^^^^^^

* fix logger
* setup.py is now executable


0.0.10 (2014-02-15)
^^^^^^^^^^^^^^^^^^^

* core: add clean ability to relist (remove sold cards)
* core: keepalive returns credit amount


0.0.9 (2014-01-26)
^^^^^^^^^^^^^^^^^^

* fix relist


0.0.8 (2014-01-26)
^^^^^^^^^^^^^^^^^^

* add new exception Conflict
* init docs
* core: add relist
* core: add sendToClub


0.0.7 (2014-01-13)
^^^^^^^^^^^^^^^^^^

* add few exceptions


0.0.6 (2013-12-30)
^^^^^^^^^^^^^^^^^^

* core: add DEBUG feature
* add multiplatform support (xbox/ps3/and/ios)


0.0.5 (2013-12-23)
^^^^^^^^^^^^^^^^^^

* core: add assetId param to searchAuction method
* core: add pileSize
* core: add leagueId to item data parser


0.0.4 (2013-11-10)
^^^^^^^^^^^^^^^^^^

* convert lowercase function/method names to mixedCase (send_to_tradepile -> sendToTradepile)
* drop python-2.5 (requests)
* core: python 3 support


0.0.3 (2013-10-25)
^^^^^^^^^^^^^^^^^^

* core: move requests session init & headers from login to init
* core: update credits on every request (only if it is avaible included in response)


0.0.2 (2013-10-17)
^^^^^^^^^^^^^^^^^^

* core: add watchlist
* core: add card_info function
* core: add alias for base_id & card_info


0.0.1 (2013-10-15)
^^^^^^^^^^^^^^^^^^

* init
