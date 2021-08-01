import discord
from discord.ext import commands

from bot import bot, config


class Suggestion(commands.Cog):
    def __init(self, _bot):
        self.bot = _bot

    @commands.command()
    async def vorschlag(self, ctx, *args):
        if len(args) < 2:
            embed = discord.Embed()
            embed.title = "Verwende mindestens zwei Argumente"
            await ctx.send(embed=embed)
            return

        embed = discord.Embed()
        embed.title = "Der Vorschlag wurde gesendet"

        suggestion_not = discord.Embed()
        suggestion_not.title = "Vorschlag"
        suggestion_not_description = ""
        suggestion_not_layer = ""

        layer = False

        for i in args:
            if layer:
                suggestion_not_description += i + " "
            else:
                layer = True
                suggestion_not_layer = i

        suggestion_not.add_field(name="Ebene", value=suggestion_not_layer, inline=False)
        suggestion_not.add_field(name="Vorschlag", value=suggestion_not_description, inline=False)
        suggestion_not.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        channel = bot.get_channel(config["suggestion-channel"])

        msg = await channel.send(embed=suggestion_not)
        await ctx.send(embed=embed)

        await msg.add_reaction("👍")
        await msg.add_reaction("👎")


def setup(_bot):
    _bot.add_cog(Suggestion(_bot))
