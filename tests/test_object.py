import unittest


class TestObjects(unittest.TestCase):
    """ Contains Test cases for whether two objects are considered to be equal """

    def setUp(self):
        # Load test data
        self.obj1 = object(["shape", "bird1", "rect", 10, 20, 20, [1, 2, 3]])
        self.obj2 = object(["shape", "bird1", "rect", 10, 20, 20, [1, 2, 3]])

    def test_same_values_are_equal(self):
        self.assertEqual(self.obj1, self.obj2,
                         "Objects with same values should be considered equal")

    def test_equal_for_different_id_but_same_materials(self):
        obj1 = object(["shape", "ice0", "rect", 10, 20, 20, [1, 2, 3]])
        obj2 = object(["shape", "ice46", "rect", 10, 20, 20, [1, 2, 3]])
        self.assertEqual(
            obj1, obj2, "Objects with different ids can still be considered equal")

    def test_not_equal_for_different_materials(self):
        self.obj1.material = "stone"
        self.assertNotEqual(
            self.obj1, self.obj2, "Objects with different materials should not be considered equal")

    def test_not_equal_for_different_shape(self):
        self.obj1.shape = "circle"
        self.assertNotEqual(
            self.obj1, self.obj2, "Objects with different shapes should not be considered equal")

    def test_not_equal_for_much_different_center(self):
        self.obj1.cx += 100
        self.assertNotEqual(
            self.obj1, self.obj2, "Objects with much different center should not be considered equal")

    def test_equal_for_similar_center(self):
        self.obj1.cx += 1
        self.obj2.cy -= 3
        self.assertEqual(
            self.obj1, self.obj2, "Objects with similar center should be considered equal")


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from object import object
    else:
        from ..object import object
    unittest.main()
