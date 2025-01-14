import unittest
from matrices.routines.base26 import Base26


class TestBase26(unittest.TestCase):

    def test_to_excel(self):
        self.assertEqual(Base26.to_excel(1), 'A')
        self.assertEqual(Base26.to_excel(26), 'Z')
        self.assertEqual(Base26.to_excel(27), 'AA')
        self.assertEqual(Base26.to_excel(52), 'AZ')
        self.assertEqual(Base26.to_excel(53), 'BA')
        self.assertEqual(Base26.to_excel(702), 'ZZ')
        self.assertEqual(Base26.to_excel(703), 'AAA')

    def test_from_excel(self):
        self.assertEqual(Base26.from_excel('A'), 1)
        self.assertEqual(Base26.from_excel('Z'), 26)
        self.assertEqual(Base26.from_excel('AA'), 27)
        self.assertEqual(Base26.from_excel('AZ'), 52)
        self.assertEqual(Base26.from_excel('BA'), 53)
        self.assertEqual(Base26.from_excel('ZZ'), 702)
        self.assertEqual(Base26.from_excel('AAA'), 703)


if __name__ == '__main__':
    unittest.main()
# The test case above is a unit test for the Base26 class.
# It tests the conversion between Excel column numbers and Base26 numbers.
