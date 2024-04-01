import unittest
from mycheck import analyze


class Controller(unittest.TestCase):

    def setUp(self) -> None:
        self.con = analyze()
        return

    def tearDown(self) -> None:
        self.con = None
        return

    def test_ka_R(self):
        excepted = 5
        result = self.con.ka_R()
        self.assertEqual(excepted, result)


if __name__ == '__main__':
    unittest.main()
