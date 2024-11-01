import os
import re 


def build_directory_tree(root):
    L = os.listdir(root)
    tr = {}
    for i in range(len(L)):
        item = os.path.join(root,L[i])
        if os.path.isdir(item):
            tr[L[i]] = build_directory_tree(item)
        else:
            tr[L[i]] = "file"
    return tr

def has_item(tree:dict, path, type="any"):
    pathList = path.split('\\')
    res = False

    N = len(pathList)
    for i in range(N):
        item = pathList[i]
        if item in tree.keys():
            tree = tree[item]

            if i == N-1: # last item, file or dir
                if type == "any":
                    continue
                d = "file" if tree == "file" else "dir"
                if not d == type:
                    break            
        else:
            break
    else:
        res = True
    return res

def has_reg_item(tree, regPathList):
    N = len(regPathList)
    for i in range(N):
        regPath = regPathList[i]
        for item in tree.keys():
            if not re.fullmatch(regPath, item):
                pass
        



        for item in corresp:
            tree = tree[item]

            if i == N-1: # last item, file or dir
                if type == "any":
                    continue
                d = "file" if tree == "file" else "dir"
                if not d == type:
                    break            
        else:
            break
    else:
        res = True
    return res

def tree2listpath(tree):
    res = []
    for key,val in tree.items():
        if val == "file":
            res.append(key)
        else:
            res.append(key)
            L = tree2listpath(val)
            L2 = [os.path.join(key, p) for p in L]
            res +=L2
    return res

def hasRegItem(listPath, regPath):
    res = []
    for item in listPath:
        m = re.fullmatch(regPath, item)
        if m:
            res.append(m.group())
    return res
    
def list_path(root):
    return tree2listpath(build_directory_tree(root))

def reg_path(*args):
    return r"\\".join(args)

if __name__ == "__main__":
    root = os.path.join(os.getcwd(), "tests", "etalon")
    L = list_path(root)

    print(L)
    print(hasRegItem(L, reg_path("src", "tests", r".*.py")))
