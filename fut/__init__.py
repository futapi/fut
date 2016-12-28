# -*- coding: utf-8 -*-

"""
fut
~~~~~~~~~~~~~~~~~~~~~

fut is a simple library for managing Fifa Ultimate Team.

Basic usage:

    >>> import fut
    >>> fifa = fut.Core('email', 'password', 'secret_answer')
    >>> items = fut.searchAuctions('development')
    >>> fut.bid(items[0]['trade_id'], 600)
    True
    >>> fut.sell(item['item_id'], 150)
    1123321


:copyright: (c) 2013 by Piotr Staroszczyk.
:license: GNU GPLv3, see LICENSE for more details.

"""

__title__ = 'fut'
__version__ = '0.2.5'
__author__ = 'Piotr Staroszczyk'
__author_email__ = 'piotr.staroszczyk@get24.org'
__license__ = 'GNU GPL v3'
__copyright__ = 'Copyright 2013 Piotr Staroszczyk'


# from .api import baseId, cardInfo
from .core import Core
