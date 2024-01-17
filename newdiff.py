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

def getPermsOf(Permslist, dirRoot):
    return [item for item in Permslist if dirRoot in item]

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

def getFilesPerms(dir1, dir2):
    print(GREEN + 'Comparing file permissions ...' + RESET)
    cmd = f'find . -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
    perms1 = clean(cdRun(cmd, dir1))
    cmd = f'find . -printf {RED}%-20M{RESET}%-10u%-10g{PURPLE}%-10p{RESET}\\n'.split()
    perms2 = clean(cdRun(cmd, dir2))
    arrange(perms1, perms2)


def getDiffs(dir1, dir2):
    print(GREEN + 'Comparing the content of the files ...' + RESET)
    cmd = f'diff -Naur {dir1} {dir2} | grep -v diff'
    diffs_str = run(cmd)
    print(*diffs_str, sep=YELLOW + '\n===========================================\n' + RESET)

def main():
    parser = argparse.ArgumentParser(description='Compare files including permissions and ownership.')
    parser.add_argument("DIR1", help="First directory to compare.")
    parser.add_argument("DIR2", help="Directory to compare with.")
    parser.add_argument("-p", help="Compare the permissions and the ownership only.", action="store_true")
    parser.add_argument("-d", help="Compare the differences line by line.", action="store_true")
    parser.add_argument("-a", help="Run -p and -d respectively [DEFAULT].", action="store_true", default=True)
    args = parser.parse_args()
    if args.p:
        getFilesPerms(args.DIR1, args.DIR2)
    elif args.d:
        getDiffs(args.DIR1, args.DIR2)
    else:
        getFilesPerms(args.DIR1, args.DIR2)
        getDiffs(args.DIR1, args.DIR2)

if __name__ == '__main__':
    main()
