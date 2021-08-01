import discord
from discord.ext import commands

import bot


class Modules(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.command(aliases=["load-module", "load_extension", "load-extension"])
    async def load_module(self, ctx, module):
        bot.bot.load_extension(module)
        embed = discord.Embed(title="Modul Aktiviert", description=f"Das Modul {module} wurde aktiviert!",
                              color=discord.Color(0x0fff0f))
        await ctx.channel.send(embed=embed)

    @load_module.error
    async def load_module_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Falsche Benutzung", description="Bitte benutze " + bot.config["prefix"] + "load-module <Modul>",
                                  color=discord.Color(0xff0000))

            await ctx.send(embed=embed, delete_after=5)

    @commands.command(aliases=["unload-module", "unload_extension", "unload-extension"])
    async def unload_module(self, ctx, module):
        bot.bot.unload_extension(module)
        embed = discord.Embed(title="Modul Deaktiviert", description=f"Das Modul {module} wurde deaktiviert!",
                              color=discord.Color(0x0fff0f))
        await ctx.channel.send(embed=embed)

    @unload_module.error
    async def unload_module_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Falsche Benutzung", description="Bitte benutze " + bot.config["prefix"] + "unload-module <Modul>",
                                  color=discord.Color(0xff0000))

            await ctx.send(embed=embed, delete_after=5)

    @commands.command(aliases=["reload-module", "reload_extension", "reload-extension"])
    async def reload_module(self, ctx, module):
        bot.bot.reload_module(module)
        embed = discord.Embed(title="Modul Neu Geladen", description=f"Das Modul {module} wurde neu geladen!",
                              color=discord.Color(0x0fff0f))
        await ctx.channel.send(embed=embed)

    @reload_module.error
    async def reload_module_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Falsche Benutzung", description="Bitte benutze " + bot.config["prefix"] + "reload-module <Modul>",
                                  color=discord.Color(0xff0000))

            await ctx.send(embed=embed, delete_after=5)

    @commands.command(aliases=["reload-modules, reload_extensions", "reload-extensions"])
    async def reload_modules(self, ctx):
        extensions = list(self.bot.extensions.keys())
        for extension in extensions:
            await self.reload_module(ctx, extension)

    @commands.command(aliases=["list-modules", "list_extensions", "list-extensions"])
    async def list_modules(self, ctx):
        extensions = list(self.bot.extensions.keyS())
        message = ""
        for extension in extensions:
            message += f"{extension}\n"
        await ctx.channel.send(message)


def setup(_bot):
    _bot.add_cog(Modules(_bot))
