import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

from bot import logger, config
from config import save_config
from utils.math import is_int


class ReactionRoles(commands.Cog):
    reaction_roles = config["reaction-roles"]

    def __init__(self, _bot):
        self.bot = _bot

    async def process_reaction(self, payload: discord.RawReactionActionEvent, r_type=None):
        for reactrole in self.reaction_roles:
            if payload.message_id == reactrole["message-id"]:
                for obj in reactrole["roles"]:
                    if obj["emoji"] == payload.emoji.name:
                        guild = self.bot.get_guild(payload.guild_id)
                        user = await guild.fetch_member(payload.user_id)
                        role = guild.get_role(obj["role"])
                        if role is None:
                            logger.debug(f"An invalid Role ID {obj['role']} was provided in Reaction Roles for message {reactrole['message-id']}")
                        elif r_type == "add":
                            await user.add_roles(role)
                        elif r_type == "remove":
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
        await self.process_reaction(payload, "add")

    @commands.command()
    @has_permissions(manage_roles=True)
    async def reactrole(self, ctx, *, args):
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
        message_id = int(message_id)
        role_id = int(role_id)
        for i in range(len(self.reaction_roles)):
            if self.reaction_roles[i]["message-id"] == message_id:
                config["reaction_roles"][i]["roles"].append({
                    "emoji": emoji,
                    "role": role_id
                })
                save_config()
                return
        config["reaction-roles"].append({
            "message-id": message_id,
            "roles": [
                {
                    "emoji": emoji,
                    "role": role_id
                }
            ]
        })
        save_config()
        message = await ctx.fetch_message(message_id)
        await message.add_reaction(emoji)
        await ctx.message.delete()
        embed = discord.Embed()
        embed.title = "Die Reaction-Role wurde erfolgreich hinzugefügt!"
        embed.colour = discord.Color(0x00ff0)

    @reactrole.error
    async def reactrole_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed()
            embed.title = "Dazu hast du keine Rechte!"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)


def setup(_bot):
    _bot.add_cog(ReactionRoles(_bot))
