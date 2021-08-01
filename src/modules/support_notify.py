import discord
from discord.ext import commands

from bot import config, bot


class SupportNotify(commands.Cog):
    def __init(self, _bot):
        self.bot = _bot

    @commands.command()
    async def sn(self, ctx):
        if not ctx.channel.id == config["team-commands"]:
            return

        author = ctx.author

        has_role = False

        for role in author.roles:
            role: discord.Role
            if role.id == config["supportnotify-role"]:
                has_role = True

        guild = bot.get_guild(ctx.guild.id)

        if has_role:
            await author.remove_roles(guild.get_role(config["supportnotify-role"]))
            await ctx.send("Dein **SupportNotify** wurde entfernt")
        else:
            await author.add_roles(guild.get_role(config["supportnotify-role"]))
            await ctx.send("Dein **SupportNotify** wurde hinzugefügt")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if after.channel.id == config["supportnotify-channel"]:
                embed = discord.Embed()
                embed.title = f"{member.display_name} benötigt Support!"

                role = member.guild.get_role(config["supportnotify-role"])
                await bot.get_channel(config["team-commands"]).send(role.mention, embed=embed)


def setup(_bot):
    _bot.add_cog(SupportNotify(_bot))
