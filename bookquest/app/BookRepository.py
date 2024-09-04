import json
import requests
from urllib.request import urlopen


class BookRepository:

    def __init__(self):
        self.base_url = 'https://www.googleapis.com/books/v1/volumes'

    def _extract_infos(self, volume: list):
        empty_value = ""

        title = volume.get("title", empty_value)
        subtitle = volume.get("subtitle", empty_value)
        authors = volume.get("authors", [])
        publisher = volume.get("publisher", empty_value)
        published_date = volume.get("publishedDate", empty_value)
        description = volume.get("description", empty_value)
        identifiers = volume.get("industryIdentifiers", [])
        page_count = volume.get("pageCount", empty_value)
        categories = volume.get("categories", [])
        average_rating = volume.get("averageRating", empty_value)
        ratings_count = volume.get("ratingsCount", empty_value)
        language = volume.get("language", empty_value)
        image_link = (
            volume.get("imageLinks", {}).get("thumbnail", empty_value))

        isbn_10 = ""
        isbn_13 = ""
        for identifier in identifiers:
            id_value = identifier.get('identifier', empty_value)
            if len(id_value) == 10:
                isbn_10 = id_value
            elif len(id_value) == 13:
                isbn_13 = id_value

        infos = {
            "title": title,
            "subtitle": subtitle,
            "publisher": publisher,
            "published_date": published_date,
            "description": description,
            "authors": authors,  # list
            "page_count": page_count,
            "categories": categories,  # list
            "average_rating": average_rating,
            "ratings_count": ratings_count,
            "isbn_10": isbn_10,
            "isbn_13": isbn_13,
            "image_link": image_link,
            "language": language
        }
        return infos

    def _can_add_book(self, lang: str, volume_info: dict):
        # Check if the lang is matching
        if lang is not None and volume_info.get('language') != lang:
            return False

        # Can add only if at least one of the isbn exist
        return volume_info.get('isbn_10') or volume_info.get('isbn_13')

    def findBookByIsbn(self, isbn: str):
        api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        isbn.strip()
        try:
            resp = urlopen(f"{api}{isbn}")
            book_data = json.load(resp)

            if 'items' not in book_data:
                return None

            volume_info = book_data["items"][0]["volumeInfo"]
            infos = self._extract_infos(volume_info)

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        return infos

    def find_books_by_keyword_and_lang(self, keyword: str,
                                       lang: str = None, limit: int = 40):
        keyword.strip()

        total_books_fetched = 0
        books_info = []

        while total_books_fetched < limit:
            # Calculate remaining books to fetch
            # based on the number of valid books fetched
            remaining_books = limit - len(books_info)

            # Set the max results for this request
            max_results = min(40, remaining_books)

            params = {
                'q': keyword,
                'langRestrict': lang,
                'maxResults': max_results,
                'startIndex': total_books_fetched
            }

            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()  # Vérifier les erreurs
                books_data = response.json()

                if "items" not in books_data:
                    break

                for book in books_data["items"]:
                    volume_info = self._extract_infos(
                        book["volumeInfo"])

                    # Add only books with an ISBN and a valid lang
                    #   Unfortunately, Google Books API seems to have
                    #   problems with the 'langRestrict' param ...
                    if self._can_add_book(lang, volume_info):
                        books_info.append(volume_info)

                        if len(books_info) == limit:
                            break

                # Update counters
                total_books_fetched += len(books_data["items"])

                # Break loop if fewer books were returned than
                # requested, meaning no more books are available
                if len(books_data["items"]) < max_results:
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        return books_info

    def find_books_by_author(self, author: str, lang: str = None):
        total_books_fetched = 0
        books_info = []
        limit = 20

        while total_books_fetched < limit:
            # Calculate remaining books to fetch,
            # based on the number of valid books fetched
            remaining_books = limit - len(books_info)

            # Set the max results for this request
            max_results = min(40, remaining_books)

            params = {
                'q': f"inauthor:{author}",
                'langRestrict': lang,
                'maxResults': 40,
            }

            try:

                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                books_data = response.json()

                if "items" not in books_data:
                    break

                for book in books_data["items"]:
                    volume_info = self._extract_infos(
                        book["volumeInfo"])

                    # Add only books with matching lang and an ISBN
                    #   Unfortunately, Google Books API seems to have
                    #   problems with the 'langRestrict' param ...
                    if self._can_add_book(lang, volume_info):
                        books_info.append(volume_info)

                        if len(books_info) == limit:
                            break

                # Update counters
                total_books_fetched += len(books_data["items"])

                # Break loop if fewer books were returned than
                # requested, meaning no more books are available
                if len(books_data["items"]) < max_results:
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        return books_info
