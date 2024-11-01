import unittest
import lab6
import numpy as np
import cv2 as cv
import os
import sys


class TestClass(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        env = np.array([[1, 3, 3, 4],
                        [7, 2, 6, 1],
                        [10, 9, 1, 2],
                        [4, 2, 5, 8]])
        
        img_name = 'map_test.png'
        cv.imwrite(img_name, env)
        
        img_path = os.path.join(os.path.dirname(lab6.__file__), img_name)
        sys.argv = ['mock argv', img_path]
        
        self.assertEqual(lab6.generate_path(env), [(0, 3), (1, 3), (2, 3), (2, 2), (3, 2)])
        
    # @unittest.expectedFailure
    # def test__get_pi_2_failure(self):
    #     self.assertEqual(get_pi(5), '3.14160')
    
    @staticmethod
    def startTests():
        unittest.main()
        
        
if __name__ == '__main__':
    TestClass.startTests()
