import unittest


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


if __name__ == '__main__':
    unittest.main()
