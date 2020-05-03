


class Parser:

    arith_logic_commads = ['add','sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    branch_commads = ['goto','if-goto','label']
    insert_del_commands = ['push','pop']
    funct_commands = ['function','call','return']
    mem_segments = ['local','argument','constant','pointer','temp','this','that','static']
    hack_mem_segments = {'local':'LCL','argument':'ARG','this':'THIS','that':'THAT'}

    def __init__(self):
        #
        self.sp = 256
        self.lcl = 1
        self.arg = 2
        self.this = 3
        self.that = 4
        self.temp = 5
        self.static = 16

    def parse(self,lines,file_name):

        trans_lines=[]

        for i in lines:

            if(len(i)>0):
                command = i[0]
                command_type = self.get_comm_type(command)
                if(command_type == 1):
                    #arithmetic
                    trans_lines.append(self.arith_c_translate(command))
                elif(command_type == 2):
                    #branch
                    trans_lines.append(self.branch_c_translate(command))
                elif(command_type == 3):
                    #push_pop
                    trans_lines.append(self.push_pop_c_translate(command,i[1],i[2],file_name))

                else:
                    #funct
                    self.funct_c_translate(command,i[1],i[2])
        return trans_lines


    '''
    Need to add the (EXIT) label
    '''
    def arith_c_translate(self,commad):
        trans = ''
        if(commad == 'add'):
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D'
        elif(command == 'sub'):
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D'
        elif(commad == 'neg'):
            trans = '@SP\nA=M-1\nM=!M'
        elif(commad == 'eq'):
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@EXIT\nD;JEQ\n@SP\nA=M-1\nM=0'
        elif(command == 'gt'):
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@EXIT\nD;JGT\n@SP\nA=M-1\nM=0'
        elif(commad == 'lt'):
            trans ='@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@EXIT\nD;JLT\n@SP\nA=M-1\nM=0'
        elif(commad == 'and'):
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D'
        elif(commad == 'or'):
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D'
        else:                                           #Not command
            trans = '@SP\nAM=M-1\nM=!M'
        
        return trans
            
    def branch_c_translate(self,command,etiq):
        trans = ''
        if(command == 'label'):
            trans = f"({etiq})"
        elif(command == 'goto'):
            trans = f"@{etiq}\n0;JMP"
        else:                                          #if-goto command
            trans = f"@SP\nAM=M-1\nD=M\@{etiq}\nD;JNE"

        return trans

    def push_pop_c_translate(self,command, segment, number,file_name):
        trans = ''
        if(command == 'push'):
            if(segment=='local'or segment=='argument'or segment=='this' or segment=='that'):
                trans=f"@{number}\nD=A\n@{self.hack_mem_segments[segment]}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='constant'):
                trans=f"@{number}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='static'):
                trans=f"@{file_name}.{number}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='temp'):
                trans=f"@{number}\nD=A\n@{self.temp}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='pointer'):
                if(int(number)==0):
                    trans=f"@{number}\nD=A\n@{self.this}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
                else:
                    trans=f"@{number}\nD=A\n@{self.that}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

        else:
            if(segment=='local' or segment=='argument' or segment=='this' or segment=='that'):
                trans=f"@{number}\nD=A\n@{self.hack_mem_segments[segment]}\nD=M+D\n@value\nM=D\n@SP\nAM=M-1\nD=M\n@value\nM=D"
            elif(segment=='static'):
                trans=f"@SP\nAM=M-1\nD=M\n@{file_name}.{number}\nM=D"
            elif(segment=='temp'):
                trans=f"@SP\nAM=M-1\nD=M\n@{self.temp+int(number)}\nM=D"
            elif(segment=='pointer'):
                if(int(number)==0):
                    trans=f"@SP\nAM=M-1\nD=M\n@{self.this}\nM=D"
                else:
                    trans=f"@SP\nAM=M-1\nD=M\n@{self.that}\nM=D"
        
        return trans
    
    def get_comm_type(self,command):
        if(command in self.arith_logic_commads):
            return 1
        elif(command in self.branch_commads):
            return 2
        elif (command in self.insert_del_commands):
            return 3
        elif (command in self.funct_commands):
            return 4
        


'''
    def funct_c_translate(self,commad,segment,num_vars):

        if(commad=='call'):
            #
        elif(command=='function'):
        else:
'''

        