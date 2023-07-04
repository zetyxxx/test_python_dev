import random
from main import *
import unittest


class TestAddNumbers(unittest.TestCase):
    def test1(self):
        x1 = [i for i in range(100)]
        y1 = [random.randint(-100, 100) for _ in range(100)]
        k1 = 2
        polinom(y1, x1, k1)

    @unittest.expectedFailure
    def test2(self):
        x2 = ['a', 'b', 'c', 'd', 'e']
        y2 = ['f', 'g', 'h', 'i', 'j']
        k2 = 3
        polinom(y2, x2, k2)

    @unittest.expectedFailure
    def test3(self):
        x3 = [i for i in range(10)]
        y3 = [random.randint(-100, 100) for _ in range(10)]
        k3 = 'qwe'
        polinom(y3, x3, k3)

    @unittest.expectedFailure
    def test4(self):
        x4 = [i for i in range(10)]
        y4 = [random.randint(-100, 100) for _ in range(10)]
        k4 = -10
        polinom(y4, x4, k4)

if __name__ == '__main__':
    unittest.main()






