import xml.etree.ElementTree as ET
import tweepy
from random import choice
from datetime import datetime
import string

# 130, 200, 230

class Bot:
  def __init__(self):
    self.LAST = datetime(year=2017, month=1, day=17, hour=12)
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
    tree = ET.parse('cache.xml')

    # TODO: Check my last post time to avoid spamming
    # TODO: This, but well
    try:
      currentId = self.api.user_timeline(id="herrerabeutler", count=1)[0].id_str
      #currentId = self.api.user_timeline(id="littelbro14")[0].id_str
    except Exception as e:
      mode = tree.find('.//mode').text
      print(e)

    cachedId = tree.find('.//lastTargetPost').text
    if currentId != cachedId:
      tree.find('.//lastTargetPost').text = currentId
      tree.write('cache.xml')
      # TODO: separate out and generalize zfill to include hero and reply
      postId = '90' + str(choice(range(8)) + 1)
      self._post(postId)

  def post(self):
    """
    Just post. Let cron worry about timing.
    TODO: handle timing internally, possibly as a daemon
    :return: none
    """
    div = choice([0,1,2])  # Probably a silly way to do this
    spec = choice(range(32))

    if div != 0:  # 1/3 ought to be default
      # post default
      postId = "000"
    else:  # 2/3 ought to be non-default
      # post non-default, chosen by spec
      # TODO: separate out and generalize zfill to include hero and reply
      postId = str(spec+1).zfill(3)

    self._post(postId)

  def _post(self, id):
    root = ET.parse('strings.xml').getroot()
    days = (datetime.now() - self.LAST).days

    for child in root:
      if child.attrib["id"] == id:
        text = child.text.replace("X", str(days))

        # TODO: Go live
        #self.api.update_status(text)
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
  main(0)
