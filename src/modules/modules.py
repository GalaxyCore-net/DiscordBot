import discord
from discord.ext import commands
from discord.ext.commands import ExtensionNotLoaded, has_permissions

import bot
from bot import logger


class Modules(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @has_permissions(administrator=True)
    @commands.command(aliases=["load-module", "load_extension", "load-extension"])
    async def load_module(self, ctx, module):
        logger.debug(f"Loading Module {module}")
        bot.bot.load_extension(module)
        embed = discord.Embed(title="Modul Aktiviert", description=f"Das Modul {module} wurde aktiviert!",
                              color=discord.Color(0x0fff0f))
        await ctx.channel.send(embed=embed)

    @load_module.error
    async def load_module_error(self, ctx, error):
        logger.debug(f"An error occured while loading a module: \n {error}")
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Falsche Benutzung", description="Bitte benutze " + bot.config["prefix"] + "load-module <Modul>",
                                  color=discord.Color(0xff0000))

            await ctx.send(embed=embed, delete_after=5)

    @has_permissions(administrator=True)
    @commands.command(aliases=["unload-module", "unload_extension", "unload-extension"])
    async def unload_module(self, ctx, module):
        logger.debug(f"Unloading Module {module}")
        bot.bot.unload_extension(module)
        embed = discord.Embed(title="Modul Deaktiviert", description=f"Das Modul {module} wurde deaktiviert!",
                              color=discord.Color(0x0fff0f))
        await ctx.channel.send(embed=embed)

    @unload_module.error
    async def unload_module_error(self, ctx, error):
        logger.debug(f"An error occured while unloading a module: \n {error}")
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Falsche Benutzung", description="Bitte benutze " + bot.config["prefix"] + "unload-module <Modul>",
                                  color=discord.Color(0xff0000))

            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(error, ExtensionNotLoaded):
            embed = discord.Embed(title="Die Erweiterung ist nicht geladen")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=error)
            await ctx.send(embed=embed)

    @has_permissions(administrator=True)
    @commands.command(aliases=["reload-module", "reload_extension", "reload-extension"])
    async def reload_module(self, ctx, module):
        logger.debug(f"Reloading Module {module}")
        bot.bot.reload_module(module)
        embed = discord.Embed(title="Modul Neu Geladen", description=f"Das Modul {module} wurde neu geladen!",
                              color=discord.Color(0x0fff0f))
        await ctx.channel.send(embed=embed)

    @reload_module.error
    async def reload_module_error(self, ctx, error):
        logger.debug(f"An error occured while reloading a module: \n {error}")
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Falsche Benutzung", description="Bitte benutze " + bot.config["prefix"] + "reload-module <Modul>",
                                  color=discord.Color(0xff0000))

            await ctx.send(embed=embed, delete_after=5)

    @has_permissions(administrator=True)
    @commands.command(aliases=["reload-modules, reload_extensions", "reload-extensions"])
    async def reload_modules(self, ctx):
        extensions = list(self.bot.extensions.keys())
        for extension in extensions:
            await self.reload_module(ctx, extension)

    @has_permissions(administrator=True)
    @commands.command(aliases=["list-modules", "list_extensions", "list-extensions"])
    async def list_modules(self, ctx):
        logger.debug("Listing Modules")
        extensions = list(self.bot.extensions.keys())
        logger.debug(extensions)
        message = ""
        for extension in extensions:
            message += f"{extension}\n"
        await ctx.channel.send(message)


def setup(_bot):
    _bot.add_cog(Modules(_bot))
