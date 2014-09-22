# -*- coding: utf-8 -*-

"""
fut.log
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's logger.

"""

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


def logger(save=False):
    """Init and configure logger."""
    logformat = '%(asctime)s [%(levelname)s] [%(name)s] %(funcName)s: %(message)s (line %(lineno)d)'

    logger = logging.getLogger()

    if save:
        log_file_path = 'fut.log'  # TODO: define logpath
        open(log_file_path, 'w').write('')  # remove old logs
        logger.setLevel(logging.DEBUG)
        logger_handler = logging.FileHandler(log_file_path)
        logger_handler.setFormatter(logging.Formatter(logformat))
    else:
        logger_handler = NullHandler()

    logger.addHandler(logger_handler)

    return logger
