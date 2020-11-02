import locale
import time

import discord
from discord import utils
from discord.ext import commands

TOKEN = "Gnome Is Love Gnome Is Life."
PREFIX = "?"
ROLEID = 771845335479484456

locale.setlocale(locale.LC_ALL, "en_US.utf8")
start_time = time.time()


class Bot(commands.Bot):
    def __init__(self):
        super(Bot, self).__init__(
            command_prefix=PREFIX,
            case_insensitive=True,
            max_messages=5000)

    @commands.Cog.listener()
    async def on_ready(self):
        """Output after the Bot fully loaded"""
        end_time = time.time() - start_time
        await self.change_presence(status=discord.Status.online)
        print(f'#-------------------------------#\n'
              f'| Username: {self.user.name}\n'
              f'| User ID: {self.user.id}\n'
              f'| Developer: NoirCoding Team\n'
              f'| Guilds: {len(self.guilds)}\n'
              f'| Users: {len([member for member in self.users if not member.bot])}\n'
              f'| Base OAuth URL: {utils.oauth_url(self.user.id)}\n'
              f'| Bot started in \033[92m{"%.3f" % end_time}\033[0m seconds\n'
              f'| Current Discord.py Version: {discord.__version__}\n'
              f'# ------------------------------#')


client = Bot()
client.load_extension('commands')

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after)
client.run(TOKEN)
