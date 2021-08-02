from discord.ext import commands
from bot import config, bot
import discord


# noinspection DuplicatedCode
class Team(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.command()
    async def team(self, ctx: commands.Context, *args):
        if ctx.channel.id != config["leitung-commands"]:
            return

        ok_embed = discord.Embed()
        ok_embed.title = "Teamupdate"
        ok_embed.description = "Die Nachricht wurde gesendet."
        ok_embed.colour = discord.Color(0x00ff00)

        if len(args) == 2:
            teamnotify = ctx.guild.get_channel(config["up-down-ranks"])

            if args[0] == "quit":
                embed = discord.Embed()
                embed.title = f"Teamupdate - {args[1]}"
                embed.description = f"Neuigkeit von **{ctx.author.mention}**\n" \
                                    f"Das Teammitglied **{args[1]}** hat das Team freiwillig verlassen."
                embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.colour = discord.Color(0xff0000)

                await teamnotify.send(content="", embed=embed)
                await ctx.send(embed=ok_embed)
            elif args[0] == "kick":
                embed = discord.Embed()
                embed.title = f"Teamupdate - {args[1]}"
                embed.description = f"Neuigkeit von **{ctx.author.mention}**\n" \
                                    f"Das Teammitglied **{args[1]}** fliegt aus dem Team."
                embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.colour = discord.Color(0xff0000)

                await teamnotify.send(content="", embed=embed)
                await ctx.send(embed=ok_embed)
            else:
                embed = discord.Embed()
                embed.title = f"{config['prefix']}team"
                embed.description = f"Verwende {config['prefix']}team <quit|kick> <name>"
                embed.colour = discord.Color(0xff0000)

                await ctx.send(embed=embed)
        elif len(args) == 3:
            teamnotify = ctx.guild.get_channel(config["up-down-ranks"])

            if args[0] == "new":
                embed = discord.Embed()
                embed.title = f"Teamupdate - {args[1]}"
                embed.description = f"Neuigkeit von **{ctx.author.mention}**\n" \
                                    f"Das Teammitglied **{args[1]}** kommt als **{args[2]}** ins Team."
                embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.colour = discord.Color(0x00ff00)

                await teamnotify.send(embed=embed)
                await ctx.send(embed=ok_embed)
            elif args[0] == "promote":
                embed = discord.Embed()
                embed.title = f"Teamupdate - {args[1]}"
                embed.description = f"Neuigkeit von **{ctx.author.mention}**\n" \
                                    f"Das Teammitglied **{args[1]}** wurde zum **{args[2]}** geupranked."
                embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.colour = discord.Color(0x00ff00)

                await teamnotify.send(embed=embed)
                await ctx.send(embed=ok_embed)
            elif args[0] == "demote":
                embed = discord.Embed()
                embed.title = f"Teamupdate - {args[1]}"
                embed.description = f"Neuigkeit von **{ctx.author.mention}**\n" \
                                    f"Das Teammitglied **{args[1]}** wurde zum **{args[2]}** gedownranked."
                embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.colour = discord.Color(0xff0000)

                await teamnotify.send(embed=embed)
                await ctx.send(embed=ok_embed)
            else:
                embed = discord.Embed()
                embed.title = f"{config['prefix']}team"
                embed.description = f"Verwende {config['prefix']}team <new|promote|demote> <name> <rang>"
                embed.colour = discord.Color(0xff0000)

                await ctx.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = f"{config['prefix']}team"
            embed.description = f"Verwende {config['prefix']}team <new|promote|demote|quit|kick> <name> [rang]"
            embed.colour = discord.Color(0xff0000)

            await ctx.send(embed=embed)


def setup(_bot):
    _bot.add_cog(Team(_bot))
