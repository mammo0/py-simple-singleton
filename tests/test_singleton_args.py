import unittest

from tests.res.singleton_args_class import TSingletonArgs, TSingletonArgsWithoutInit


class Test(unittest.TestCase):
    def test_with_same_args(self):
        arg1 = "test_arg"

        instance1 = TSingletonArgs(arg1)
        instance2 = TSingletonArgs(arg1)

        # the instances must be equal
        self.assertEqual(instance1, instance2)
        self.assertEqual(instance1.param1, instance2.param1)
        self.assertEqual(arg1, instance1.param1)

    def test_with_different_args(self):
        arg1 = "first_arg"
        arg2 = "second_arg"

        instance1 = TSingletonArgs(arg1)
        instance2 = TSingletonArgs(arg2)
        instance3 = TSingletonArgs(arg1, arg2)

        # the instances must not be equal
        self.assertNotEqual(instance1, instance2)
        self.assertNotEqual(instance1, instance3)
        self.assertNotEqual(instance2, instance3)

        self.assertEqual(instance1.param1, arg1)
        self.assertEqual(instance2.param1, arg2)
        self.assertEqual(instance1.param1, instance3.param1)
        self.assertEqual(instance2.param1, instance3.param2)

    def test_class_without_init(self):
        instance1 = TSingletonArgsWithoutInit()
        instance2 = TSingletonArgsWithoutInit()

        self.assertEqual(instance1, instance2)


if __name__ == "__main__":
    unittest.main()
