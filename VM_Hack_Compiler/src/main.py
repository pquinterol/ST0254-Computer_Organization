
import sys
from fileManager import FileManager
from VMParser import Parser

if __name__ == "__main__":

    files = sys.argv
    files = files[1:]
    fm = FileManager()
    if(len(files) == 0):
        print('At least one .vm file must be passed to the program')
        exit()
    else:
        file_name = ''
        parser = Parser()
        for i in files:
            lines = fm.read(i)
            if(i.find('\\')!=-1):
                file_name = i[i.rfind('\\')+1:i.rfind('.')]
            else:
                file_name = i[:i.rfind('.')]
            trans_lines = parser.parse(lines,file_name)
            for i in trans_lines:
                print(i)
            
            

