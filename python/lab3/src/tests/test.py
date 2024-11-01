import unittest
import os
import sys
from lab3 import get_c


class TestClass(unittest.TestCase):
    
    def setUp(self):
        print('initializing tests')

    def tearDown(self):
        print('closing tests')

    @unittest.expectedFailure
    def test_1_failure(self):
        self.assertEqual(get_c(), 1)
    
    @staticmethod
    def startTests():
        unittest.main()

if __name__ == '__main__':
    TestClass.startTests()
