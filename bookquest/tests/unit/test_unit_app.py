import unittest

from app.ocr import OCR


def to_uppercase(s):
    """Retourne la chaîne en majuscules."""
    return s.upper()


class SimpleTestCase(unittest.TestCase):
    def test_to_uppercase(self):
        """Teste la fonction to_uppercase."""
        self.assertEqual(to_uppercase("hello"), "HELLO")
        self.assertEqual(to_uppercase("world"), "WORLD")
        self.assertEqual(to_uppercase("Python"), "PYTHON")
        self.assertEqual(to_uppercase(""), "")

    def test_is_valid_code(self):
        """Teste la fonction is_valid_code."""
        ocr = OCR()
        self.assertEqual(ocr.is_valid_code("123456789X"), True)
        self.assertEqual(ocr.is_valid_code("1234567890"), False)


if __name__ == '__main__':
    unittest.main()
