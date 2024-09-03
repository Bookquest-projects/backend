import unittest

from bookquest.app.ocr import OCR


class SimpleTestCase(unittest.TestCase):
    def test_is_valid_code(self):
        """Teste the is_valid_code function"""
        ocr = OCR()

        # Valid ISBN-10
        self.assertTrue(ocr.is_valid_code('0306406152'))
        self.assertTrue(ocr.is_valid_code('1566199093'))
        self.assertTrue(ocr.is_valid_code('123456789X'))

        # Invalid ISBN-10
        self.assertFalse(ocr.is_valid_code('0306406153'))
        self.assertFalse(ocr.is_valid_code('1566199090'))
        self.assertFalse(ocr.is_valid_code('034297719A'))
        self.assertFalse(ocr.is_valid_code('034297719'))

        # valid ISBN-13
        self.assertTrue(ocr.is_valid_code('9782021290639'))
        self.assertTrue(ocr.is_valid_code('9798988013112'))

        # Invalid ISBN-13
        self.assertFalse(ocr.is_valid_code('9782021290630'))
        self.assertFalse(ocr.is_valid_code('9798988013115'))
        self.assertFalse(ocr.is_valid_code('978202129063X'))
        self.assertFalse(ocr.is_valid_code('978202129063'))


if __name__ == '__main__':
    unittest.main()
