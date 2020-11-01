import random

import discord
from discord.ext import commands

from main import client, ROLEID


def _getline(command: str):
    with open(f"./{command}.txt", mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        value = random.choice(lines)
        file.close()
    if command == "unbanned":
        del lines[lines.index(value)]
        new_file = open(f"./unbanned.txt", mode="w+", encoding="utf-8")
        for line in lines:
            new_file.write(line)
        new_file.close()
    return value


class Commands(commands.Cog):
    def __init__(self):
        self.bot = client

    @commands.command(name="ping")
    async def _ping(self, ctx):
        """Ping the Bot"""
        calc = await ctx.send(embed=discord.Embed(description="Ping"))
        clientping = (calc.created_at - ctx.message.created_at).total_seconds() * 1000
        await calc.edit(embed=discord.Embed(
            description=f"Bot Latency ``{round(self.bot.latency * 1000)}``\nClient Latency ``{clientping}``\n",
            delete_after=10))

    @commands.command(name="banned")
    @commands.has_role(int(ROLEID))
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _banned(self, ctx):
        line = _getline("banned")
        embed = discord.Embed(title="Account Information")
        embed.add_field(name="Email", value=line.split(":")[0], inline=False)
        embed.add_field(name="Password", value=line.split(":")[1], inline=False)
        await ctx.author.send(embed=embed, delete_after=60)
        await ctx.send("Generated a banned alt. Check your DMs!", delete_after=59)

    @commands.command(name="unbanned")
    @commands.has_role(int(ROLEID))
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _unbanned(self, ctx):
        line = _getline("unbanned")
        embed = discord.Embed(title="Account Information")
        embed.add_field(name="Email", value=line.split(":")[0], inline=False)
        embed.add_field(name="Password", value=line.split(":")[1], inline=False)
        await ctx.author.send(embed=embed,  delete_after=60)
        await ctx.send("Generated an unbanned alt. Check your DMs!", delete_after=59)

    @commands.command(name="compare")
    @commands.has_role(int(ROLEID))
    async def _compare(self, ctx):
        with open(f"./banned.txt", mode="r", encoding="utf-8") as banned_file:
            banned = len(banned_file.readlines())
            banned_file.close()
        with open(f"./unbanned.txt", mode="r", encoding="utf-8") as unbanned_file:
            unbanned = len(unbanned_file.readlines())
            unbanned_file.close()
        embed = discord.Embed(title="File Comparison", description=f"Banned: {banned}\nUnbanned: {unbanned}")
        await ctx.send(embed=embed, delete_after=60)
        


def setup(bot):
    bot.add_cog(Commands())
