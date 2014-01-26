# -*- coding: utf-8 -*-

"""
fut14.log
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut14's logger.

"""

import logging


def logger(level='WARNING'):
    """Init and configure logger."""
    log_file_path = 'fut14.log'  # TODO: define logpath
    open(log_file_path, 'w').write('')  # remove old logs

    logformat = '%(asctime)s [%(levelname)s] [%(name)s] %(funcName)s: %(message)s (line %(lineno)d)'

    logger = logging.getLogger()
    if level == 'WARNING': logger.setLevel(logging.WARNING)
    elif level == 'INFO':  logger.setLevel(logging.INFO)
    elif level == 'DEBUG': logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(log_file_path)
    logger_handler.setFormatter(logging.Formatter(logformat))
    logger.addHandler(logger_handler)

    return logger
