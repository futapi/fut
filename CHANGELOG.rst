.. :changelog:

Changelog
---------


0.2.5 (2016-12-28)
++++++++++++++++++
* add timeout (#226)

0.2.4 (2016-12-15)
++++++++++++++++++
* proper(?) page_size and start values correction (thanks to rafaelget #220)
* fix fut_home url (thanks to Fanatico1981 #219)

0.2.3 (2016-11-20)
++++++++++++++++++
* correct page_size value #216

0.2.2 (2016-10-31)
++++++++++++++++++
* add bans wave warning

0.2.1 (2016-10-03)
++++++++++++++++++
* fix tradepile/watchlist when consumable in pile (#194)
* fix card info url & bump default year in leagues/teams
* fix credits resetting to 0 on search (thanks to hunterjm #198)

0.2.0 (2016-09-26)
++++++++++++++++++
* fifa 17 & dump versions (thanks to rafaelget #192)

0.1.10 (2016-04-30)
++++++++++++++++++
* fix python 3 compatibility #183
* bump client version for and/ios (fix #190 thanks to rafaelget)
* bump user-agent and flash version

0.1.9 (2015-12-11)
++++++++++++++++++
* bump client version for and/ios
* bump user-agent * flash version

0.1.8 (2015-12-09)
++++++++++++++++++
* core: fix #172, fix #176 crash when skuAccessList is empty

0.1.7 (2015-11-30)
++++++++++++++++++
* core: fix baseId calculation (thanks to hunterjm #174)

0.1.6 (2015-11-19)
++++++++++++++++++
* core: store credits after every call instead of making an additional call out

0.1.5 (2015-11-15)
++++++++++++++++++
* core: fix club (thanks to hunterjm #169)

0.1.4 (2015-10-29)
++++++++++++++++++
* core: fix itemParse (thanks to hunterjm #163)

0.1.3 (2015-10-28)
++++++++++++++++++
* core: bump clientversion for android/ios emulation
* core: add tradeStatus (thanks to hunterjm #161)
* exceptions: add code, reason, string to FutError

0.1.2 (2015-09-28)
++++++++++++++++++
* core: fix baseId calculation
* support app authentication (#147)

0.1.1 (2015-09-19)
++++++++++++++++++
* fix for ps/xbox

0.1.0 (2015-09-17)
++++++++++++++++++
* fifa 16
* core: update credits only on demand
* config: update user-agent (chrome 45 @ win10)

0.0.24 (2015-02-11)
+++++++++++++++++++
* core: fix #135 type conversion in quickSell & watchlistDelete
* core: rename parameter squad_num to squad_id

0.0.23 (2015-02-09)
+++++++++++++++++++
* urls: fix #131
* Captcha exception got img & token parameter
* core: add logout
* core: quickSell & watchlistDelete accepts now int/str or tuple/list with multiple ids
* urls: enable ssl for all urls
* core & urls: add timestamp dynamically (just right before every request)

0.0.22 (2014-12-28)
+++++++++++++++++++
* setup: fix manifest
* core: save session if code is not provided but required


0.0.21 (2014-12-13)
+++++++++++++++++++
* two-step verification
* fix cookies parameter not working (#99)
* core: use LWPCookieJar instead of pickle
* core: fix logging in __sendToPile__


0.0.20 (2014-10-19)
+++++++++++++++++++
* fix typo


0.0.19 (2014-10-19)
+++++++++++++++++++
* core: update old fut14 urls
* core: add cookies feature (save cookies after every request and load it when restaring app like browser)
* core: add saveSession, searchDefinition
* core: log sendToPile action


0.0.18 (2014-10-01)
+++++++++++++++++++
* core: add methods to list and delete available messages (thanks to jamslater)
* core: rework base id from resource id calculation, use new constant (thanks to jamslater)
* core: update android * ios clientVersion (9->11)


0.0.17 (2014-09-22)
+++++++++++++++++++
* rename project (fut14->fut)
* fut15 (drop support for fifa 14)


0.0.16 (2014-08-31)
+++++++++++++++++++
* #76 fix buying (thanks to arthurnn)


0.0.15 (2014-08-29)
+++++++++++++++++++
* add new exceptions: doLoginFail, MaxSessions, Captcha
* add changelog
* NullHandler is default logging handler
* core: bump clientVersion (8->9)


0.0.14 (2014-07-06)
+++++++++++++++++++

* core: relist returns number of delted/sold if clean parameter was set
* add new exception FeatureDisabled
* core: add emulate
* core: add stats
* core: add clubInfo


0.0.13 (2014-04-19)
+++++++++++++++++++

* core: add sendToWatchlist


0.0.12 (2014-02-23)
+++++++++++++++++++

* exceptions: add Unauthorized & MultipleSession
* fix quicksell


0.0.11 (2014-02-15)
+++++++++++++++++++

* fix logger
* setup.py is now executable


0.0.10 (2014-02-15)
+++++++++++++++++++

* core: add clean ability to relist (remove sold cards)
* core: keepalive returns credit amount


0.0.9 (2014-01-26)
++++++++++++++++++

* fix relist


0.0.8 (2014-01-26)
++++++++++++++++++

* add new exception Conflict
* init docs
* core: add relist
* core: add sendToClub


0.0.7 (2014-01-13)
++++++++++++++++++

* add few exceptions


0.0.6 (2013-12-30)
++++++++++++++++++

* core: add DEBUG feature
* add multiplatform support (xbox/ps3/and/ios)


0.0.5 (2013-12-23)
++++++++++++++++++

* core: add assetId param to searchAuction method
* core: add pileSize
* core: add leagueId to item data parser


0.0.4 (2013-11-10)
++++++++++++++++++

* convert lowercase function/method names to mixedCase (send_to_tradepile -> sendToTradepile)
* drop python-2.5 (requests)
* core: python 3 support


0.0.3 (2013-10-25)
++++++++++++++++++

* core: move requests session init & headers from login to init
* core: update credits on every request (only if it is avaible included in response)


0.0.2 (2013-10-17)
++++++++++++++++++

* core: add watchlist
* core: add card_info function
* core: add alias for base_id & card_info


0.0.1 (2013-10-15)
++++++++++++++++++

* init
