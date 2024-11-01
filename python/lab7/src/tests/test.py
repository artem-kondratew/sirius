import unittest
import lab7


class TestClass(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        pass
        
    @unittest.expectedFailure
    def test_1_failure(self):
        pass
    
    @staticmethod
    def startTests():
        unittest.main()
        
        
if __name__ == '__main__':
    TestClass.startTests()
