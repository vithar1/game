import unittest

from src.main.objects.units.unit import Unit


class UnitTest(unittest.TestCase):

    def setUp(self) -> None:
        self.unit = Unit('foo')
        self.foo = 'FOO'

    def test1(self):
        self.assertTrue(self.foo.isupper())
        self.assertFalse(self.unit.name.isupper())
