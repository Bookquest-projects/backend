def is_valid_isbn(isbn):
    def _validate_isbn10(isbn_10):
        val = 0
        for i in range(10, 1, -1):
            val = val + i * int(isbn[10 - i])
        return (11 - val % 11 == 10 and isbn[
            -1] == "X") or 11 - val % 11 == int(isbn[-1])

    def _validate_isbn13(isbn_13):
        if not isbn.startswith(("978", "979")):
            return False

        val = 0
        for i in range(12):
            val += int(isbn[i]) * (1 if i % 2 == 0 else 3)
        r = val % 10
        return (r == 0 and r == int(isbn[12])) or 10 - r

    if len(isbn) == 10:
        return _validate_isbn10(isbn)
    elif len(isbn) == 13:
        return _validate_isbn13(isbn)
    return False
