import unittest
from tests.res.singleton_class import TSingleton


class Test(unittest.TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        # reset the singleton classes (for further tests)
        TSingleton._instance = None

    def test_basic(self) -> None:
        instance1: TSingleton = TSingleton()
        instance2: TSingleton = TSingleton()

        self.assertEqual(instance1, instance2)

    def test_different_args(self) -> None:
        instance1: TSingleton = TSingleton("first_instance")
        instance2: TSingleton = TSingleton("second_instance")

        # the instances must be equal
        self.assertEqual(instance1, instance2)

        # also the second instance must ignore the 'second_instance' argument
        self.assertEqual(instance1.param1, instance2.param2)


if __name__ == "__main__":
    unittest.main()
