import cv2
from pyzbar.pyzbar import decode


class OCR:

    def __init__(self):
        super().__init__()

    def imread(self, path: str):
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def clean_isbn(self, isbn: str, unwanted_chars=['-', ' ']) -> str:
        isbn_cleaned = '%s' % isbn
        for c in unwanted_chars:
            isbn_cleaned = isbn_cleaned.replace(c, '')
        return isbn_cleaned

    def tmp_debug(self, path: str):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        cv2.imshow(path, img)

        # waits for user to press any key
        # (this is necessary to avoid Python kernel form crashing)
        cv2.waitKey(0)

        # closing all open windows
        cv2.destroyAllWindows()

    def get_bar_code_info(self, img_cv2):
        detectedBarcodes = decode(img_cv2)

        if not detectedBarcodes:
            print(
                "DEBUG Barcode Not Detected or "
                "your barcode is blank/corrupted!")  # debug
            return None
        else:
            for barcode in detectedBarcodes:
                if barcode.data != "":
                    print("DEBUG", barcode.type, barcode.data)  # debug

        return detectedBarcodes

    def is_valid_code(self, isbn: str) -> bool:
        if len(isbn) == 10:
            # print("lenght 10 ok")
            val = 0
            for i in range(10, 1, -1):
                val = val + i * int(isbn[10 - i])
            return (11 - val % 11 == 10 and isbn[
                -1] == "X") or 11 - val % 11 == int(isbn[-1])
        elif len(isbn) == 13:
            # print("lenght 13 ok")
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
                print("this barcode is EAN13 but doesn't concern a book")
                return False
        else:
            print("barcode not reconnize as an EAN13 neither ISBN-10")
            return False
