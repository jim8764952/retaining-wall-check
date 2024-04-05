import os
import sys
import unittest
from mycheck import analyze

# my_lib_path = os.path.abspath('D://python//retaining-wall-check//mycheck')
# sys.path.append(my_lib_path)


class Controller(unittest.TestCase):

    def setUp(self) -> None:
        self.con = analyze.analyze()
        return

    def tearDown(self) -> None:
        self.con = None
        return

    def test_FSFall(self):
        excepted = 2.42
        res = self.con.FSFall()
        self.assertEqual(excepted, round(res, 2))

    def test_FSSlide(self):
        excepted = 2.45
        res = self.con.FSSlide()
        self.assertAlmostEqual(excepted, round(res, 2))

    def test_FSCarrying(self):
        excepted = 4.61
        res = self.con.FSCarrying()
        self.assertAlmostEqual(excepted, round(res, 2))


if __name__ == '__main__':
    unittest.main()
