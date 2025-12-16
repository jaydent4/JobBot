from github import githubScraper
from ycombinator import ycombinatorScraper

SCRAPER_REGISTRY = {
    "github": githubScraper,
    "ycombinator": ycombinatorScraper,
}

