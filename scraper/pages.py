# scraper_project/scraper/pages.py
import re

from bs4 import BeautifulSoup
from .locators.page_locators import PageLocators
from .parsers.book import BookParser

class Pages:
    def __init__(self, page) -> None:
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def books(self) -> list[BookParser]:
        return [BookParser(e) for e in self.soup.select(PageLocators.BOOKS)]

    @property
    def page_count(self) -> int:
        content = self.soup.select_one(PageLocators.PAGER).string
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher: re.Match[str] | None = re.search(pattern, content)
        pages = int(matcher.group(1))
        return pages

