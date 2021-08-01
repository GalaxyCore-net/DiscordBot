import discord
import mcrcon
from discord.ext import commands
from bot import config


class Minecraft(commands.Cog):
    invalid_characters = [
        "§0",
        "§1",
        "§2",
        "§3",
        "§4",
        "§5",
        "§6",
        "§7",
        "§8",
        "§9",
        "§a",
        "§b",
        "§c",
        "§d",
        "§e",
        "§f",
    ]

    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_message(self, message):
        _config = config["minecraft"]
        if not message.channel.id == _config["console-channel"]:
            return
        if message.author.bot:
            return
        if message.content.startswith(_config["prefix"]):
            command = message.content[len(_config["prefix"]):]
            try:
                with mcrcon.MCRcon(host=_config["server-host"], password=_config["server-password"], port=_config["server-port"]) as server:
                    server.connect()
                    feedback = server.command(command)
                    for char in self.invalid_characters:
                        feedback = feedback.replace(char, "")
                    if feedback == "" or feedback is None:
                        feedback = "Command ausgeführt"
                    await message.channel.send(f"```{feedback}```")
            except ConnectionRefusedError:
                await message.channel.send(f"Verbindung zum Server {_config['server-host']}:{_config['server-port']} fehlgeschlagen")

    async def update_server_status(self):
        channel: discord.TextChannel = self.bot.get_channel(config["server-status-channel"])
        try:
            with mcrcon.MCRcon(host=config["minecraft"]["server-host"], password=config["minecraft"]["server-password"], port=config["minecraft"]["server-port"]) as server:
                server.connect()
                await channel.edit(name="» Server-Status: Online")
        except ConnectionRefusedError:
            await channel.edit(name="» Server-Status: Offline")


def setup(_bot):
    _bot.add_cog(Minecraft(_bot))
