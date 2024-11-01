import subprocess
import re
import os, sys
import shutil
from io import StringIO, FileIO
from contextlib import redirect_stdout, redirect_stderr


def parse_digits(listLines, delim=" "):
    intReg = r'-?\d+'
    floatReg = r'-?\d+(\.\d+)?'
    lines2 = []
    for line in listLines:
        parts = line[:-1].split(delim)
        for i in range(len(parts)):
            if re.fullmatch(intReg, parts[i]):
                parts[i] = int(parts[i])
            elif re.fullmatch(floatReg, parts[i]):
                parts[i] = float(parts[i])
        if len(parts) == 1:
            parts = parts[0]
        lines2.append(parts)
    if len(lines2) == 1:
        lines2 = lines2[0]
    
    return lines2

def run_script(name, args, inputs=None, copyFile=None, repo=os.getcwd(), filesFolder=os.getcwd()):
    assert name.split('.')[-1] == "py", "'run_script' runs python scripts only"
    if not os.path.exists(filesFolder):
        os.mkdir(filesFolder)
    inputFileName = os.path.join(filesFolder, "input.txt")
    errorsFileName = os.path.join(filesFolder, "errors.txt")
    outputFileName = os.path.join(filesFolder, "output.txt")

    appFileName = os.path.join(repo, name)
    args = [str(a) for a in args]
    command = ["python", appFileName, *args]

    if not copyFile is None:
        for fileFrom, fileTo in copyFile:
            shutil.copyfile(fileFrom, fileTo)

    with open(inputFileName, 'w+') as f:
        if isinstance(inputs, list):
            f.writelines(inputs)

    with open(outputFileName, 'w+') as fout, open(errorsFileName, 'w+') as ferr, open(inputFileName, 'r+') as fin:
        proc = subprocess.run(command, stdout=fout, stderr=ferr, stdin=fin)
    with open(outputFileName, 'r') as f:
        res = f.readlines()
    with open(errorsFileName, 'r') as f:
        err = f.readlines()

    if proc.returncode:
        print(f"\nDuring run command:\n'{' '.join(command)}'\nerrors occured:\n")
        print(' '.join(err[-1:]))
        print("End of internal errors\n")
    return proc.returncode,res,err


if __name__=="__main__":
    root = os.getcwd()
    dataFileName = "data.csv"
    filePathData = os.path.join(root, "tests", "etalon", dataFileName)
    flag,expected,err = run_script("main.py", [filePathData, 20], 
                              repo=os.path.join(root, "tests", "etalon"),
                              filesFolder=os.path.join(root, "tests", "etalon", "files"), 
                              )