import unittest


def add_numbers(a, b):
    """Retourne la somme de deux nombres."""
    return a + b


class IntegrationTestCase(unittest.TestCase):
    def test_add_numbers(self):
        """Teste la fonction add_numbers."""
        # Cas de test 1
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

        # Cas de test 2
        result = add_numbers(-1, 1)
        self.assertEqual(result, 0)

        # Cas de test 3
        result = add_numbers(-5, -3)
        self.assertEqual(result, -8)

        # Cas de test 4
        result = add_numbers(0, 0)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
