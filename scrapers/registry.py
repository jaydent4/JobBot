from scrapers.github import githubScraper
from scrapers.ycombinator import ycombinatorScraper

SCRAPER_REGISTRY = {
    "github": githubScraper,
    "ycombinator": ycombinatorScraper,
}

