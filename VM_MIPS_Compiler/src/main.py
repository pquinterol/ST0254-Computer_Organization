
import sys
from fileManager import FileManager
from VMTranslator import VMTranslator

if __name__ == "__main__":

    files = sys.argv
    files = files[1:]
    fm = FileManager()
    if(len(files) == 0):
        print('At least one .vm file must be passed to the program')
        exit()
    else:
        file_name = ''
        translator = VMTranslator()
        trans_lines = [translator.init_MIPS_ASM()]
        print(files[0])
        fm.write(files[0],trans_lines)
        for i in files:
            lines = fm.read(i)
            if(i.find('\\')!=-1):
                file_name = i[i.rfind('\\')+1:i.rfind('.')]
            else:
                file_name = i[:i.rfind('.')]
            trans_lines.append(translator.translate(lines,file_name))

        fm.write(files[0],trans_lines)
            
            

