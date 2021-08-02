import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init(self, _bot):
        self.bot: discord.ext.commands.Bot = _bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed()
        embed.title = "Pong!"
        await ctx.send(embed=embed)


def setup(_bot):
    _bot.add_cog(Ping(_bot))
