# PSL import
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from random import choice

# AWS imports
import boto3
import botocore

# Local imports
from libs import tweepy
from libs.tweepy.error import TweepError
from libs.pytz import timezone
from libs import pytz


class Bot:
  def __init__(self, CACHE_FILE):
    self.tz = timezone('US/Pacific')
    print(datetime.now(self.tz), " - Log: __init__")

    self.LAST = datetime(year=2017, month=1, day=17, tzinfo=self.tz)
    self.CACHE_FILE = CACHE_FILE

    self.reupload = True
    conf = ET.parse('res/OAuth.xml')
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
    except Exception as e:
      print(datetime.now(self.tz), " - Error: Twitter auth failed. Exception: ", e)
      exit(-1)  # Exit code -1: Twitter auth error
    print(datetime.now(self.tz), " - Log: Auth succeeded")

    self.cache = ET.parse(self.CACHE_FILE)

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
        print(datetime.now(self.tz), " - Error: Failed to get timeline. Exception: ", e)
        exit(-3)  # Exit Code -3: Failed to get timeline for non-block reason

    cachedId = self.cache.find('.//lastTargetPost').text
    if currentId != cachedId:
      self.cache.find('.//lastTargetPost').text = currentId
      self.cache.write(self.CACHE_FILE)
      # TODO: separate out and generalize zfill to include hero and reply
      postId = '90' + str(choice(range(8)) + 1)
      self._post(postId, replyId=currentId)
    else:
      print(datetime.now(self.tz), " - Log: No new post to reply to")

  def post(self):
    """
    Just post. Let cron worry about timing.
    TODO: handle timing internally, possibly as a daemon
    :return: none
    """
    print(datetime.now(self.tz), " - Log: Started post")
    div = choice([0, 1])  # Probably a silly way to do this

    if div != 0:  # 1/2 ought to be default
      # post default
      postId = "000"
    else:  # 1/2 ought to be non-default
      # post non-default, chosen by spec
      # TODO: separate out and generalize zfill to include hero and reply
      spec = choice(range(32))
      postId = str(spec + 1).zfill(3)

    print(datetime.now(self.tz), " - Log: postId selected: ", postId)
    self._post(postId)

  def _post(self, strId, replyId=0):
    print(datetime.now(self.tz), " - Log: internal post called with reply id: ", replyId)

    root = ET.parse('res/strings.xml').getroot()
    days = (datetime.now(self.tz) - self.LAST).days
    stamp = str(datetime.now(self.tz).hour) + ":" + str(datetime.now(self.tz).minute).zfill(2)

    mode = int(self.cache.find('.//mode').text)

    for child in root:
      if child.attrib["id"] == strId:
        text = child.text.replace("X", str(days))
        text = text.replace("Z", stamp)
        if mode == 1 or mode == 2:
          text = text.replace('@', '#')
        print(datetime.now(self.tz), " - Log: Text retrieved and altered: ", text)
        try:
          if (replyId == 0 and strId[0] != '9'):
            self.api.update_status(text)
          else:
            self.api.update_status(text, replyId)
        except TweepError as e:
          if e.api_code == 187:
            print(datetime.now(self.tz), " - Error: Duplicate tweet exception")
          else:
            print(datetime.now(self.tz), " - Error: Unknown post failed exception")
            self.reupload = False
            print(e)
        break

  def setMode(self, mode):
    self.cache.find('.//mode').text = mode
    self.cache.write(self.CACHE_FILE)
    if mode == 1:
      # We've been blocked!
      self._post('111')
      print(datetime.now(self.tz), " - Log: MODE 1: JHB has blocked the bot")
    elif mode == 2:
      # JHB Opted Out
      # TODO: implement auto opt-out from DMs
      self._post('112')
      print(datetime.now(self.tz), " - Log: MODE 2: JHB has Opted Out")
    else:
      print(datetime.now(self.tz), " - Error: setMode encountered unknown mode: ", mode)
      self.reupload = False


def main(op):
  """
  Entry Point
  :param op: 0 for check. 1 for scheduled post
  :return: none
  """
  tz = timezone('US/Pacific')
  BUCKET_NAME = 'jaimewherecache'
  FILE_NAME_REMOTE = 'cache.xml'
  FILE_NAME_LOCAL = '/tmp/cache.xml'

  s3 = boto3.resource('s3')

  try:
    s3.Bucket(BUCKET_NAME).download_file(FILE_NAME_REMOTE, FILE_NAME_LOCAL)
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
      print(" - Error: The s3 object does not exist")
    else:
      print(" - Error: s3 download failed for unknown reason. Exception: ", e)
    exit(-4)  # Exit code -3: Couldn't download cache

  bot = Bot(FILE_NAME_LOCAL)
  if op == 0:  # Check
    print(datetime.now(tz), " - Log: Started in op: 0")
    bot.check()
  elif op == 1:  # Scheduled Post
    print(datetime.now(tz), " - Log: Started in op: 1")
    bot.post()
  else:
    print(datetime.now(tz), " - Error: Unrecognized arg. You should never see this. Called with ", type(op), ": ", op)
    bot.reupload = False
    exit(-2)  # Exit code -2: Bad Arg

  if bot.reupload:
    try:
      s3.meta.client.upload_file(FILE_NAME_LOCAL, BUCKET_NAME, FILE_NAME_REMOTE)
    except Exception as e:
      print(" - Error: Reupload failed for unknown reason. Exception: ", e)
  exit(0)


if __name__ == "__main__":
  main(int(sys.argv[1]))
