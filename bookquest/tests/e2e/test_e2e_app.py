import unittest


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


class MathOperationsTestCase(unittest.TestCase):
    def test_add(self):
        """Test de la fonction add."""
        result = add(1, 2)
        self.assertEqual(result, 3)

    def test_subtract(self):
        """Test de la fonction subtract."""
        result = subtract(5, 3)
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()
