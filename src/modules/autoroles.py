import discord
from discord.ext import commands

from bot import config


class AutoRoles(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        roles = []
        for role_id in config["autoroles"]:
            roles.append(member.guild.get_role(role_id))
        for role in roles:
            await member.add_roles(role)


def setup(_bot):
    _bot.add_cog(AutoRoles(_bot))
