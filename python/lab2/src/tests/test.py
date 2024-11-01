import unittest
import lab2
import os
import sys


data = os.path.join(os.path.dirname(lab2.__file__), 'data', 'data.txt')


class TestClass(unittest.TestCase):
    
    def setUp(self):
        print('initializing tests')

    def tearDown(self):
        print('closing tests')

    # @unittest.mock.patch('sys.argv', ['mock.py', data])
    def test_1(self):
        sys.argv = ['mock argv', data] 
        self.assertEqual(lab2.main(), '* \n' \
                                      ' *\n' \
                                      '\n' \
                                      '  \n' \
                                      '**\n\n')

    @unittest.expectedFailure
    def test_1_failure(self):
        self.assertEqual(lab2.main(), '')
        
    @unittest.expectedFailure
    def test_2_failure(self):
        self.assertEqual(lab2.main(), '* \n *\n\n * \n**\n\n')
    
    @staticmethod
    def startTests():
        global data
        data = '* \n' \
               ' *'
        with open(data, 'w') as file:
            file.write(data)
        unittest.main()

if __name__ == '__main__':
    TestClass.startTests()

