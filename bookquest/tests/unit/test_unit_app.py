import unittest

from bookquest.app.helper import is_valid_isbn


class SimpleTestCase(unittest.TestCase):
    def test_is_valid_code(self):
        """Teste the is_valid_code function"""
        # Invalid length
        self.assertFalse(is_valid_isbn('034297719'))
        self.assertFalse(is_valid_isbn('978202129063'))

        # Valid ISBN-10
        self.assertTrue(is_valid_isbn('0306406152'))
        self.assertTrue(is_valid_isbn('1566199093'))
        self.assertTrue(is_valid_isbn('123456789X'))

        # Invalid ISBN-10
        self.assertFalse(is_valid_isbn('0306406153'))
        self.assertFalse(is_valid_isbn('1566199090'))
        self.assertFalse(is_valid_isbn('034297719A'))

        # valid ISBN-13
        self.assertTrue(is_valid_isbn('9782021290639'))
        self.assertTrue(is_valid_isbn('9798988013112'))

        # Invalid ISBN-13
        self.assertFalse(is_valid_isbn('9782021290630'))
        self.assertFalse(is_valid_isbn('9798988013115'))
        self.assertFalse(is_valid_isbn('978202129063X'))


if __name__ == '__main__':
    unittest.main()
