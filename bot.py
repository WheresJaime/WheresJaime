import xml.etree.ElementTree as ET
import tweepy

def main():
  conf = ET.parse('config.xmls')

  auth = tweepy.OAuthHandler("rhAY860C1DuGoUfFJoF2tgv6K", "3gXa5BCKGzkKaIlVFwAgMplpVa4MmO47i4TsOO66TmO4lsLYSa")
  auth.set_access_token("1182123915239288832-4Nc2JXBTcykBHruWQ0VzWbGg5JMAXU", "mdkhYQToTKwvTBPsux1EzyTiw8Hc8VBW5eNqNg33ci7xa")

  api = tweepy.API(auth)

  try:
    api.verify_credentials()
  except:
    print("Twitter authentication failed.")

  api.update_status(".@littelbro14 This is a test of the 'at' system.");


if __name__ == "__main__":
  main()
