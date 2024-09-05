def is_valid_isbn(isbn):
    def _validate_isbn10(isbn_10):
        total = 0
        for i in range(10, 1, -1):
            total += i * int(isbn_10[10 - i])
        check_digit = 11 - total % 11
        return (check_digit == 10 and isbn_10[
            -1] == "X") or check_digit == int(isbn_10[-1])

    def _validate_isbn13(isbn_13):
        if not isbn.startswith(("978", "979")):
            return False

        total = 0
        for i in range(12):
            total += int(isbn_13[i]) * (1 if i % 2 == 0 else 3)
        check_digit = (10 - total % 10) % 10
        return check_digit == int(isbn_13[-1])

    if len(isbn) == 10:
        if not (isbn[:-1].isdigit() and (
                isbn[-1].isdigit() or isbn[-1] == "X")):
            return False
        return _validate_isbn10(isbn)
    elif len(isbn) == 13:
        if not isbn.isdigit():
            return False
        return _validate_isbn13(isbn)
    return False


def clean_isbn(isbn: str, chars_to_remove=None) -> str:
    if chars_to_remove is None:
        chars_to_remove = list()

    if len(chars_to_remove) == 0:
        chars_to_remove = ['-', ' ']

    isbn_cleaned = '%s' % isbn
    for c in chars_to_remove:
        isbn_cleaned = isbn_cleaned.replace(c, '')
    return isbn_cleaned
