import unittest
from Ship import Ship


class TestShip(unittest.TestCase):
    def test_is_sunk_when_hits_equal_length(self):
        s = Ship('Destroyer', 2)
        self.assertFalse(s.is_sunk(), "New ship should not be sunk")
        s.hit()
        self.assertFalse(s.is_sunk(), "Ship with 1/2 hits should not be sunk")
        s.hit()
        self.assertTrue(s.is_sunk(), "Ship with 2/2 hits should be sunk")

    def test_is_sunk_with_extra_hits(self):
        s = Ship('Sub', 1)
        s.hit()
        s.hit()  # extra hit should still be considered sunk
        self.assertTrue(s.is_sunk())


if __name__ == '__main__':
    unittest.main()
