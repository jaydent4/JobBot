import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
from manager.manager import Manager
from logging_config import setup_logging
from config import Config

config = Config()

JOB_POSTING_CHANNEL = config.channel
UPDATE_RATE = config.rate

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename="discord_log", encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

manager = Manager(config.sources)
assert(0)
@bot.event
async def on_ready():
    print(f"{bot.user.name} is working")
    update.start()

"""
Uses the manager to periodically check if the job posting database is updated.
If the database is updated, a response is sent to the discord channel

Args:
    None

Return:
    None
"""
@tasks.loop(hours=UPDATE_RATE)
async def update():
    updateInfo = manager.update()
    if updateInfo[0]:
        new_postings = updateInfo[1]
        channel = bot.get_channel(JOB_POSTING_CHANNEL)
        await channel.send(f"{new_postings}")


"""
Fowards user query to manager and then sends a response to the discord channel

Args:
    --time int type: time scale of interest. 
        ex: --time 5 days
        note: we can add weeks/months
    --loc [insert location name]: location of interest. 
        ex: --loc menlo park 
        note: (we could do states too)
    --comp [insert company name]: company of interst.
        ex: --comp amazon

Returns:
    None
"""
@bot.command()
async def job(ctx, *args): # args is a tuple
    # use args to query
    query_results: list[tuple] = manager.getData(args)
    # sends msg to discord
    await ctx.send(f"{query_results}")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
