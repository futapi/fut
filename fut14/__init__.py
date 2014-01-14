# -*- coding: utf-8 -*-

"""
fut14
~~~~~~~~~~~~~~~~~~~~~

fut14 is a simple library for managing Fifa 14 Ultimate Team.

Usage:

    >>> import fut14
    to be continued ;-)


:copyright: (c) 2013 by Piotr Staroszczyk.
:license: GNU GPLv3, see LICENSE for more details.

"""

__title__ = 'fut14'
__version__ = '0.0.7'
__author__ = 'Piotr Staroszczyk'
__author_email__ = 'piotr.staroszczyk@get24.org'
__license__ = 'GNU GPL v3'
__copyright__ = 'Copyright 2013 Piotr Staroszczyk'


# logging
import logging
log_file_path = 'fut14.log'  # TODO: define logpath
open(log_file_path, 'w').write('')  # remove old logs

logformat = '%(asctime)s [%(levelname)s] [%(name)s] %(funcName)s: %(message)s (line %(lineno)d)'

logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.WARNING)
logger_handler = logging.FileHandler(log_file_path)
logger_handler.setFormatter(logging.Formatter(logformat))
logger.addHandler(logger_handler)


#from .api import baseId, cardInfo
from .core import Core
