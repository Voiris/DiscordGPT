from dotenv import load_dotenv
import os
from discord import Bot
from discord.commands.context import ApplicationContext
import discord

from .gpt import ChatGPT

load_dotenv(".env")

token = os.environ["DISCORD_TOKEN"]
api_key = os.environ["OPENAI_API_KEY"]

intents = discord.Intents.all()
# noinspection PyDunderSlots,PyUnresolvedReferences
intents.message_content = True
bot = Bot(intents=intents)
gpt = ChatGPT(api_key=api_key)


@bot.slash_command()
async def start(ctx: ApplicationContext):
    await ctx.respond(gpt.start_session(ctx.channel.id, ctx.user.id))


@bot.slash_command()
async def stop(ctx: ApplicationContext):
    await ctx.respond(gpt.stop_session(ctx.channel.id, ctx.user.id))


@bot.event
async def on_message(ctx: discord.Message):
    if ctx.author.id != bot.user.id:
        if gpt.has_session(ctx.channel.id, ctx.author.id):
            answer = await ctx.reply("Думаю...")
            await answer.edit(content=gpt.handle(ctx.channel.id, ctx.author.id, ctx.content))


bot.run(token=token)
