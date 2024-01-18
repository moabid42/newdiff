import subprocess
import argparse
import sys
import os

PURPLE = '\033[94m'
GRAY = '\033[97m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[00m'

def disableColors():
    global PURPLE
    global GRAY
    global RED
    global GREEN
    global YELLOW
    PURPLE = RESET
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

def run(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    return stdout.split('---')

def trimElems(Permslist, dirRoot):
    return [item for item in Permslist if dirRoot not in item]

def clean(arr):
    arr.pop()
    return arr

def arrange(perms1, perms2):
    flag = False
    for elem in perms1:
        print(YELLOW + '===========================================' + RESET)
        print(elem)
        for item in perms2:
            if elem.split()[3] == item.split()[3]:
                print(item)
                print(YELLOW + '===========================================' + RESET)   
                break
            elif item == perms2[-1]:
                flag = True
        if flag == True:
            print('not found')
            print(YELLOW + '===========================================' + RESET)
            flag = False
    print('\n\n')

def getFilesPerms(dir1, dir2, depth, exclude):
    print(GREEN + 'Comparing file permissions ...' + RESET)
    if depth != None:
        if exclude != None:
            cmd1 = f'find . -maxdepth {depth} -not -path {exclude} -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
            cmd2 = f'find . -maxdepth {depth} -not -path {exclude} -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
        else:
            cmd1 = f'find . -maxdepth {depth} -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
            cmd2 = f'find . -maxdepth {depth} -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
    else :
        if exclude != None:
            cmd1 = f'find . -not -path {exclude} -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
            cmd2 = f'find . -not -path {exclude} -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
        else:
            cmd1 = f'find . -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
            cmd2 = f'find . -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
    perms1 = clean(cdRun(cmd1, dir1))
    perms2 = clean(cdRun(cmd2, dir2))
    arrange(perms1, perms2)

def adjustdepth(diffs, depth):
    for elems in diffs:
        if elems == '':
            continue
        (firstWord, *_) = elems.split(maxsplit=1)
        if depth != None and len(firstWord.split('/')) > (depth + 1):
            continue
        print(YELLOW + '===========================================' + RESET)
        lst = elems.split('\n')
        print(RED + '---' + RESET, end='')
        for line in lst:
            if line == '':
                break 
            elif line[:3] == '+++':
                print(GREEN + '+++' + RESET + PURPLE + line[3:] + RESET)
            elif line[0] == '+':
                print(GREEN + line + RESET)
            elif line[0] == '-':
                print(RED + line + RESET)
            else :
                print(line)
        print(YELLOW + '===========================================' + RESET)

def getDiffs(dir1, dir2, depth, exclude):
    print(GREEN + 'Comparing the content of the files ...' + RESET)
    if exclude != None:
        cmd = f'diff -Naur {dir1} {dir2} -x {exclude} | grep -v "diff\|@"'
    else:
        cmd = f'diff -Naur {dir1} {dir2} | grep -v "diff\|@"'
    diffs_str = run(cmd)
    adjustdepth(diffs_str, depth)

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
    if args.p:
        getFilesPerms(args.DIR1, args.DIR2, args.depth, args.exclude)
    elif args.f:
        getDiffs(args.DIR1, args.DIR2, args.depth, args.exclude)
    else:
        getFilesPerms(args.DIR1, args.DIR2, args.depth, args.exclude)
        getDiffs(args.DIR1, args.DIR2, args.depth, args.exclude)

if __name__ == '__main__':
    main()
