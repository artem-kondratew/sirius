import unittest
from parameterized import parameterized
from ExtraFunctions import *
from PathFunctions import *
import os
import shutil

class TestTree(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.root = os.getcwd()
        self.tree = build_directory_tree(self.root)
        self.tree.pop(".cache")
        self.tree.pop(".git")
        self.tree.pop("build")
        self.tree = {k:v for k,v in self.tree.items() if not re.match(r'.*env.*', k)}

        self.listPath = tree2listpath(self.tree)
        self.listPath = {p for p in self.listPath if not re.match(r'.*\.egg-info', p)}
        
        p  =reg_path("src", r"[a-z, A-Z, \d]*")
        subProjects = hasRegItem(self.listPath, p)
        try:
            subProjects.remove(os.path.join("src", "tests"))
        except ValueError:
            pass
        self.subProjects = subProjects

    @parameterized.expand([
        (["src"], "dir"),
        (["README.md"], "file"),
        ([".gitignore"], "file"),
    ])
    def test_src_tree(self, path, type):
        pathStr = os.path.join(*path)
        self.assertTrue(has_item(self.tree, pathStr, type), f"Project folder must contain '{pathStr}'")

    @parameterized.expand([
        ([r"[A_Za-z\d]\.txt"], ["requirements.txt"]),
        (["src",r"[A_Za-z\d]\.txt"], []),
        (["src", r"tests?",r"[A_Za-z\d]\.txt"], []),
        ([r".*\.csv"], []),
        (["src",r"[A_Za-z\d]\.csv"], []),
        (["src", r"tests?",r"[A_Za-z\d]\.csv"], []),
        ([r"\.vs"], []),
    ])
    def test_restricted_files(self, restrictedFiles, exclude):
        p = reg_path(*restrictedFiles)
        res = hasRegItem(self.listPath, p)

        for e in exclude:
            pe = reg_path(e)
            r = hasRegItem(self.listPath, pe)
            for item in r:
                if item in res:
                    res.remove(item)
        self.assertFalse(res, "Project contains restricted file(s): \n" + "\n".join(res))

    def test_project_tree(self):
        for pathStr in self.subProjects:
            self.assertTrue(has_item(self.tree, os.path.join(pathStr, "__main__.py"), "file"), f"Project folder must contain '__main__.py'")
            self.assertTrue(has_item(self.tree, os.path.join(pathStr, "__init__.py"), "file"), f"Project folder must contain '__init__.py'")

    def test_setup(self):
        self.assertTrue(has_item(self.tree, os.path.join("setup.py"), "file") or \
                        has_item(self.tree, os.path.join("pyproject.toml"), "file")
        , f"Project folder must contain one of setup files")



class TestPackage(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        root = os.getcwd()
        tree = build_directory_tree(root)
        tree.pop(".cache")
        tree.pop(".git")
        tree.pop("build")
        tree = {k:v for k,v in tree.items() if not re.fullmatch(r'.*env.*', k)}
        listPath = tree2listpath(tree)
        listPath = {p for p in listPath if not re.fullmatch(r'.*\.egg-info', p)}
        listPath = {p for p in listPath if re.fullmatch(r'src.{1,4}[A-Za-z\d]*', p)}
        listPath = {p for p in listPath if not re.fullmatch(r'.*test.*', p)}
        self.subProjects = listPath
        
        

    def test_install_package(self):
        pexits = []
        errors = []
        try:
            print()
            print("Launch modules")
            print(self.subProjects)
            for module in self.subProjects:
                module = os.path.split(module)[-1]
                command = "python -m "+module
                print(f"Launch module: '{command}'")
                pexits.append(subprocess.run("python -m "+module, shell=True))
            
            command = "python "+ os.path.join("src", "tests", "test.py") 
            print(f"Launch tests: {command}")
            pexits.append(subprocess.run(command, shell=True))

        except Exception as e:
            errors.append(e)
            
        finally:
            # buildDirs = os.listdir(os.getcwd())
            # buildDirs = [d for d in buildDirs if os.path.isdir(d)]
            # print(buildDirs)
            # buildDirs.remove("src") if "src" in buildDirs else None
            # buildDirs.remove("tests") if "tests" in buildDirs else None
            # buildDirs.remove(".git") if ".git" in buildDirs else None
            # buildDirs += hasRegItem(list_path(os.getcwd()), r".*\.egg-info")
            # print(buildDirs)
            # [shutil.rmtree(d) for d in buildDirs]

            pexits = [p.returncode for p in pexits]
            if sum(pexits) or errors!=[]:
                d = dict(zip(["Install package from '.'", "Launch package using __main__.py", "Launch yours tests for package"], pexits))
                print("Process exits (normally 0):")
                for key, val in d.items():
                    print(key, ": ", val)
                
                if errors:
                    print("Errors occured: \n", errors)
                self.fail("Fail to install and launch package")
                


def test():
    # try:
        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTree))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPackage))
        runner = unittest.TextTestRunner(verbosity=2)
        res = runner.run(suite)
        if len(res.errors)>0:
            print("Errors during testing occured, please contact to test manager to solve it")
    # except:
    #     print("Errors during testing occured, please contact to test manager to solve it")
        return res


if __name__=="__main__":
    result = test()
    if result.wasSuccessful():
       exit(0)
    else:
       exit(1)