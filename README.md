**This is a private version of bot, see details below.**

*-- Original README.md start --*

# Genshin Artifact Rater - https://discord.gg/SyGmBxds3M

Discord bot that rates an artifact against an optimal 5* artifact. Put the command and image in the same message.

If you would like to add it to your private server use the link: \
https://discord.com/api/oauth2/authorize?client_id=774612459692621834&permissions=19456&scope=bot

You can also use the bot by sending the command in a DM to Artifact Rater#6924.

If you have any issues, please contact shrubin#1866 on discord or use the `-feedback` command.

## Usage

```
-rate <image/url> [lvl=<level>] [<stat>=<weight> ...]
```

#### Default Weights

ATK%, DMG%, Crit - 1 \
ATK, EM, Recharge - 0.5 \
Everything else - 0

### Options
#### Level
Compare to specified artifact level (defaults to parsed artifact level)
```
-rate lvl=20
```

#### Weights
Set custom weights (valued between 0 and 1)
```
-rate atk=1 er=0 atk%=0.5
```
\<stat> is any of HP, HP%, ATK, ATK%, ER (Recharge), EM, PHYS, CR (Crit Rate), CD (Crit Damage), ELEM (Elemental DMG%), Heal, DEF, DEF%

## Development
If you need help or want to contribute, feel free to DM shrubin#1866 or join https://discord.gg/SyGmBxds3M

### Setup
```
python3.8 -m pip install -r requirements.txt
```

Set up a bot on the Discord Developer Portal \
Go to https://ocr.space and get an API key

Store environment variables for OCR Space and Discord in `.env`
```
DISCORD_TOKEN=<token>
OCR_SPACE_API_KEY=<key>
```

Optional: \
Set a Discord `CHANNEL_ID=<id>` to receive messages when the bot goes up/down \
Set `DEVELOPMENT=True` to divert all messages to `CHANNEL_ID`

### Run the bot
```
python3.8 bot.py
```

### Run one-off
Edit `url` in `rate_artifact.py`
```
python3.8 rate_artifact.py
```

*-- Original README.md end --*

# Modifications
This is a forked project, I&#39;m trying to avoid as much modification to the original code just in case the original project is updated, I may easily apply the modifications I made to this project to the new one.

The original bot can be freely use by everyone via DM or by adding it to a channel in a Discord server.

In this version, the bot is turned into a private bot, the bot&#39;s main functionality can only be used to the channel(s) allowed by the bot admin.

### Added bot admin commands

#### DM commands:

`-channel list` lists the channel IDs where the bot is allowed to respond

`-channel grant CHANNEL_ID` enable the bot to respond to the given channel

`-channel revoke CHANNEL_ID` disable the bot to respond to the given channel

#### Channel commands:

`-channel grant` enable the bot to respond to the current channel

`-channel revoke` disable the bot to respond to the current channel

#### DM/Channel commands:

`-channel info` shows the current channel ID and to check if the bot is enabled/disabled in the channel

`-ping` ping the bot

### Additional setup

This additional environment variables must be added in `.env`
```
EXT_ADMIN_ID=<discord_user_id>
EXT_CHANNEL_DB_URL=<channel_db_path>
```

Example `.env` file
```
DISCORD_TOKEN=zI2g0FFXj2ncjJfz3F4Q0lk6.UAkp-u.LdecfRzCa6NIVV892M5jpeEzKow
OCR_SPACE_API_KEY=ggHpcldNFAjl84C
DATABASE_URL=sqlite:///database.db

EXT_ADMIN_ID=900000000000000000
EXT_CHANNEL_DB_URL=sqlite:///extensions/channels.db
```
