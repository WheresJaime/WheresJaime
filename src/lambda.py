from datetime import datetime
import json
import sys
sys.path.append('/var/task/libs')

# Ignore unresolved reference
import bot # This will never be called when stored locally, so no need to specify the src folder

from libs.pytz import timezone


def lambda_handler(event, context):
  time = datetime.now(timezone('US/Pacific'))
  callHour = time.hour
  callMin = time.minute
  timeRange = range(callMin - 4, callMin + 5)  # Account for delays, which can apparently be in the minutes on AWS
  bot.main(0)
  if callHour % 2 == 0 and 0 in timeRange:
    bot.main(1)
  return {
    'statusCode': 200
  }

