import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
from manager.manager import Manager
from config import Config
from embed import embed, bad_embed

config = Config()

JOB_POSTING_CHANNEL = config.channel
UPDATE_RATE = config.rate
JOB_COUNTER = config.job_counter
GROUP_ID_COUNTER = config.grp_id

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
print(token)

handler = logging.FileHandler(filename="discord_log", encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

manager = Manager(config.sources, JOB_COUNTER, GROUP_ID_COUNTER)

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
    channel = bot.get_channel(JOB_POSTING_CHANNEL)
    await channel.send("Automatic dB Update began")
    updateInfo = manager.update()
    if updateInfo[0]:
        new_postings = updateInfo[1]

        for new_job in new_postings:
            await channel.send(embed=embed(new_job))
    else:
        await channel.send("No new j*bs posted. Stay unemployed gang L bozo")


"""
Fowards user query to manager and then sends a response to the discord channel

Args:
    --time [insert number of days]
        ex: !job --time 5
        note: we can add weeks/months
        available options: int interpreted as days from today

    --role [insert role's name]
        ex: !job --role ML

    --location [insert location name] 
        ex: !job --location menlo park 
        note: (we could do states too)

    --company [insert company name]
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
    if "--help" in args:
        if len(args) == 1:
            await ctx.send("[jayden insert something helpful here]")
            return None
        else:
            await ctx.send(embed=bad_embed("y u putting other args with help"))
            return None
    
    query_results = manager.get_data(args)
    if not query_results:
        await ctx.send(embed=bad_embed("invalid args"))
    results = False
    for row in query_results:
        results = True
        print(row) #debug print
        await ctx.send(embed=embed(row))
    if not results:
        await ctx.send(embed=bad_embed("no query results"))


bot.run(str(token), log_handler=handler, log_level=logging.DEBUG)
