import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from sqlalchemy.orm import sessionmaker

from bot import logger
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
        if message.author.bot:
            return
        session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
        session.begin()
        words = session.query(BadWordsModel).all()
        for bad_word in words:
            if bad_word.word in message.content.lower():
                logger.info(f"{message.author.name} wrote the forbidden word '{bad_word.word}'")
                await message.author.send(content="Du hast ein schlimmes Wort geschrieben!\n"
                                                  "Genauer Wortlaut: \n"
                                                  f"{message.content}\n"
                                                  "Bitte unterlasse das!")
                return True
        return False

    @has_permissions(administrator=True)
    @commands.command(aliases=["add-insult"])
    async def add_insult(self, ctx, *, insult):
        session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()
        session.begin()
        new_word = BadWordsModel(word=insult)
        session.add(new_word)
        session.commit()
        session.flush()
        session.close()

        embed = discord.Embed()
        embed.title = "Wort hinzugefügt!"
        embed.description = f"Das Word {insult} wurde erfolgreich hinzugefügt!"
        embed.colour = discord.Color(0x00ff00)

        ctx.send(embed=embed)


def setup(_bot):
    _bot.add_cog(Automod(_bot))
