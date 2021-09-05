# Message LeaderBot
Discord bot to track how many messages a user has in a server.

## Setup
With python 3.9 (or newer) and `discord.py` installed, download/copy and execute [main.py](https://github.com/RafaeI11/Message_LeaderBot/blob/main/main.py). A token will be requested, which you can get from your bot profile. After that the bot will be running.

If your bot is in more than one server and you want to be safe, download/copy [file_saver.py](https://github.com/RafaeI11/Message_LeaderBot/blob/main/file_saver.py) and keep it running alongside the bot. A json file will be created for every server the bot is in and it'll be updated every 24 hours.

## Command List

### Mod Commands:

`-autoupdate` : turns on/off automatic addition of new users to the leaderboard

`-edit <user_id> <message_number>`: update a user's message number

`-delete <user_id>`: delete a user from the leaderboard

`-alt <user_id> <alt_id>`: adds up the alt's messages to the user's messages (1 alt per user)

`-removealt <user_id> <alt_id>`: removes alt from user

`-addbot <user>`: saves a user as a bot (displayed on the bottom of the leaderboard)

`-rmvbot <user>`: removes bot tag from a user

`-minimum <value>`: change the minimum amount of messages necessary to appear on the leaderboard (defaults to 20000)

### Global Commands:

`-name`: updates author's name on the leadeboard

`-minfo`: prints the current minimum value to appear on the leaderboard

`-source`: prints the source code link

`-msglb`: prints the message leaderboard

`-msg <username>`: prints the user's message number

`-help`: prints help message
