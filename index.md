# fut

## Index 
### Quick Example
To log-in to the webapp and get your current coin count:

```python
>>> import fut
>>> fut = fut.Core('email', 'password', 'secret', 'platform')
>>> fut.keepalive()
15594
```
[See more quick examples in the cookbook!](link)

### What is Fut?
[![](https://img.shields.io/pypi/v/fut.svg?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://img.shields.io/pypi/l/fut.svg?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://img.shields.io/pypi/pyversions/fut.svg?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://travis-ci.org/futapi/fut.png?branch=master?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://codecov.io/github/futapi/fut/coverage.svg?raw=true)](https://pypi.python.org/pypi/fut)
[![](https://api.codacy.com/project/badge/Grade/f599808fba2447c98253cf44cca86a1b?raw=true)](https://pypi.python.org/pypi/fut)
[<img src="https://cdn.worldvectorlogo.com/logos/slack.svg" alt="alt text" width="70" height="50">](https://gentle-everglades-93932.herokuapp.com)

fut is a simple Python library for managing Fifa Ultimate Team. The library enables programmatic access to the official [FUT Web App and FIFA Companion App](https://www.easports.com/fifa/ultimate-team/web-app/). If you prefer php language, there is ported version made by InkedCurtis available here: https://github.com/InkedCurtis/FUT-API.

#### Functionality

The fut library can perform 28 basic [REST](https://spring.io/understanding/REST) functions on your Fifa Ultimate Team. It also includes 6 properties that provide access to various FUT databases (nations, leagues, teams, stadiums, balls, players, playStyles).


#### The FUT Web App

The basic layout of the FUT Web App is below. There are 5 primary categories: Squads, Squad Building Challenge, Transfers, Store, and Club. You can perform several actions in each category with the methods available in the fut library, but not all actions in the Web App have yet been mapped out. **Click on a category below** to learn more about the methods currently available in the fut library. 

[<img src="https://i.imgur.com/uvsXykU.png" alt="FUT Squads" style="height: 100px;"/>](https://jbt.github.io/markdown-editor/#ZZFPT9xADMXv+RRPyQVWKAtXKD206rGiEos4IISGiTexmni2M04hfHo8k6VC6m08fv7zfm6wn7VqGtz+mV2XYM8G3+cYSRS36pSqbzSGF3CCDgR/TKWcQthbuXjlIG5kXfDCOrAU5Wazttxs4E3bh7i0uBHCRDqEDvTKSa1pQCSd41p0GN1CMSEIljBHOOv9l5Byp7PSPcyKyYnriywiWFkEK02pXU0c01Ne00mH3c3uHi4SJChY/Dh31GGhHJShRgAjP0eXN6yqLzz1SNFf14PqIV1ut9za1xxbH6btnf/x9rbr2oP0Ndyo1/VqszYky0hWRNwPeomL8/PD61W9/VoVpj+L65TfFtnItpg6Oa2qT8GRRYKzjZJmwB2vfCNTOgM5P8AHUcfC0puFfYiTywq45wwnyAfG7O8/ii0eduU6/zT7UGbYnezGI8tvo2NMqX08aVbRUxY9ZdEpfi3mQ8p2qVB9Bw==)

[<img src="https://i.imgur.com/qHZ7jMZ.png" alt="FUT SBS" style="height: 100px;"/>](https://jbt.github.io/markdown-editor/#ZZFPT9xADMXv+RRPyQVWKAtXKD206rGiEos4IISGiTexmni2M04hfHo8k6VC6m08fv7zfm6wn7VqGtz+mV2XYM8G3+cYSRS36pSqbzSGF3CCDgR/TKWcQthbuXjlIG5kXfDCOrAU5Wazttxs4E3bh7i0uBHCRDqEDvTKSa1pQCSd41p0GN1CMSEIljBHOOv9l5Byp7PSPcyKyYnriywiWFkEK02pXU0c01Ne00mH3c3uHi4SJChY/Dh31GGhHJShRgAjP0eXN6yqLzz1SNFf14PqIV1ut9za1xxbH6btnf/x9rbr2oP0Ndyo1/VqszYky0hWRNwPeomL8/PD61W9/VoVpj+L65TfFtnItpg6Oa2qT8GRRYKzjZJmwB2vfCNTOgM5P8AHUcfC0puFfYiTywq45wwnyAfG7O8/ii0eduU6/zT7UGbYnezGI8tvo2NMqX08aVbRUxY9ZdEpfi3mQ8p2qVB9Bw==)

[<img src="https://i.imgur.com/yavAJma.png" alt="FUT Transfers" style="height: 100px;"/>](https://jbt.github.io/markdown-editor/#ZZFPT9xADMXv+RRPyQVWKAtXKD206rGiEos4IISGiTexmni2M04hfHo8k6VC6m08fv7zfm6wn7VqGtz+mV2XYM8G3+cYSRS36pSqbzSGF3CCDgR/TKWcQthbuXjlIG5kXfDCOrAU5Wazttxs4E3bh7i0uBHCRDqEDvTKSa1pQCSd41p0GN1CMSEIljBHOOv9l5Byp7PSPcyKyYnriywiWFkEK02pXU0c01Ne00mH3c3uHi4SJChY/Dh31GGhHJShRgAjP0eXN6yqLzz1SNFf14PqIV1ut9za1xxbH6btnf/x9rbr2oP0Ndyo1/VqszYky0hWRNwPeomL8/PD61W9/VoVpj+L65TfFtnItpg6Oa2qT8GRRYKzjZJmwB2vfCNTOgM5P8AHUcfC0puFfYiTywq45wwnyAfG7O8/ii0eduU6/zT7UGbYnezGI8tvo2NMqX08aVbRUxY9ZdEpfi3mQ8p2qVB9Bw==)

[<img src="https://i.imgur.com/oQpJmDZ.png" alt="FUT Store" style="height: 100px;"/>](https://jbt.github.io/markdown-editor/#ZZFPT9xADMXv+RRPyQVWKAtXKD206rGiEos4IISGiTexmni2M04hfHo8k6VC6m08fv7zfm6wn7VqGtz+mV2XYM8G3+cYSRS36pSqbzSGF3CCDgR/TKWcQthbuXjlIG5kXfDCOrAU5Wazttxs4E3bh7i0uBHCRDqEDvTKSa1pQCSd41p0GN1CMSEIljBHOOv9l5Byp7PSPcyKyYnriywiWFkEK02pXU0c01Ne00mH3c3uHi4SJChY/Dh31GGhHJShRgAjP0eXN6yqLzz1SNFf14PqIV1ut9za1xxbH6btnf/x9rbr2oP0Ndyo1/VqszYky0hWRNwPeomL8/PD61W9/VoVpj+L65TfFtnItpg6Oa2qT8GRRYKzjZJmwB2vfCNTOgM5P8AHUcfC0puFfYiTywq45wwnyAfG7O8/ii0eduU6/zT7UGbYnezGI8tvo2NMqX08aVbRUxY9ZdEpfi3mQ8p2qVB9Bw==)

[<img src="https://i.imgur.com/m8WVY9X.png" alt="FUT Club" style="height: 100px;"/>](https://jbt.github.io/markdown-editor/#ZZFPT9xADMXv+RRPyQVWKAtXKD206rGiEos4IISGiTexmni2M04hfHo8k6VC6m08fv7zfm6wn7VqGtz+mV2XYM8G3+cYSRS36pSqbzSGF3CCDgR/TKWcQthbuXjlIG5kXfDCOrAU5Wazttxs4E3bh7i0uBHCRDqEDvTKSa1pQCSd41p0GN1CMSEIljBHOOv9l5Byp7PSPcyKyYnriywiWFkEK02pXU0c01Ne00mH3c3uHi4SJChY/Dh31GGhHJShRgAjP0eXN6yqLzz1SNFf14PqIV1ut9za1xxbH6btnf/x9rbr2oP0Ndyo1/VqszYky0hWRNwPeomL8/PD61W9/VoVpj+L65TfFtnItpg6Oa2qT8GRRYKzjZJmwB2vfCNTOgM5P8AHUcfC0puFfYiTywq45wwnyAfG7O8/ii0eduU6/zT7UGbYnezGI8tvo2NMqX08aVbRUxY9ZdEpfi3mQ8p2qVB9Bw==)

#### Other FUT databases

The fut library has the following databases inside of it. Click on one property below to see an example:  
**players**  
**playStyles**  
**nations**  
**leagues**  
**teams**  
**stadiums**

A database for consumables (contracts, healing, fitness, training, position changes, chemistry styles, managers) has not been included in the library, but a csv file including detailed consumables information by koolaidjones can be found here: https://github.com/koolaidjones/FUT-Consumables-Resource-IDs.


