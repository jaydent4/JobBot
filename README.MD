# JobBot
A Discord bot to help chronic Discord users find software engineering internships and opportunities. This bot pulls job postings from multiple sources periodically and sends messsages when new postings are found. Previous job postings can also be queried.

## Features:
### Automatic Job Postings
Configurable scrapers are periodically ran and sends messages of new postings.

### Scraper Scalability
The bot can easily add new scraper modules for new sites. New scrapers must follow the base class defined in `scrapers/base.py`.

### Queries
You can query the previously-scraped job postings from the bot with the following command:

Command Usage:
```
!job [OPTIONS]
```

Options:
```
--time <days>        Filter jobs scraped within the last <days> days
--company <name>     Filter by company name
--role <keyword>     Filter by role/title
--city <city>        Filter by city
--state <state>      Filter by state
--level <level>      Filter by experience level
--source <source>    Filter by scrape source
--count <number>     Limit the number of results returned
```

## Setup

### Requirements
- Python **3.13+**
- A Discord bot token
- `pip` (Python package manager)

---

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/jaydent4/JobBot.git
cd JobBot
pip install -r requirements.txt
```

### Discord Bot Setup
1. Create a Discord application at the
https://discord.com/developers/applications
2. Add a Bot to the application and copy the discord bot token.
3. Invite the bot to your server with the appropriate permissions
(at minimum: Read Messages and Send Messages).
4. Create a `.env` file in the main project directory with the line `DISCORD_TOKEN=your_bot_token_here`

### Running
Run the following command:
```
python main.py
```

## Limitations
- Scrapers depend on third-party site HTML and may break if layouts change
- Job deduplication is best-effort
- Rate limits are enforced by source sites