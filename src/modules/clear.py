import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument

from bot import bot, logger
from utils.math import is_int
from utils.message import no_permission


class Clear(commands.Cog):

    def __init__(self, _bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        if is_int(amount):
            amount = int(amount) + 1
            await ctx.channel.purge(limit=amount)

            embed = discord.Embed(title="Nachrichten gelöscht", description=f"{amount - 1} Nachrichten wurden gelöscht.",
                                  color=discord.Color(0x0fff0f))

            await ctx.channel.send(embed=embed, delete_after=3)
            logger.debug(f"Cleared {amount - 1} messages in #{ctx.channel.name}")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)
        elif isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title="Falsche Benutzung", description="Bitte benutze " + bot.config["prefix"] + "clear <Nachrichtenzahl>",
                                  color=discord.Color(0xff0000))

            await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(title=error)
            await ctx.send(embed, delete_after=5)
        logger.debug(f"Error in clear command: \n{error}")


def setup(_bot):
    _bot.add_cog(Clear(_bot))
