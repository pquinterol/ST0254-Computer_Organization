

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
                file.close()
            
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
            if(path.find("\\")!=-1):
                name = path[:path.rfind("\\")+1]+'translation.asm'
            else:
                name = 'translation.asm'
            file = open(name,'w')
            for i in lines:
                #print(i)
                #print(type(i))
                for j in i:
                    file.write(j)
            file.close()
        except Exception as e:
            print('Here')
            print('Error:',e)

    def isValidExtension(self,path):

        extension = path.split('.')[-1]
        if(extension.find(self.extns)!=-1):
            return True
        else:
            return False


