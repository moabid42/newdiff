import subprocess
import argparse
import os

BLUE = '\033[94m'
GRAY = '\033[97m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[00m'

def disableColors():
    global BLUE
    global GRAY
    global RED
    global GREEN
    global YELLOW
    global RESET
    RESET = ''
    BLUE = RESET
    GRAY = RESET
    RED = RESET
    GREEN = RESET
    YELLOW = RESET

def cdRun(command, runDir):
    wd = os.getcwd()
    os.chdir(runDir)
    result = subprocess.run(command, capture_output=True, text=True)
    os.chdir(wd)
    return result.stdout.split('\n')

def clean(arr):
    arr.pop()
    return arr

def printPerms(elem1, elem2):
    print(YELLOW + '===========================================' + RESET)
    print(elem1)
    print(elem2)
    print(YELLOW + '===========================================' + RESET)

def generateDiffs(file1, file2):
    command = f'diff -u {file1} {file2}'
    result = subprocess.run(command.split(), capture_output=True, text=True)
    with open(file2 + '.diff', 'w') as file:
        file.write(result.stdout)

def getFullPath(dirPath, path):
    if dirPath[-1] == '/':
        return dirPath[:-1] + path[1:]
    return dirPath + path[1:]

def arrange(dir1, dir2, perms1, perms2, isPerms, isFileDiffs):
    flag = False
    for elem in perms1:
        for item in perms2:
            if elem.split()[3] == item.split()[3]:
                if isPerms:
                    printPerms(elem, item)
                if isFileDiffs:
                    generateDiffs(getFullPath(dir1, elem.split()[3]), getFullPath(dir2, item.split()[3]))
                break
            elif item == perms2[-1]:
                flag = True
        if flag == True:
            if isPerms:
                printPerms(elem, 'not found')
            flag = False
    print('\n\n')

def getFilesPerms(dir1, dir2, depth, exclude, isPerms, isFileDiffs):
    print(GREEN + 'Comparing file permissions ...' + RESET)
    if depth != None:
        if exclude != None:
            cmd1 = f'find . -maxdepth {depth} -not -path {exclude} -printf {RED}%-20M{RESET}%-10u%-10g{BLUE}%-10p{RESET}\\n'.split()
            cmd2 = f'find . -maxdepth {depth} -not -path {exclude} -printf {RED}%-20M{RESET}%-10u%-10g{BLUE}%-10p{RESET}\\n'.split()
        else:
            cmd1 = f'find . -maxdepth {depth} -printf {RED}%-20M{RESET}%-10u%-10g{BLUE}%-10p{RESET}\\n'.split()
            cmd2 = f'find . -maxdepth {depth} -printf {RED}%-20M{RESET}%-10u%-10g{BLUE}%-10p{RESET}\\n'.split()
    else :
        if exclude != None:
            cmd1 = f'find . -not -path {exclude} -printf {RED}%-20M{RESET}%-10u%-10g{BLUE}%-10p{RESET}\\n'.split()
            cmd2 = f'find . -not -path {exclude} -printf {RED}%-20M{RESET}%-10u%-10g{BLUE}%-10p{RESET}\\n'.split()
        else:
            cmd1 = f'find . -printf {RED}%-20M{RESET}%-10u%-10g{BLUE}%-10p{RESET}\\n'.split()
            cmd2 = f'find . -printf {RED}%-20M{RESET}%-10u%-10g{BLUE}%-10p{RESET}\\n'.split()
    perms1 = clean(cdRun(cmd1, dir1))
    perms2 = clean(cdRun(cmd2, dir2))
    arrange(dir1, dir2, perms1, perms2, isPerms, isFileDiffs)

def main():
    parser = argparse.ArgumentParser(description='Compare files including permissions and ownership.')
    parser.add_argument("DIR1", help="First directory to compare.")
    parser.add_argument("DIR2", help="Directory to compare with.")
    parser.add_argument("-p", help="Compare the permissions and the ownership only.", action="store_true")
    parser.add_argument("-f", help="Compare the differences line by line.", action="store_true")
    parser.add_argument("-a", help="Run -p and -d respectively [DEFAULT].", action="store_true", default=True)
    parser.add_argument("-c", "--colorsoff", help="Disable the colors", action="store_true")
    parser.add_argument("-d", "--depth", type=int, help="Specify the depth.")
    parser.add_argument("-e", "--exclude", help="Exclude a particular dir [ACCEPTS WILDCARDS]")
    args = parser.parse_args()
    if args.colorsoff:
        disableColors()
    if args.p != args.f:
        getFilesPerms(args.DIR1, args.DIR2, args.depth, args.exclude, args.p, args.f)
    else :
        getFilesPerms(args.DIR1, args.DIR2, args.depth, args.exclude, 1, 1)

if __name__ == '__main__':
    main()
