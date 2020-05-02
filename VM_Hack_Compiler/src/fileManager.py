

class FileManger:

    def __init__(self):
        self.extns = ['vm']
    
    def read(path):
        
        lines = []
        if(isValidExtension(path)):
            try:
                file = open(path, 'r')
                for i in file.readlines():
                    lines.append(i.strip().split())
            
            except FileNotFoundError as e:
                print("The file has not been found",e)
            except Exception as e:
                print('Error:',e)
        else:
            print("Invalid file extension\n","Note: Files must have .vm extension")

        return lines

    def write(path,lines):
        try:
            name = path.split('.vm')
            name = name[0]+'.asm'
            file = open(name,'w')
            file.writelines(lines)
        except Exception as e:
            print('Error:',e)


    def isValidExtension(self,path):

        try:
            extension = path.split('.')[-1]
            self.extns.index(extension)
            return True
        except Exception:
            return False


