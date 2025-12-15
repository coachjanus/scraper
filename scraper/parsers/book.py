# scraper_project/scraper/parsers/book.py
import re
import logging
import html
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

from scraper.locators.book_locators import BookLocators

logger = logging.getLogger(__name__)

class BookParser:
    """
    A class to take in an HTML page or content, and find properties of an item
    in it.
    """

    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent: Any) -> None:
        self.parent = parent

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'price': self.price,
            'rating': self.rating,
        }


    def __repr__(self) -> str:
        return str(self.to_dict())
        # return f'<Book {self.name} {self.price}, {self.rating} stars>'
        

    @property
    def name(self) -> str:
        """метод select_one() знаходить лише перший тег, який відповідає селектору"""
        locator = BookLocators.NAME_LOCATOR
        el = self.parent.select_one(locator)
        if not el:
            logger.warning("Name element not found using locator: %s", locator)
            return ""
        # Ви можете отримати доступ до атрибутів тегу, розглядаючи тег як слов��ик:
        title = el.attrs.get('title') if hasattr(el, 'attrs') else None
        if title:
            return html.unescape(title).strip()
        text = el.get_text(strip=True) if hasattr(el, 'get_text') else ""
        return html.unescape(text)

    @property
    def link(self) -> str:
        locator = BookLocators.LINK_LOCATOR
        el = self.parent.select_one(locator)
        if not el:
            logger.warning("Link element not found using locator: %s", locator)
            return ""
        href = el.attrs.get('href', '') if hasattr(el, 'attrs') else ''
        return href.strip()

    @property
    def price(self) -> Optional[Decimal]:
        locator = BookLocators.PRICE_LOCATOR
        el = self.parent.select_one(locator)
        if not el:
            logger.warning("Price element not found using locator: %s", locator)
            return None
        raw = (el.get_text(strip=True) if hasattr(el, 'get_text') else (el.string or '')).strip()
        raw = raw.replace('\xa0', ' ')
        numeric = re.sub(r'[^\d\.,]', '', raw)
        if not numeric:
            logger.warning("Could not parse numeric value from price string: %r", raw)
            return None
        normalized = numeric.replace(',', '')
        try:
            return Decimal(normalized)
        except (InvalidOperation, ValueError) as exc:
            logger.error("Failed to convert price to Decimal from %r: %s", normalized, exc)
            return None

    @property
    def rating(self) -> Optional[int]:
        locator = BookLocators.RATING_LOCATOR
        star_rating_element = self.parent.select_one(locator)
        if not star_rating_element or not hasattr(star_rating_element, 'attrs'):
            logger.info("Rating element not found using locator: %s", locator)
            return None
        classes = star_rating_element.attrs.get('class', [])
        for cls in classes:
            if cls == 'star-rating':
                continue
            mapped = BookParser.RATINGS.get(cls)
            if mapped is not None:
                return mapped
        logger.info("No known rating class found in %r", classes)
        return None
