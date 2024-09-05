import re

import cv2
import easyocr
from pyzbar.pyzbar import decode

regex_13 = r'9(?:[ -]*7)(?:[ -]*[89])(?:[ -]*\d){10}'
regex_10 = r'\d(?:[ -]*\d){8}(?:[ -]*[\dX])'


class OCR:

    def __init__(self):
        super().__init__()

    def imread(self, path: str):
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

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

    # TODO : utiliser ça quand on enregistre un isbn10 dans la db et
    #  qu'un isbn13 n'est pas dispo !
    def get_isbn13_from_isbn10(self, isbn_10, prefix: str = "978"):
        return prefix + isbn_10[:-1] + self.compute_isbn13_code(
            prefix + isbn_10[:-1])

    def compute_isbn13_code(self, isbn_13_without_code) -> str:
        val = 0
        for i in range(12):
            val += int(isbn_13_without_code[i]) * (1 if i % 2 == 0 else 3)
        r = val % 10
        return str(r) if r == 0 else str(10 - r)
