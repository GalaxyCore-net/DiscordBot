import discord
from discord.ext import commands


class ServerInfo(commands.Cog):
    def __init(self, _bot):
        self.bot = _bot

    @commands.command()
    async def serverinfo(self, ctx):

        guild = ctx.guild

        embed = discord.Embed()
        embed.title = "Serverinfo"

        embed.add_field(name="Servername", value=f"{guild.name}", inline=False)
        embed.add_field(name="Mitglieder", value=f"{guild.member_count}", inline=False)
        embed.add_field(name="Besitzer", value=f"{guild.owner.name}", inline=False)
        embed.add_field(name="Textkanäle", value=f"{len(guild.text_channels)}", inline=False)
        embed.add_field(name="Sprachkanäle", value=f"{len(guild.voice_channels)}", inline=False)
        embed.add_field(name="Botentwickler", value=f"Flo Mit H", inline=False)
        embed.colour = discord.Color(0x5f34aa)

        await ctx.send(embed=embed)


def setup(_bot):
    _bot.add_cog(ServerInfo(_bot))
