import unittest

from modules.Intersection import Intersection
from modules.Street import Street


class TestStreet(unittest.TestCase):
    def test_street(self):
        street = Street()
        self.assertTrue(1 == 1)


class TestIntersection(unittest.TestCase):
    def test_street(self):
        inter = Intersection()
        self.assertTrue(1 == 1)


if __name__ == '__main__':
    unittest.main()
