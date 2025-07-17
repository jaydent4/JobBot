import discord 
from const import Columns

def bad_embed(msg) -> discord.Embed:
    description = f"{msg}... just put the fries in the bag..."
    fries = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnRoeTFkN3ZrMGNoOXprczI1cWM5NWE2bGRocjU0bGs4cDkwMG1zeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ReqpJ6fApNvOw/giphy.gif"
    embed = discord.Embed(description=description, color=discord.Color.blue())
    embed.set_image(url=fries)
    return embed

def embed(query:tuple) -> discord.Embed:
    id = replace_none(query[Columns.ID.value])
    company_name = replace_none(query[Columns.COMPANY_NAME.value])
    role = replace_none(query[Columns.ROLE.value])
    location = replace_none(query[Columns.LOCATION.value])
    link = replace_none(query[Columns.APPLICATION_LINK.value])
    date_posted = replace_none(query[Columns.DATE_POSTED.value])
    date_scraped = replace_none(query[Columns.DATE_SCRAPED.value])
    level = replace_none(query[Columns.LEVEL.value])

    title = f'**{company_name}**: {role} ({id})'
    link = link if link.startswith("http") else None
    embed = discord.Embed(title=title, url=link, color=discord.Color.blue())
    embed.add_field(name="Location", value=location, inline=True)
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="Date Posted", value=date_posted, inline=False)
    embed.add_field(name="Date Scraped", value=date_scraped, inline=True)

    issues_url = "https://github.com/jaydent4/JobBot/issues"
    embed.set_footer(text=f'For issues and suggestions, visit: {issues_url}')
    return embed

def replace_none(value):
    if value == "NONE":
        return "N/A"
    return value