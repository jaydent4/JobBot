import discord 
from const import Columns

def embed(query:tuple) -> discord.Embed:
    id = replace_none(query[Columns.ID.value])
    company_name = replace_none(query[Columns.COMPANY_NAME.value])
    role = replace_none(query[Columns.ROLE.value])
    location = replace_none(query[Columns.LOCATION.value])
    link = replace_none(query[Columns.APPLICATION_LINK.value])
    date_posted = replace_none(query[Columns.DATE_POSTED.value])
    date_scraped = replace_none(query[Columns.DATE_SCRAPED.value])
    level = replace_none(query[Columns.LEVEL.value])

    embed = discord.Embed(title=f'**{company_name}**: {role} ({id})', url=link, color=discord.Color.blue())
    embed.add_field(name="Location", value=location, inline=True)
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="Date Posted", value=date_posted, inline=False)
    embed.add_field(name="Date Scraped", value=date_scraped, inline=True)

    embed.set_footer(text="For issues and suggestions, visit: https://github.com/jaydent4/JobBot/issues")
    return embed

def replace_none(value):
    if value == "NONE":
        return "N/A"
    return value