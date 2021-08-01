import discord
from discord.ext import commands

from bot import bot


class Ping(commands.Cog):
    def __init(self, _bot):
        self.bot = _bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed()
        embed.title = f"{str(round(bot.latency * 1000))}ms"
        await ctx.send(embed=embed)


def setup(_bot):
    _bot.add_cog(Ping(_bot))
