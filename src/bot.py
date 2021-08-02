import asyncio
import json
import logging
import os.path

import discord
from discord.ext import commands

from modules import modules
from config import config
from modules import minecraft

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=config["prefix"], description=config["description"], intents=intents, help_command=None)

logger = logging.getLogger("main")

guilds = []


class Application:
    """
    This class is the main application of the GalaxyCore bot.
    When started, it blocks the main thread and runs the bot
    """

    __cogs = []

    def __init__(self, discord_bot, bot_token, _logger):
        self.bot = discord_bot
        self.logger = _logger
        self.logger.setLevel(logging.DEBUG if config["debug"] else logging.INFO)

        if not os.path.isfile("config/config.json"):
            with open("config/config.json", "w") as f:
                json.dump({
                    "prefix": "!"
                }, f, indent=4)

        self.load_extensions()

        @self.bot.event
        async def on_ready():
            global guilds
            self.logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator}")
            self.logger.debug("Initializing Update Task")
            bot.loop.create_task(self.update_task())
            self.logger.info("Initialized Update Task")
            self.logger.debug("Initializing Minecraft Server Status Task")
            bot.loop.create_task(self.server_status_task())
            self.logger.info("Initialized Minecraft Server Status Task")
            guilds = bot.guilds

        bot.run(bot_token)

    def load_extensions(self):
        self.logger.debug(f"Loading Extension Modules")
        modules.setup(bot)
        self.logger.info("Loaded Modules Extension")
        for extension in config["extensions"]:
            self.logger.debug(f"Loading Extension {extension}")

            bot.load_extension(f"modules.{extension}")

            self.logger.info(f"Loaded Extension {extension}")
        self.logger.info(f"Loaded {len(self.__cogs)} Extensions in total")

    @staticmethod
    async def update_task():
        while True:
            for state in config["rich-presence"]["states"]:
                bot.command_prefix = config["prefix"]

                # Activity
                activity = discord.Game(state["message"])

                statusstr = state["status"]
                status = discord.Status.online
                if statusstr == "idle":
                    status = discord.Status.idle
                elif statusstr == "dnd" or statusstr == "do_not_disturb":
                    status = discord.Status.do_not_disturb
                elif statusstr == "offline":
                    status = discord.Status.offline

                await bot.change_presence(activity=activity, status=status, afk=state["afk"])
                await asyncio.sleep(state["delay"])

    @staticmethod
    async def server_status_task():
        while True:
            await minecraft.Minecraft(bot).update_server_status()
            await asyncio.sleep(5)


logging.basicConfig(
    level=logging.DEBUG if config["debug"] else logging.INFO,
    format='(%(asctime)s) %(levelname)7s - %(name)20s: %(message)s'
)

token = open("config/token.txt", "r").read()

if __name__ == "__main__":
    Application(bot, token, logger)

# On message automod

# Autoroles

# Reaction Roles
