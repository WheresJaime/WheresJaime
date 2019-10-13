import xml.etree.ElementTree as ET
from datetime import datetime
from random import choice

import tweepy
from tweepy.error import TweepError


class Bot:
  def __init__(self):
    self.LAST = datetime(year=2017, month=1, day=17)
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

    self.cache = ET.parse('cache.xml')

  def check(self):
    """
    Check if target account has posted, update the cache, fire reply if needed
    :return: none
    """
    # TODO: Check my last post time to avoid spamming
    currentId = None

    try:
      currentId = self.api.user_timeline(id="herrerabeutler", count=1)[0].id_str
    except TweepError as e:
      mode = self.cache.find('.//mode').text
      if mode != 1 and e.api_code == 136:  # We've been blocked!
        self.setMode(1)
      else:
        print("Failed to get timeline. Exception: ", e)
        exit(-3)  # Exit Code -3: Failed to get timeline for non-block reason

    cachedId = self.cache.find('.//lastTargetPost').text
    if currentId != cachedId:
      self.cache.find('.//lastTargetPost').text = currentId
      self.cache.write('cache.xml')
      # TODO: separate out and generalize zfill to include hero and reply
      postId = '90' + str(choice(range(8)) + 1)
      self._post(postId)

  def post(self):
    """
    Just post. Let cron worry about timing.
    TODO: handle timing internally, possibly as a daemon
    :return: none
    """
    div = choice([0, 1, 2])  # Probably a silly way to do this
    spec = choice(range(32))

    if div != 0:  # 1/3 ought to be default
      # post default
      postId = "000"
    else:  # 2/3 ought to be non-default
      # post non-default, chosen by spec
      # TODO: separate out and generalize zfill to include hero and reply
      postId = str(spec + 1).zfill(3)

    self._post(postId)

  def _post(self, id):
    root = ET.parse('strings.xml').getroot()
    days = (datetime.now() - self.LAST).days

    mode = int(self.cache.find('.//mode').text)

    for child in root:
      if child.attrib["id"] == id:
        text = child.text.replace("X", str(days))
        if mode == 1 or mode == 2:
          text = text.replace('@', '#')
        self.api.update_status(text)
        break

  def setMode(self, mode):
    self.cache.find('.//mode').text = mode
    self.cache.write('cache.xml')
    if mode == 1:
      # We've been blocked!
      self._post('111')
      print("MODE 1: JHB has blocked the bot")
    elif mode == 2:
      # JHB Opted Out
      # TODO: implement auto opt-out from DMs
      self._post('112')
      print("MODE 2: JHB has Opted Out")
    else:
      print("setMode encountered unknown mode")



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
  main(0)
