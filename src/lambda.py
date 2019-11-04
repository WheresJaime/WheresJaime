from datetime import datetime

# Ignore unresolved reference
import bot # This will never be called when stored locally, so no need to specify the src folder


def lambda_handler(event, context):
  callHour = datetime.now().hour
  callMin = datetime.now().minute
  timeRange = range(callMin - 4, callMin + 5)  # Account for delays, which can apparently be in the minutes on AWS
  bot.main(0)
  if callHour % 2 == 0 and callMin in timeRange:
    bot.main(1)
  return {
    'statusCode': 200
  }
