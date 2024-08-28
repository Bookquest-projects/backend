import json
from urllib.request import urlopen


class BookRepository:

    def findBookByIsbn(self, isbn):
        api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

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

            identifier_strings = []
            for identifier in identifiers:
                type = identifier.get('type', 'N/A')
                id_value = identifier.get('identifier', 'N/A')
                identifier_strings.append(f"{type}: {id_value}")
            identifiers_str = ', '.join(identifier_strings)

            info = {
                "title": title,
                "subtitle": subtitle,
                "authors": authors,
                "publisher": publisher,
                "published_date": published_date,
                "description": description,
                "identifiers": identifiers_str,
                "page_count": page_count,
                "categories": categories,
                "average_rating": average_rating,
                "ratings_count": ratings_count,
                "language": language,
                "image_link": image_link,
                "preview_link": preview_link,
                "info_link": info_link,
                "print_type": print_type,
                "maturity_rating": maturity_rating,
                "access_info": access_info,
                "sale_info": sale_info,
                "content_version": content_version
            }

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        return info
