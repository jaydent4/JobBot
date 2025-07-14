import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
from manager.manager import Manager
from logging_config import setup_logging
from config import Config
from embed import embed

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
        ex: !job --time 5
        note: we can add weeks/months
        avaiable options: int interpreted as days from today
    --location [insert location name]: location of interest. 
        ex: !job --location menlo park 
        note: (we could do states too)
    --company [insert company name]: company of interst.
        ex: !job --company amazon
    --count [insert number]
        ex: !job --count 2
        available options: any int
    --level [insert level]
        ex: !job --level intern
        available options: intern
Returns:
    None
"""
@bot.command()
async def job(ctx, *args): # args is a tuple
    query_results = manager.get_data(args)
    for row in query_results:
        print(row) #debug print
        await ctx.send(embed=embed(row))


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
