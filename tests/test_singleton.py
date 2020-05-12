import unittest
from tests.res.singleton_class import TestSingleton


class Test(unittest.TestCase):
    def test_basic(self):
        instance1 = TestSingleton()
        instance2 = TestSingleton()

        self.assertEqual(instance1, instance2)

    def test_different_args(self):
        instance1 = TestSingleton("first_instance")
        instance2 = TestSingleton("second_instance")

        # the instances must be equal
        self.assertEqual(instance1, instance2)

        # also the second instance must ignore the 'second_instance' argument
        self.assertEqual(instance1.param1, instance2.param2)


if __name__ == "__main__":
    unittest.main()
