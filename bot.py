import xml.etree.ElementTree as ET
import tweepy
from random import choice

# 130, 200, 230

class Bot:
  def __init__(self):
    conf = ET.parse('OAuth.xmls')
    confRoot = conf.getroot()

    self._consumer_key = confRoot[0].text
    self._consumer_key_secret = confRoot[1].text
    self._access_token = confRoot[2].text
    self._access_token_secret = confRoot[3].text

    auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_key_secret)
    auth.set_access_token(self._access_token, self._access_token_secret)

    self.api = tweepy.API(auth)

    try:
      self.api.verify_credentials()
    except:
      print("Twitter auth failed.")
      exit(-1)  # Exit code -1: Twitter auth error

  def check(self):
    """
    Check if target account has posted, update the cache, fire reply if needed
    :return: none
    """
    pass

  def post(self):
    """
    Just post. Let cron worry about timing.
    TODO: handle timing internally, possibly as a daemon
    :return: none
    """
    root = ET.parse('strings.xml').getroot()
    div = choice([0,1,2])  # Probably a silly way to do this
    spec = choice(range(32))

    if div != 0:  # 1/3 ought to be default
      # post default
      postId = "000"
      pass
    else:  # 2/3 ought to be non-default
      # post non-default, chosen by spec
      postId = str(spec+1).zfill(3)

    # TODO: Separate out into own method and generalize for replies and heroes also
    for child in root:
      if child.attrib["id"] == postId:
        print(child.text)  # TODO: go live
        break


def main(op):
  """
  Entry Point
  :param op: 0 for check. 1 for scheduled post
  :return: none
  """
  bot = Bot()

  if op == 0:  # Check
    bot.check()
  elif op == 1:  # Scheduled Post
    bot.post()
  else:
    print("Unrecognized arg. Called with ", type(op), ": ", op)
    exit(-2)  # Exit code -2: Bad Arg


if __name__ == "__main__":
  main(1)
