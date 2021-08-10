import os
import sys
import discord

from discord.ext import commands
from extensions import channel_db as db
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = os.getenv('EXT_ADMIN_ID')
CHANNEL_DB_URL = os.getenv('EXT_CHANNEL_DB_URL')

CHANNEL_LIST = None

def is_channel_granted(channel_id):
    return channel_id in CHANNEL_LIST

def is_admin(user_id):
    return str(user_id) == ADMIN_ID

def is_dm(ctx):
    return isinstance(ctx.channel, discord.channel.DMChannel)

def get_list_index_value(obj, index):
    if isinstance(obj, list):
        if (index < len(obj)):
            return obj[index]
    return None

def plural_s(count):
    if count > 1:
        return 's'
    return ''

async def send(ctx, msg):
    if isinstance(msg, list):
        await ctx.send('\n'.join(str(x) for x in msg))
    else:
        await ctx.send(str(msg))

def init_extension_commands(bot, rate_limit_n, rate_limit_time):
    global CHANNEL_LIST

    @bot.command()
    @commands.cooldown(rate_limit_n, rate_limit_time, commands.BucketType.user)
    async def ping(ctx):
        if not is_admin(ctx.message.author.id):
            return
        await send(ctx, 'Pong! ({}ms)'.format(round(bot.latency, 2)))

    @bot.command()
    @commands.cooldown(rate_limit_n, rate_limit_time, commands.BucketType.user)
    async def channel(ctx):
        global CHANNEL_LIST

        if not is_admin(ctx.message.author.id):
            return

        args = ctx.message.content.split()[1:]
        args_length = len(args)
        if args_length > 0:
            command = args[0]

            if command == 'info':
                msg = []
                msg.append('Channel ID: {}'.format(ctx.channel.id))

                if db.is_channel_exist(ctx.channel.id):
                    msg.append('I\'m enabled on this channel.')
                else:
                    msg.append('I\'m not enabled on this channel.')

                await send(ctx, msg)

            elif command == 'grant':
                
                channel_id = get_list_index_value(args, 1)
                if channel_id:

                    if not is_dm(ctx):
                        return

                    if channel_id.isdigit():
                        channel_id = int(channel_id)
                        
                        if db.is_channel_exist(channel_id):
                            await send(ctx, 'I\'m already enabled on channel ID {}.'.format(channel_id))
                            return

                        if db.add_channel(channel_id):
                            CHANNEL_LIST = db.get_channel_list()
                            msg = 'I\'m now enabled on channel ID {}.'.format(channel_id)
                        else:
                            msg = 'Grant failed.'
                        await send(ctx, msg)

                    else:
                        await send(ctx, 'Invalid Channel ID.')

                else:

                    if db.is_channel_exist(ctx.channel.id):
                        await send(ctx, 'I\'m already enabled on this channel.')
                        return

                    if db.add_channel(ctx.channel.id):
                        CHANNEL_LIST = db.get_channel_list()
                        msg = 'I\'m now enabled on this channel.'
                    else:
                        msg = 'Grant failed.'
                    await send(ctx, msg)

            elif command == 'revoke':

                channel_id = get_list_index_value(args, 1)
                if channel_id:

                    if not is_dm(ctx):
                        return

                    if channel_id.isdigit():
                        channel_id = int(channel_id)

                        if not db.is_channel_exist(channel_id):
                            await send(ctx, 'I\'m not enabled channel ID {}.'.format(channel_id))
                            return

                        if db.del_channel(channel_id):
                            CHANNEL_LIST = db.get_channel_list()
                            msg = 'I\'m now disabled on channel ID {}.'.format(channel_id)
                        else:
                            msg = 'Revoke failed.'
                        await send(ctx, msg)

                    else:
                        await send(ctx, 'Invalid Channel ID.')
                else:

                    if not db.is_channel_exist(ctx.channel.id):
                        await send(ctx, 'I\'m not enabled on this channel.')
                        return

                    if db.del_channel(ctx.channel.id):
                        CHANNEL_LIST = db.get_channel_list()
                        msg = 'I\'m now disabled on this channel.'
                    else:
                        msg = 'Revoke failed.'
                    await send(ctx, msg)

            elif command == 'list':
                if not is_dm(ctx):
                    return
                
                channel_count = len(CHANNEL_LIST)

                if channel_count > 0:
                    msg = []
                    msg.append('I\'m enabled on {} channel{}.'.format(channel_count, plural_s(channel_count)))

                    count = 0
                    for channel_id in CHANNEL_LIST:
                        count += 1
                        if channel_id == ctx.channel.id:
                            msg.append('{}. {} (this channel)'.format(count, channel_id))
                        else:
                            msg.append('{}. {}'.format(count, channel_id))

                else:
                    msg = 'I\'m not enabled on any channels.'
                
                await send(ctx, msg)

    if not ADMIN_ID:
        print('Error: EXT_ADMIN_ID not found')
        sys.exit(1)

    if not CHANNEL_DB_URL:
        print('Error: EXT_CHANNEL_DB_URL not found')
        sys.exit(1)

    CHANNEL_LIST = db.get_channel_list()
