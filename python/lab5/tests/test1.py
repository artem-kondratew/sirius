import unittest
from parameterized import parameterized
from ExtraFunctions import *
from PathFunctions import *
from etalon.gen_data import generateEvalString
import os
import numpy as np


class EtalonError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Test1(unittest.TestCase):

    def find_module(self):
        modules = find_modules()
        self.assertTrue(len(modules)==1,  f"Expected one module for launch, got {len(modules)}, found modules: {modules}")
        module = modules[0]
        p = os.path.join(os.getcwd(), "src", module)
        pm = os.path.join(p, "main.py")
        ex = os.path.exists(pm)
        self.assertTrue(ex,  f"'main.py' file not found in {p}")
        return p

    @parameterized.expand([
        ("rot", f"rot({np.pi/6})"),
        ("tran", f"tran(5, 6.89)"),
        ("rot_tran", f"rot({np.pi/6})@tran(5, 6.89)"),
        ("inv", f"inv(rot({np.pi/6})@tran(5, 6.89))"),
        ("rot_vec", f"rot({np.pi/6})@[0.5, {np.sqrt(3)/2}]"),
        ("tran_vec", f"tran(5, 0)@[0.5, {np.sqrt(3)/2}]"),
        ("double_inv_vec", f"inv(rot({np.pi/6})@tran(5, 6.89))@rot({np.pi/6})@tran(5, 6.89)@[0.5, {np.sqrt(3)/2}]"),
        *[("random", generateEvalString(70)) for _ in range(5)],
    ])
    def test(self, name, s):
        root = os.getcwd()
        
        flag,res,err = run_script("main.py", [s], 
                        repo=self.find_module(),
                        filesFolder=os.path.join(root, "tests", "files"), 
                        )
        self.assertFalse(flag, "Internal program errors")
        # print(f"\nGot program output:\n{res}")
        # print(f"End of program output")
        self.assertTrue(len(res) == 1, f"Output must contain only one string with end 'newline', got {len(res)} strings")
        res = res[0]

        

        flag,expected,err = run_script("main.py", [s], 
                              repo=os.path.join(root, "tests", "etalon"),
                              filesFolder=os.path.join(root, "tests", "etalon", "files"), 
                              )
        if flag or len(expected) != 1:
            raise EtalonError("EtalonError")
        expected = expected[0]
       
        self.assertEqual(res, expected, f"Output string are not equal:\n Expected: '{expected}'\nGot: {res}")
    
def test():
    try:
        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test1))
        runner = unittest.TextTestRunner(verbosity=2)
        res = runner.run(suite)
        if len(res.errors)>0:
            print("Errors during testing occured, please contact to test manager to solve it")
    except Exception as e:
        print(e)
        print("Errors during testing occured, please contact to test manager to solve it")
    return res


if __name__=="__main__":
    result = test()
    if result.wasSuccessful():
       exit(0)
    else:
       exit(1)