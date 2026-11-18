import unittest

from tiny_prefix_sum_array import PrefixSumArray


class TestPrefixSumArray(unittest.TestCase):
    def test_empty(self):
        p = PrefixSumArray([])
        self.assertEqual(len(p), 0)
        self.assertEqual(p.size, 0)
        self.assertEqual(p.total(), 0)
        self.assertEqual(p.query(0, 0), 0)
        self.assertEqual(p.prefix_at(0), 0)

    def test_single(self):
        p = PrefixSumArray([7])
        self.assertEqual(p.size, 1)
        self.assertEqual(p.total(), 7)
        self.assertEqual(p.query(0, 1), 7)
        self.assertEqual(p.query(0, 0), 0)
        self.assertEqual(p.query(1, 1), 0)
        self.assertEqual(p.prefix_at(0), 0)
        self.assertEqual(p.prefix_at(1), 7)

    def test_basic_ranges(self):
        p = PrefixSumArray([1, 2, 3, 4, 5])
        self.assertEqual(p.query(0, 5), 15)
        self.assertEqual(p.query(0, 1), 1)
        self.assertEqual(p.query(1, 3), 5)
        self.assertEqual(p.query(2, 5), 12)
        self.assertEqual(p.query(4, 5), 5)
        self.assertEqual(p.prefix_at(3), 6)

    def test_negative_and_float(self):
        p = PrefixSumArray([-1, 2.5, -3, 0.5])
        self.assertAlmostEqual(p.total(), -1.0)
        self.assertAlmostEqual(p.query(1, 4), 0.0)
        self.assertAlmostEqual(p.query(0, 2), 1.5)

    def test_query_out_of_bounds(self):
        p = PrefixSumArray([1, 2, 3])
        for left, right in [(-1, 1), (0, 4), (2, 1), (4, 4), (3, 2)]:
            with self.assertRaises(IndexError):
                p.query(left, right)

    def test_prefix_at_out_of_bounds(self):
        p = PrefixSumArray([1, 2, 3])
        with self.assertRaises(IndexError):
            p.prefix_at(-1)
        with self.assertRaises(IndexError):
            p.prefix_at(4)

    def test_type_rejection(self):
        with self.assertRaises(TypeError):
            PrefixSumArray([1, "two"])
        with self.assertRaises(TypeError):
            PrefixSumArray([1, None])
        with self.assertRaises(TypeError):
            PrefixSumArray([1, 2 + 3j])

    def test_accepts_bool(self):
        p = PrefixSumArray([True, False, True])
        self.assertEqual(p.total(), 2)
        self.assertEqual(p.query(0, 2), 1)

    def test_accepts_generator(self):
        p = PrefixSumArray(x for x in range(5))
        self.assertEqual(p.size, 5)
        self.assertEqual(p.total(), 10)

    def test_repr(self):
        p = PrefixSumArray([1, 2, 3])
        self.assertEqual(repr(p), "PrefixSumArray(size=3)")

    def test_consistency_with_manual_sum(self):
        values = [3, -1, 4, -1, 5, -9, 2, 6]
        p = PrefixSumArray(values)
        for left in range(len(values) + 1):
            for right in range(left, len(values) + 1):
                self.assertEqual(p.query(left, right), sum(values[left:right]))


if __name__ == "__main__":
    unittest.main()
