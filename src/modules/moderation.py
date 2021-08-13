import asyncio
import time
from threading import Thread

import discord
from discord.ext import commands
from sqlalchemy.orm import sessionmaker

import bot
from bot import config
from database import engine
from database.models import MutesModel, BanModel
from utils.math import is_int


def has_role(member: discord.Member, role: int):
    for curr in member.roles:
        if curr.id == role:
            return True
        permissions: discord.Permissions = curr.permissions
        if permissions.administrator:
            return True
    return False


class Moderation(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason="Fehlverhalten"):
        if has_role(member=member, role=config["permaban-role"]):
            embed = discord.Embed()

            embed.title = f"Du wurdest von {config['server-name']} gebannt!"
            embed.colour = discord.Color(0xff0000)
            embed.description = f"Grund: {reason}"

            session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
            new_ban = BanModel(userid=member.id, expires=-1, reason=reason, guildid=member.guild.id)
            session.begin()
            session.add(new_ban)
            session.commit()
            session.flush()
            session.close()

            await member.send(embed=embed)
            await member.ban(reason=reason)
            channel = self.bot.get_channel(config["mod-log"])

            embed.title = f"Der User {member.name}#{member.discriminator} wurde gebannt"
            channel.send(embed=embed)
            await ctx.message.delete()
        else:
            embed = discord.Embed()

            embed.title = "Dazu hast du keine Rechte!"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def mute(self, ctx, member: discord.Member, _time, unit, *, reason="Fehlverhalten"):

        if has_role(member=ctx.author, role=config["moderation-role"]):

            if is_int(_time):

                _time = int(_time)
                muterole = ctx.guild.get_role(config["muted-role"])
                await member.add_roles(muterole)
                add = 0
                if unit == "m":
                    add = _time * 60
                elif unit == "h":
                    add = _time * 60 * 60
                elif unit == "d":
                    add = _time * 60 * 60 * 24
                elif unit == "w":
                    add = _time * 60 * 60 * 24 * 7
                elif unit == "y":
                    add = 31556926
                expires = time.time() + add

                session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
                new_mute = MutesModel(userid=member.id, expires=expires, reason=reason, guildid=member.guild.id)
                session.begin()
                session.add(new_mute)
                session.commit()
                session.flush()
                session.close()

                embed = discord.Embed()
                embed.title = f"{member.name}#{member.discriminator} wurde gemutet"
                if unit == "m":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Minute(n) gemutet"
                elif unit == "h":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Stunde(n) gemutet"
                elif unit == "d":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Tag(e) gemutet"
                elif unit == "w":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Woche(n) gemutet"
                elif unit == "y":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Jahr(e) gemutet"
                embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
                embed.colour = discord.Color(0xff0000)
                await ctx.message.delete()

                channel = ctx.guild.get_channel(config["mod-log"])
                await channel.send(embed=embed)

            else:
                embed = discord.Embed()
                embed.title = "Falsche Benutzung!"
                embed.description = f"Bitte benutze {self.bot.command_prefix}mute <@user> <zeit> <zeiteinheit> [Grund]"
                embed.colour = discord.Color(0xff0000)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed()
            embed.title = "Dazu hast du keine Rechte!"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def tempban(self, ctx, member: discord.Member, _time, unit, *, reason="Fehlverhalten"):
        if has_role(member=ctx.author, role=config["moderation-role"]):

            if is_int(time):

                embed = discord.Embed()

                embed.title = f"Du wurdest von {config['server-name']} gebannt!"
                embed.colour = discord.Color(0xff0000)
                embed.description = f"Grund: {reason}"

                await member.send(embed=embed)
                await member.ban(reason=reason)

                _time = int(_time)
                add = 0
                if unit == "m":
                    add = _time * 60
                elif unit == "h":
                    add = _time * 60 * 60
                elif unit == "d":
                    add = _time * 60 * 60 * 24
                elif unit == "w":
                    add = _time * 60 * 60 * 24 * 7
                elif unit == "y":
                    add = 31556926
                if add > 31556926:
                    add = 31556926
                expires = time.time() + add

                session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
                new_ban = BanModel(userid=member.id, expires=expires, reason=reason, guildid=member.guild.id)
                session.begin()
                session.add(new_ban)
                session.commit()
                session.flush()
                session.close()

                embed = discord.Embed()
                embed.title = f"{member.name}#{member.discriminator} wurde temporär gebannt"
                if unit == "m":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Minute(n) gebannt"
                elif unit == "h":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Stunde(n) gebannt"
                elif unit == "d":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Tag(e) gebannt"
                elif unit == "w":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Woche(n) gebannt"
                elif unit == "y":
                    embed.description = f"{member.name}#{member.discriminator} wurde für {_time} Jahr(e) gebannt"
                embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
                embed.colour = discord.Color(0xff0000)
                await ctx.message.delete()

                channel = ctx.guild.get_channel(config["mod-log"])
                await channel.send(embed=embed)

            else:
                embed = discord.Embed()
                embed.title = "Falsche Benutztung!"
                embed.description = f"Bitte benutze {self.bot.command_prefix}tempban <@user> <zeit> <zeiteinheit> [grund]"
                embed.colour = discord.Color(0xff0000)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed()
            embed.title = "Dazu hast du keine Rechte!"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def unban(self, ctx, member_id):
        if has_role(member=ctx.author, role=config["permaban-role"]):

            if is_int(member_id):

                banned_users = await ctx.guild.bans()

                for ban_entry in banned_users:
                    user = ban_entry.user

                    if user.id == member_id:
                        await ctx.guild.unban(user)

                        session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
                        session.begin()
                        session.query(BanModel) \
                            .filter(BanModel.userid == str(user.id)) \
                            .filter(BanModel.guildid == str(ctx.guild.id)) \
                            .delete()
                        session.commit()
                        session.flush()
                        session.close()

                        embed = discord.Embed()
                        embed.title = f"{user.name}#{user.discriminator} wurde entbannt!"
                        embed.colour = discord.Color(0x00ff00)
                        await ctx.message.delete()

                        channel = ctx.guild.get_channel(config["mod-log"])
                        await channel.send(embed=embed)
            else:
                embed = discord.Embed()
                embed.title = "Falsche Benutztung!"
                embed.description = f"Bitte benutze {self.bot.command_prefix}unban <userid>"
                embed.colour = discord.Color(0xff0000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = "Dazu hast du keine Rechte!"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if has_role(member=ctx.author, role=config["moderation-role"]):
            embed = discord.Embed()

            embed.title = f"Du wurdest von {config['server-name']} gekickt!"
            embed.colour = discord.Color(0xff0000)
            embed.description = f"Grund: {reason}"

            await member.send(embed=embed)
            await member.kick(reason=reason)

            channel = ctx.guild.get_channel(config["mod-log"])
            embed.title = f"Der User {member.name}#{member.discriminator} wurde gekickt"
            await channel.send(embed=embed)
            await ctx.message.delete()
        else:
            embed = discord.Embed()

            embed.title = "Dazu hast du keine Rechte!"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if has_role(member=ctx.author, role=config["moderation-role"]):

            await member.remove_roles(ctx.guild.get_role(config["muted-role"]))
            embed = discord.Embed()
            embed.title = f"Du wurdest von {config['server-name']} entmutet!"
            embed.colour = discord.Color(0x00ff00)

            await member.send(embed=embed)

            embed = discord.Embed()
            embed.title = f"Der User {member.name}#{member.discriminator} wurde entmutet"
            embed.colour = discord.Color(0x00ff00)

            channel = ctx.guild.get_channel(config["mod-log"])
            await channel.send(embed=embed)
            await ctx.message.delete()
        else:
            embed = discord.Embed()
            embed.title = "Dazu hast du keine Rechte!"
            embed.colour = discord.Color(0xff0000)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_meber_join(self, member):
        session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
        if session.query(MutesModel) \
                .filter(MutesModel.userid == member.id) \
                .filter(MutesModel.guildid == member.guild.id) \
                .count() > 0:
            muterole = await member.guild.get_role(config["muted-role"])
            await member.add_roles(muterole)


def setup(_bot):
    _bot.add_cog(Moderation(_bot))


exit_flag = False


async def unmute_ban_async():
    while True:
        session = sessionmaker(bind=engine, autocommit=True)()
        session.begin()
        for mute in session.query(MutesModel).all():
            if float(mute.expires) < time.time():
                guild = bot.bot.get_guild(id=int(mute.guildid))
                for _guild in guilds:
                    if _guild.id == int(mute.guildid) and not guild:
                        guild = _guild
                member: discord.Member = await guild.fetch_member(int(mute.userid))
                role = guild.get_role(config["muted-role"])
                await member.remove_roles(role)
                session.delete(mute)
                session.commit()
                session.flush()
                session.close()
        for ban in session.query(BanModel).all():
            if float(ban.expires) < time.time():
                guild = bot.bot.get_guild(id=int(ban.guildid))
                for _guild in guilds:
                    if _guild.id == int(ban.guildid) and not guild:
                        guild = _guild
                banned_users = await guild.bans()
                for ban_entry in banned_users:
                    user = ban_entry.user
                    if user.id == ban.userid:
                        await guild.unban(user)

                        session.delete(ban)
                        session.commit()
                        session.lush()
                        session.close()
        await asyncio.sleep(5)
        if exit_flag:
            break


def thread_unmute_ban():
    bot.bot.loop.create_task(unmute_ban_async())


guilds = []
th_unmute_ban = Thread(target=thread_unmute_ban)


def start_thread(_guilds):
    global guilds
    guilds = _guilds
    th_unmute_ban.start()


def set_exit_flag():
    global exit_flag
    exit_flag = True
