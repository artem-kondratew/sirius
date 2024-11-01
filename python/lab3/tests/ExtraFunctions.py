import subprocess
import re
import os
import shutil

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

def run_script(name, args, inputs=None, copyFile=None, repo=os.getcwd(), filesFolder=os.getcwd(), py=True):
    if not os.path.exists(filesFolder):
        os.mkdir(filesFolder)

    inputFileName = os.path.join(filesFolder, "input.txt")
    errorsFileName = os.path.join(filesFolder, "errors.txt")
    outputFileName =os.path.join(filesFolder, "output.txt")
    appFileName = os.path.join(repo, name)
    args = [str(a) for a in args]
    command = [appFileName, *args]
    if name.split('.')[-1]=='py':
        command = ["python"]+command

    if not copyFile is None:
        for fileFrom, fileTo in copyFile:
            shutil.copyfile(fileFrom, fileTo)

    with open(inputFileName, 'w+') as f:
        if isinstance(inputs, list):
            f.writelines(inputs)

    with open(outputFileName, 'w+') as fout, open(errorsFileName, 'w+') as ferr, open(inputFileName, 'r+') as fin:
        subprocess.run(command, stdout=fout, stderr=ferr, stdin=fin)
    with open(outputFileName, 'r') as f:
        res = f.readlines()
    return res
