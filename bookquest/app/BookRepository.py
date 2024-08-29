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

            empty_value = ""

            volume_info = book_data["items"][0]["volumeInfo"]
            title = volume_info.get("title", empty_value)
            subtitle = volume_info.get("subtitle", empty_value)
            authors = volume_info.get("authors", [empty_value])
            publisher = volume_info.get("publisher", empty_value)
            published_date = volume_info.get("publishedDate", empty_value)
            description = volume_info.get("description", empty_value)
            identifiers = volume_info.get("industryIdentifiers", [])
            page_count = volume_info.get("pageCount", empty_value)
            categories = volume_info.get("categories", [empty_value])
            average_rating = volume_info.get("averageRating", empty_value)
            ratings_count = volume_info.get("ratingsCount", empty_value)
            language = volume_info.get("language", empty_value)
            image_link = (volume_info.get("imageLinks", {})
                          .get("thumbnail", empty_value))
            # preview_link = volume_info.get("previewLink", empty_value)
            # info_link = volume_info.get("infoLink", empty_value)
            # print_type = volume_info.get("printType", empty_value)
            # maturity_rating = volume_info.get("maturityRating", empty_value)
            # access_info = (book_data["items"][0].get("accessInfo", {})
            #                .get("accessViewStatus", empty_value))
            # sale_info = (book_data["items"][0].get("saleInfo", {})
            #              .get("buyLink", empty_value))
            # content_version = volume_info.get("contentVersion", empty_value)

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

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        return infos
