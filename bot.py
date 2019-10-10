import xml.etree.ElementTree as ET
import tweepy

# 130, 200, 230

def main(arg):
  """
  Entry Point
  :param x: 0 for check. 1 for scheduled post
  :return: none
  """
  conf = ET.parse('config.xmls')
  confRoot = conf.getroot()

  auth = tweepy.OAuthHandler(confRoot[0].text, confRoot[1].text)
  auth.set_access_token(confRoot[2].text, confRoot[3].text)

  api = tweepy.API(auth)

  try:
    api.verify_credentials()
  except:
    print("Twitter authentication failed.")
    exit(-1)  # Exit code -1: Twitter Auth error

  if arg == 0:  # Check
    pass
  elif arg == 1:  # Scheduled Post
    pass
  else:
    print("Unrecognized arg. Called with ", type(arg), ": ", arg)
    exit(-2)  # Exit code -2: Bad Arg


if __name__ == "__main__":
  main('x')
