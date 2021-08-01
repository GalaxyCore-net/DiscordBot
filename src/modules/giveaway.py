import datetime

import discord
from discord import Member, Role
from discord.ext import commands

from bot import config, bot


def has_admin_permission(ctx: commands.context):
    member: Member = ctx.author
    roles = member.roles
    for role in roles:
        role: Role
        if role.id is config["discord-admin-role"]:
            return True
    return False


class Giveaway(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.command(aliases=["gcreate"])
    async def giveawayrceate(self, ctx, *args):
        if not has_admin_permission(ctx):
            return

        if len(args) > 3:
            int(args[0])
            int(args[1])

            win = ""
            for i in range(2, len(args)):
                win += args[i] + " "

            end = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(args[0]) * 60)

            embed = discord.Embed()
            embed.title = "Giveaway!"
            embed.colour = ctx.author.color
            embed.description = f"{win} \n{args[1]}x"
            embed.set_footer(text=f"Endet: {end} UTC", icon_url="galaxycore.net/img/favicon.png")

            await bot.get_channel(config["event-channel"]).send(embed=embed)

        else:
            embed = discord.Embed()
            embed.title = "!giveawaycreate"
            embed.description = "Verwende !gcreate <Time in minutes> <HowmanyWins> <Win>"
            embed.colour = discord.Colour(0x00ff00)
            await ctx.send(embed=embed)


def setup(_bot):
    _bot.add_cog(Giveaway(_bot))
