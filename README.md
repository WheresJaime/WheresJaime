**_Where's Jaime Bot_**

**About**

This is a simple bot that tweets periodically to remind Jaime Herrera-Beutler (R-WA3) that she hasn't held an in person town hall for several years now.

That's literally all.

**Use**

This code is licensed under MIT, so feel free to use it for your own projects, like pressuring your absentee representatives into talking to their constituents. 

This code is currently built around a cron job as an AWS Lambda function. It pulls the cache file from an AWS S3 server. Set those up, add your `OAuth.xml` file with pertinent info (described at the top of the Bot class `__init__` method), change the bucket name in `main()` in `bot.py` (as well as the target account and strings), and configure your cron job.

The handy `deploy.py` file can be used to package the Lambda function for upload. In the future the upload (and versioning) will also be automated.

Sometime in the distant future, I may add in a setup script to help configure for other use. Right now you have to do it manually. Sorry.

**Modes**

This bot operates in 3 modes:

_0:_ Default operating mode. Reply to JHB posts and periodically post updates with mentions of JHB.

_1:_ The bot has been blocked. Operates the same as mode 0, but @s are converted to hashtags

_2:_ JHB has opted out. Functionally the same as mode 1 for the moment.

**Opt-Out**

_JHB:_
Twitter requires bots to allow people to opt-out of receiving @s. If you are JHB or one of her staffers, you may opt-out by replying to the bot account from the JHB account with the following text: `I don't care about my constituents. Please leave me alone.` Other replies from that account will have no effect on the bot's operating mode.

_AOC or ElectLong:_ Currently, automatic opt-out is not enabled for your accounts. Sorry. Please DM the bot account, and the human behind the account will remove your accounts from the strings file. Sorry for the inconvenience.

**Quick Notes**

_Did this bot respond inappropriately to a serious subject matter?_

I truly apologize. This bot is largely unmonitored, and isn't intelligent enough to know when it shouldn't respond to something. It merely blindly responds to any tweets from JHB. It is never my intention to cause pain or offense.

_Is this bot spammy?_

This bot currently posts a new tweet every other hour, except when replying to a tweet, which is not limited and only dependent on when JHB tweets. If the 2 hour interval is too short, please let me know and I will consider adjusting based on feedback.

_Did I use something you own improperly (libs, photos, etc)?_

Sorry about that! Shoot me a DM with info (or the photo in question) and I'll fix it (whether that be removing it or providing proper attribution, based on your needs)

