import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from sqlalchemy.orm import sessionmaker

from bot import logger, config
from database import engine
from database.models import ReactionRolesModel
from utils.math import is_int


class ReactionRoles(commands.Cog):

    def __init__(self, _bot):
        self.bot = _bot

    async def process_reaction(self, payload: discord.RawReactionActionEvent, r_type=None):
        session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
        session.begin()
        for reactrole in session.query(ReactionRolesModel).all():
            logger.info(reactrole)
            if payload.message_id == int(reactrole.messageid):
                logger.info("Message ID´s match")
                if reactrole.emoji == payload.emoji.name:
                    logger.info("Emojis match")
                    guild = self.bot.get_guild(payload.guild_id)
                    logger.info(f"Guild: {guild}")
                    logger.info(f"Role ID: {reactrole.roleid}")
                    user = await guild.fetch_member(payload.user_id)
                    role = guild.get_role(int(reactrole.roleid))
                    logger.info(f"User: {user}")
                    logger.info(f"Role: {role}")
                    if role is None:
                        logger.debug(f"An invalid Role ID {reactrole.roleid} was provided in Reaction Roles for message {reactrole.messageid}")
                    if r_type == "add":
                        logger.info("Add Roles")
                        await user.add_roles(role)
                    elif r_type == "remove":
                        logger.info("Remove Roles")
                        await user.remove_roles(role)
                    else:
                        logger.debug("Invalid Reaction Type was provided in reaction_roles.py 'process_reaction'")
                        logger.debug("Not performing any Action as result")
                    break

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.process_reaction(payload, "add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.process_reaction(payload, "remove")

    @commands.command()
    @has_permissions(manage_roles=True)
    async def reactrole(self, ctx, *, args):
        session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
        session.begin()
        if not args:
            return
        args = args.split(" ")
        if ctx.message.reference is None:
            if len(args) < 3:
                return
            message_id = args[0]
            emoji = args[1]
            role_id = args[2]
        else:
            if len(args) < 2:
                return
            message_id = ctx.message.reference.message_id
            emoji = args[0]
            role_id = args[1]
        if ctx.message.role_mentions:
            role_id = ctx.message.role_mentions[0].id

        if message_id is None or emoji is None or role_id is None or not (is_int(message_id) or is_int(role_id)):
            embed = discord.Embed()
            embed.title = f"Bitte benutze {config['prefix']}reactrole <message_id> <emoji> <role_id>"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)
            return
        message_id = message_id
        role_id = role_id
        new_reaction_role = ReactionRolesModel(messageid=message_id, emoji=emoji, roleid=role_id)
        session.add(new_reaction_role)
        session.commit()
        session.flush()
        message = await ctx.fetch_message(message_id)
        await message.add_reaction(emoji)
        await ctx.message.delete()

    @reactrole.error
    async def reactrole_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed()
            embed.title = "Dazu hast du keine Rechte!"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)
        else:
            logger.info(error)


def setup(_bot):
    _bot.add_cog(ReactionRoles(_bot))
