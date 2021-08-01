import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Hilfe", description=open("config/helptext.txt", "r").read(),
                              color=0x0fff0f)
        await ctx.send(embed=embed)


def setup(_bot):
    _bot.add_cog(Help(_bot))
