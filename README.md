**_Where's Jaime Bot_**

**About**

This is a simple bot that tweets periodically to remind Jaime Herrera-Beutler (R-WA3) that she hasn't held an in person town hall for several years now.

That's literally all.

**Use**

This code is licensed under MIT, so feel free to use it for your own projects, like pressuring your absentee representatives into talking to their constituents. Right now this program needs to run on a cron job (2, actually, one to check for opt-out DMs and new posts to reply to (`arg = 0`), and one to post the regular updates (`arg = 1`)).

**Modes**

This bot operates in 3 modes:

_0:_ Default operating mode. Reply to JHB posts and periodically post updates with mentions of JHB.

_1:_ The bot has been blocked. Operates the same as mode 0, but @s are converted to hashtags

_2:_ JHB has opted out. Functionally the same as mode 1 for the moment.

**Opt-Out**

_JHB:_
Twitter requires bots to allow people to opt-out of receiving @s. If you are JHB or one of her staffers, you may opt-out by replying to the bot account from the JHB account with the following text: `I don't care about my constituents. Please leave me alone.` Other replies from that account will have no effect on the bot's operating mode.

_AOC or ElectLong:_ Currently, automatic opt-out is not enabled for your accounts. Sorry. Please DM the bot account, and the human behind the account will remove your accounts from the strings file. Sorry for the inconvenience.