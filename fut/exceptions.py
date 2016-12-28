# -*- coding: utf-8 -*-

"""
fut.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of fut's exceptions.

"""


class FutError(RuntimeError):
    """There was an ambiguous exception that occurred while handling
    your request."""
    def __init__(self, code=None, reason=None, string=None):
        self.code = code
        self.reason = reason
        self.string = string


class UnknownError(FutError):
    """Unknown error, please report full log at
    https://github.com/oczkers/fut/issues/24"""


class Timeout(FutError):
    """Request timeout, looks like ea servers are down."""


class ExpiredSession(FutError):
    """Session has expired,
    you should send at least one request every ~10 minutes."""


class MaxSessions(FutError):
    """[503] Service Unavailable (ut) - max session."""


class InternalServerError(FutError):
    """[500] Internal Server Error (ut). (invalid parameters?)"""


'''
class InvalidCookie(FutError):
    """[482] Invalid cookie."""
'''


class FeatureDisabled(FutError):
    """[480] Feature Disabled."""


class NoUltimateTeam(FutError):
    """[465] No Ultimate Team."""


class PermissionDenied(FutError):
    """[461] Permission Denied. (outbid?)"""


class Captcha(FutError):
    """[459] Captcha Triggered."""
    def __init__(self, code=None, reason=None, string=None, token=None, img=None):
        self.code = code
        self.reason = reason
        self.string = string
        self.token = token
        self.img = img


class Conflict(FutError):
    """[409] Conflict. (You'r trying to sell somebody's item, don't you ;-)?)"""


class Unauthorized(FutError):
    """[401] Unauthorized (ut)."""


class MultipleSession(Unauthorized):
    """[401] Unauthorized (ut) - multiple session."""


# class doLoginFail(Forbidden):
class doLoginFail(Unauthorized):
    """[403] Forbidden (ut)."""
