import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename="discord_log", encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready")

@bot.command()
async def hello(ctx):
    await ctx.send(f"your gay <@&{1278596559621193728}>")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
