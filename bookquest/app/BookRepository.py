import json
from urllib.request import urlopen


class BookRepository:

    def findBookByIsbn(self, isbn: str):
        api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        isbn.strip()
        infos = {}
        try:
            resp = urlopen(f"{api}{isbn}")
            book_data = json.load(resp)

            if 'items' not in book_data:
                return None

            volume_info = book_data["items"][0]["volumeInfo"]
            title = volume_info.get("title", "N/A")
            subtitle = volume_info.get("subtitle", "N/A")
            authors = volume_info.get("authors", ["N/A"])
            publisher = volume_info.get("publisher", "N/A")
            published_date = volume_info.get("publishedDate", "N/A")
            description = volume_info.get("description", "N/A")
            identifiers = volume_info.get("industryIdentifiers", [])
            page_count = volume_info.get("pageCount", "N/A")
            categories = volume_info.get("categories", ["N/A"])
            average_rating = volume_info.get("averageRating", "N/A")
            ratings_count = volume_info.get("ratingsCount", "N/A")
            language = volume_info.get("language", "N/A")
            image_link = (volume_info.get("imageLinks", {})
                          .get("thumbnail", "N/A"))
            preview_link = volume_info.get("previewLink", "N/A")
            info_link = volume_info.get("infoLink", "N/A")
            print_type = volume_info.get("printType", "N/A")
            maturity_rating = volume_info.get("maturityRating", "N/A")
            access_info = (book_data["items"][0].get("accessInfo", {})
                           .get("accessViewStatus", "N/A"))
            sale_info = (book_data["items"][0].get("saleInfo", {})
                         .get("buyLink", "N/A"))
            content_version = volume_info.get("contentVersion", "N/A")

            isbn_10 = ""
            isbn_13 = ""
            for identifier in identifiers:
                id_value = identifier.get('identifier', 'N/A')
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
                "authors": authors, # list
                "page_count": page_count,
                "categories": categories, # list
                "average_rating": average_rating,
                "ratings_count": ratings_count,
                "isbn_10": isbn_10,
                "isbn_13": isbn_13,
                "image_link": image_link,
                "language": language
            }

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        return infos
