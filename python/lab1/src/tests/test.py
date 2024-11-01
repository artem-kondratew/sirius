import unittest
from lab1 import get_pi


class TestClass(unittest.TestCase):
    
    def setUp(self):
        print('initializing tests')

    def tearDown(self):
        print('closing tests')

    def test_get_pi_1(self):
        self.assertEqual(get_pi(3), '3.14')
        
    def test_get_pi_2(self):
        self.assertEqual(get_pi(5), '3.1416')

    @unittest.expectedFailure
    def test__get_pi_1_failure(self):
        self.assertEqual(get_pi(5), '3.14')
        
    @unittest.expectedFailure
    def test__get_pi_2_failure(self):
        self.assertEqual(get_pi(5), '3.14160')
    
    @staticmethod
    def startTests():
        unittest.main()
