import re

import cv2
import easyocr
from pyzbar.pyzbar import decode

regex_13 = r'9(?:[ -]*7)(?:[ -]*[89])(?:[ -]*\d){10}'
regex_10 = r'\d(?:[ -]*\d){8}(?:[ -]*[\dX])'
unwanted_chars_default = ['-', ' ']


class OCR:

    def __init__(self):
        super().__init__()

    def imread(self, path: str):
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def clean_isbn(self, isbn: str,
                   chars_to_remove=None) -> str:
        if chars_to_remove is None:
            chars_to_remove = list()
        if len(chars_to_remove) == 0:
            chars_to_remove = unwanted_chars_default.copy()

        isbn_cleaned = '%s' % isbn
        for c in chars_to_remove:
            isbn_cleaned = isbn_cleaned.replace(c, '')
        return isbn_cleaned

    def get_bar_code_info(self, img_cv2):
        detectedBarcodes = decode(img_cv2)

        # if not detectedBarcodes:
        #     # print(
        #     #     "DEBUG Barcode Not Detected or "
        #     #     "your barcode is blank/corrupted!")  # debug
        #     return None
        # else:
        #     for barcode in detectedBarcodes:
        #         if barcode.data != "":
        #             print("DEBUG", barcode.type, barcode.data)  # debug

        return detectedBarcodes

    def is_valid_code(self, isbn: str) -> bool:
        if len(isbn) == 10:
            # print("length 10 ok")
            val = 0
            for i in range(10, 1, -1):
                val = val + i * int(isbn[10 - i])
            return (11 - val % 11 == 10 and isbn[
                -1] == "X") or 11 - val % 11 == int(isbn[-1])
        elif len(isbn) == 13:
            # print("length 13 ok")
            # print("begin with :", isbn[0:3])
            if isbn[0:3] == "978" or isbn[0:3] == "979":
                # print("concern a book")
                val = 0
                for i in range(12):
                    val += int(isbn[i]) * (1 if i % 2 == 0 else 3)
                    # print(val)
                # print(val)
                r = val % 10
                return (r == 0 and r == int(isbn[12])) or 10 - r == int(
                    isbn[12])
            else:
                # print("this barcode is EAN13 but doesn't concern a book")
                return False
        else:
            # print("barcode not recognize as an EAN13 neither ISBN-10")
            return False

    def get_text_info(self, path: str) -> str:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(path)

        # print("-try isbn 13-")
        pattern = re.compile(regex_13, re.UNICODE)
        # print(pattern)
        # print(result)
        not_words = ""
        for (bbox, text, prob) in result:
            if text.isdigit():
                not_words = not_words + text
                if len(not_words) > 13:
                    not_words = not_words[len(not_words) - 13:]
            # print(tmp)
            # print(f'Text: {text}, Probability: {prob}')
            for match in pattern.findall(text):
                # print("\tMATCH : isbn :", match)
                return match

            for match in pattern.findall(not_words):
                # print("\tMATCH : isbn :", match)
                return match

        # print("-try isbn 10-")
        pattern = re.compile(regex_10, re.UNICODE)
        # print(pattern)
        # print(result)
        not_words = ""
        for (bbox, text, prob) in result:
            if text.isdigit() or text == "X":
                not_words = not_words + text
                if len(not_words) > 10:
                    not_words = not_words[len(not_words) - 10:]
            # print(tmp)
            # print(f'Text: {text}, Probability: {prob}')
            for match in pattern.findall(text):
                # print("\tMATCH : isbn :", match)
                return match

            for match in pattern.findall(not_words):
                # print("\tMATCH : isbn :", match)
                return match

        return ""
