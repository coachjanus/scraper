# flask_payroll/payroll/scraper/locators/book_locators.py
class BookLocators:
    """
    Locators for an item in the HTML page.

    This allows us to easily see what our code will be looking at
    as well as change it quickly if we notice it is now different.
    
    Локатори для елемента на сторінці HTML.

    Це дозволяє нам легко бачити, на що буде дивитися наш код
    а також швидко змінити його, якщо ми помітимо, що тепер він інший.
    """
    NAME_LOCATOR = 'article.product_pod h3 a'
    LINK_LOCATOR = 'article.product_pod h3 a'
    PRICE_LOCATOR = 'article.product_pod p.price_color'
    RATING_LOCATOR = 'article.product_pod p.star-rating'
