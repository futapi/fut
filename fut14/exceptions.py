# -*- coding: utf-8 -*-

"""
fut14.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of fut14's exceptions.

"""


class Fut14Error(RuntimeError):
    """There was an ambiguous exception that occurred while handling
    your request."""

class UnknownError(Fut14Error):
    """Unknown error, please report full log at
    https://github.com/oczkers/fut14/issues/24"""

class ExpiredSession(Fut14Error):
    """Session has expired,
    you should send at least one request every ~10 minutes."""

class InternalServerError(Fut14Error):
    """[500] Internal Server Error (ut). (invalid parameters?)"""

class PermissionDenied(Fut14Error):
    """[461] Permission Denied. (outbid?)"""
