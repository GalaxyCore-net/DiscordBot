import discord
from discord.ext import commands
from sqlalchemy.orm import sessionmaker

from database import engine
from database.models import AutoRolesModel


class AutoRoles(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
        session.begin()
        roles = []
        for role in session.query(AutoRolesModel).all():
            roles.append(member.guild.get_role(role.roleid))
        for role in roles:
            await member.add_roles(role)


def setup(_bot):
    _bot.add_cog(AutoRoles(_bot))
