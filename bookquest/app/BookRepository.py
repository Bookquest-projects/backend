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
        authors = volume.get("authors", [empty_value])
        publisher = volume.get("publisher", empty_value)
        published_date = volume.get("publishedDate", empty_value)
        description = volume.get("description", empty_value)
        identifiers = volume.get("industryIdentifiers", [])
        page_count = volume.get("pageCount", empty_value)
        categories = volume.get("categories", [empty_value])
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
                                       lang: str = 'en', limit: int = 40):
        keyword.strip()

        total_books_fetched = 0
        books_info = []

        while total_books_fetched < limit:
            # Calculate remaining books to fetch
            remaining_books = limit - total_books_fetched

            # Set the max results for this request
            max_results = min(40, remaining_books)

            params = {
                'q': keyword,
                'langRestrict': lang,
                'maxResults': max_results,
                'startIndex': total_books_fetched
            }

            print(params)

            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()  # Vérifier les erreurs
                books_data = response.json()

                if "items" in books_data:
                    for book in books_data["items"]:
                        volume_info = self._extract_infos(
                            book["volumeInfo"])
                        books_info.append(volume_info)

                    # Update counters
                    total_books_fetched += len(books_data["items"])

                    # Break loop if fewer books were returned than
                    # requested, meaning no more books are available
                    if len(books_data["items"]) < max_results:
                        break
                else:
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        return books_info

    def find_books_by_author(self, author: str, lang: str = None):
        books_info = []

        try:
            params = {
                'q': f"inauthor:{author}",
                'langRestrict': lang,
                'maxResults': 20,
            }

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            books_data = response.json()

            if "items" in books_data:
                for book in books_data["items"]:
                    volume_info = self._extract_infos(
                        book["volumeInfo"])
                    books_info.append(volume_info)

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        return books_info
