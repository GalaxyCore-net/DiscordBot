import discord
from discord.ext import commands

from bot import logger

from sqlalchemy.orm import sessionmaker

from database import engine
from database.models import BadWordsModel


class Automod(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if await self.process_message(message):
            await message.delete()

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if await self.process_message(after):
            await after.edit(content=before.content, embed=before.embed)

    @staticmethod
    async def process_message(message: discord.Message):
        session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
        session.begin()
        words = session.query(BadWordsModel).all()
        for bad_word in words:
            if bad_word.word in message.content.lower():
                logger.info(f"{message.author.name} wrote the forbidden word '{bad_word}'")
                await message.author.send(content="Du hast ein schlimmes Wort geschrieben!\n"
                                                  "Genauer Wortlaut: \n"
                                                  f"{message.content}\n"
                                                  "Bitte unterlasse das!")
                return True
        return False


def setup(_bot):
    _bot.add_cog(Automod(_bot))
