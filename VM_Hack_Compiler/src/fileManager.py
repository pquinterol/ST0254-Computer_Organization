

class FileManager:

    def __init__(self):
        self.extns = 'vm'

    def read(self,path):
        
        lines = []
        if(self.isValidExtension(path)):
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
            exit(1)

        return lines

    def write(self,path,lines):
        try:
            name = path.split('.vm')
            name = name[0]+'.asm'
            file = open(name,'w')
            file.writelines(lines)
        except Exception as e:
            print('Error:',e)

    def isValidExtension(self,path):

        extension = path.split('.')[-1]
        if(extension.find(self.extns)!=-1):
            return True
        else:
            return False


