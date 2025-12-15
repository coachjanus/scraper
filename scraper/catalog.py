# scraper_project/scraper/catalog.py
import requests
from typing import List, Iterator, Optional, Any

from .pages import Pages

URL = "http://books.toscrape.com"


class Catalog:
    """
    Catalog loads all book pages from books.toscrape.com and exposes:
     - self._books: list of parsed book objects
     - next_book(): iterator over books (returns default when exhausted)
     - best_books() / cheapest_books() helpers
    """

    def __init__(self, base_url: str = URL, timeout: float = 10.0) -> None:
        self.base_url = base_url
        self.timeout = timeout

        resp = requests.get(self.base_url, timeout=self.timeout)
        resp.raise_for_status()
        self.page_content = resp.content
        self.page = Pages(self.page_content)

        # load books using the already downloaded first page
        self._books: List[Any] = self._load_books()
        self.books_generator: Iterator[Any] = iter(self._books)

    def _load_books(self) -> List[Any]:
        books: List[Any] = []
        # use the already downloaded first page
        books.extend(self.page.books)

        # fetch remaining pages (2..page_count), if any
        page_count = self.page.page_count
        for page_num in range(2, page_count + 1):
            url = f"{self.base_url}/catalogue/page-{page_num}.html"
            try:
                resp = requests.get(url, timeout=self.timeout)
                resp.raise_for_status()
            except requests.RequestException:
                # skip pages we can't fetch; alternatively: log or raise
                continue

            page = Pages(resp.content)
            books.extend(page.books)

        return books

    def next_book(self, default: Optional[Any] = None) -> Optional[Any]:
        """
        Return the next book from the internal iterator, or `default` if exhausted.
        """
        return next(self.books_generator, default)

    def best_books(self, count: int = 5) -> List[Any]:
        """
        Return top `count` books by rating (highest first).
        """
        return sorted(self._books, key=lambda x: x.rating, reverse=True)[:count]

    def cheapest_books(self, count: int = 5) -> List[Any]:
        """
        Return top `count` books by price (lowest first).
        """
        return sorted(self._books, key=lambda x: x.price)[:count]
