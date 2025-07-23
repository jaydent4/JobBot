import discord 
from const import Columns
from datetime import datetime

def bad_embed(msg) -> discord.Embed:
    description = f"{msg}... just put the fries in the bag..."
    fries = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnRoeTFkN3ZrMGNoOXprczI1cWM5NWE2bGRocjU0bGs4cDkwMG1zeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ReqpJ6fApNvOw/giphy.gif"
    embed = discord.Embed(description=description, color=discord.Color.blue())
    embed.set_image(url=fries)
    return embed

def parse_locs(cities, states) -> list[str]:
    out = []
    for c, s in zip(cities, states):
        out.append(c + ", " + s)
    return out

def embed(query:tuple) -> discord.Embed:
    id = replace_none(query[Columns.ID.value])
    company_name = replace_none(query[Columns.COMPANY_NAME.value])
    role = replace_none(query[Columns.ROLE.value])
    cities = replace_none(query[Columns.CITY.value])
    states = replace_none(query[Columns.STATE.value])
    link = replace_none(query[Columns.APPLICATION_LINK.value])
    date_posted = date_prettify(query[Columns.DATE_POSTED.value])
    date_scraped = replace_none(query[Columns.DATE_SCRAPED.value])
    level = replace_none(query[Columns.LEVEL.value])

    title = f'**{company_name}** - {role}'
    link = link if link.startswith("http") else None
    embed = discord.Embed(title=title, url=link, color=discord.Color.from_str("#7785cc"))
    embed.add_field(name="Location", value=parse_locs(cities, states), inline=True)
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Date Posted", value=date_posted, inline=True)
    embed.add_field(name="Date Scraped", value=date_scraped, inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)

    issues_url = "https://github.com/jaydent4/JobBot/issues"
    embed.add_field(
        name="Suggestions and Issues",
        value=f"For any suggestions and issues, see our [issues page]({issues_url})",
        inline=False
    )
    return embed

def replace_none(value):
    if value == "NONE":
        return "N/A"
    return value

def date_prettify(s):
    if s != "NONE":
        return datetime.strptime(s, "%Y-%m-%d").strftime("%d %B %Y")
    return "NONE"