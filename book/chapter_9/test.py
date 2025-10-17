import unittest
from add import add

class TestUnitCase(unittest.TestCase):
    def testing_add(self):
        self.assertEqual(add(2,5), 7)