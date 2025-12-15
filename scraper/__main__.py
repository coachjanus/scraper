""" Entry point for the web scraper application.
    This code demonstrates how to perform an asynchronous HTTP GET request using the aiohttp library in Python.

    Imports: The code imports aiohttp for making HTTP requests and asyncio for handling asynchronous operations.

    fetch(url) Function: This is an asynchronous function that takes a URL as an argument. It creates an aiohttp.ClientSession to manage the HTTP session. Inside the session, it performs a GET request to the specified URL and returns the response text.

    main() Function: This is another asynchronous function that calls fetch with the URL "https://example.com". It awaits the result and then prints the length of the fetched HTML content.

    asyncio.run(main()): This line runs the main() coroutine, which in turn calls fetch to retrieve and print the number of characters in the HTML content from the specified URL.
"""


# import aiohttp
# import asyncio

# URL = 'http://books.toscrape.com'

# async def fetch(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()

# async def main():
#     html = await fetch(URL)
#     print(f"Fetched {len(html)} characters")


# if __name__ == '__main__':
#     asyncio.run(main())
    
    
from scraper.catalog import Catalog

def main():
    book_app = Catalog()
    items = book_app.books()
    for item in items:
        print(item)
    print("\n\nBest 5 Books:\n")
    best_books = book_app.best_books()
    for book in best_books: 
        print(book)
    print("\n\nCheapest 5 Books:\n")
    cheapest_books = book_app.cheapest_books()
    for book in cheapest_books: 
        print(book)
    
if __name__ == '__main__':
    main()