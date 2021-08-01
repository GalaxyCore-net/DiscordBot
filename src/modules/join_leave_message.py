import discord
from discord.ext import commands
from bot import config


class JoinLeaveMessage(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(config["join-message-channel"])
        embed = discord.Embed(title="Willkommen.",
                              description=f"Willkommen {member.mention}, "
                                          f"auf dem {config['server-name']} Discord.\n "
                                          f"Bitte lese dir die <#{config['rules-channel']}> durch.",
                              color=0x0fff0f)
        embed.set_footer(text=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        await channel.send(content="", embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.member):
        channel = self.bot.get_channel(config["leave-message-channel"])
        embed = discord.Embed(title="Auf Wiedersehen.",
                              description=f"{member.name}#{member.discriminator}, "
                                          f"hat den Server verlassen.",
                              color=0xff0000)
        embed.set_footer(text=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        await channel.send(content="", embed=embed)


def setup(_bot):
    _bot.add_cog(JoinLeaveMessage(_bot))
