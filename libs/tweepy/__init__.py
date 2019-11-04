# Tweepy
# Copyright 2009-2019 Joshua Roesslein
# See LICENSE for details.

"""
Tweepy Twitter API library
"""
__version__ = '3.8.0'
__author__ = 'Joshua Roesslein'
__license__ = 'MIT'

from libs.tweepy import API
from libs.tweepy.auth import AppAuthHandler, OAuthHandler

# Global, unauthenticated instance of API
api = API()


def debug(enable=True, level=1):
  from libs.six import HTTPConnection
  HTTPConnection.debuglevel = level
