import unittest
import lab5


class TestClass(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        expr = 'rot(1.57) @ inv(tran(2, 3)) @ tran(2, 3) @ rot(-1.57/2) * [1, 0]'
        res = lab5.calculate_expr(expr)
        
        self.assertAlmostEqual(res[0], 0.7073882691671998)
        self.assertAlmostEqual(res[1], 0.706825181105366)
    
    @staticmethod
    def startTests():
        unittest.main()
        
        
if __name__ == '__main__':
    TestClass.startTests()
