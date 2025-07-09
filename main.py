import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import random

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
    andrew_gae.start()

# bot does smt when u ping it with !hello (this is for us when we want to do feature 1)
@bot.command()
async def hello(ctx):
    await ctx.send(f"your gay <@&{572240275867566080}>")

# bot periodically sends a message
# periodically checks if sqlite db has been update, if it has been updated, then send a message
@tasks.loop(hours=random.randint(1,12))
async def andrew_gae():
    # if db updates...
    print("hi")
    channel = bot.get_channel(1392010751023120394)
    await channel.send(f"<@&{572240275867566080}> is gae")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
