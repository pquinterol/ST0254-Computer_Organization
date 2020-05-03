
import sys
from fileManager import FileManger

if __name__ == "__main__":

    files = sys.argv
    files = files[1:]
    fm = FileManger()
    if(len(files) == 0):
        print('At least one .vm file must be passed to the program')
        exit()
    else:
        for i in files:
            lines = fm.read(i)

