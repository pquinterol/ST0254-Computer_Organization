
import sys
from fileManager import FileManger as fm

if __name__ == "__main__":

    files = sys.argv
    if(len(files) == 0):
        print('At least one .vm file must be passed to the program')
        exit()
    else:
        for i in files:
            lines = fm.read(i)

