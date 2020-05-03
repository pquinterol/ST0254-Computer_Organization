


class Parser:

    arith_logic_commads = ['add','sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    branch_commads = ['goto','if-goto','label']
    insert_del_commands = ['push','pop']
    funct_commands = ['function','call','return']
    mem_segments = {'local':'LCL','argument':'ARG','constant':'CONST','pointer':,'temp','this','that','static'}

    def __init__(self):
        #
        self.sp = 256
        self.lcl = 1
        self.arg = 2
        self.this = 3
        self.that = 4
        self.temp = 5
        self.static = 16

    def parse(self,lines):

        trans_lines=[]

        for i in lines:

            if(len(i)>0):
                command = i[0]
                command_type = self.get_comm_type(command)
                if(command_type == 1):
                    #arithmetic
                    trans_lines.append(self.artih_c_translate(command))
                elif(command_type == 2):
                    #branch
                    trans_lines.append(self.branch_c_translate(command))
                elif(command_type == 3):
                    #push_pop

                else:
                    #funct
                    self.funct_c_translate(command,i[1],i[2])


    '''
    Need to add the exit label
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

    def push_pop_c_translate(self,command, segment, number):
        trans = ''
        if(command == 'push'):
            if(segment=='constant'):
                trans=f"@{number}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='static'):
                trans=f"@{number}\nD=A\n@{self.static}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='temp'):
                trans=f"@{number}\nD=A\n@{self.temp}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='local'):
                trans=f"@{number}\nD=A\n@{self.lcl}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='argument'):
                trans=f"@{number}\nD=A\n@{self.arg}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='this'):
                trans=f"@{number}\nD=A\n@{self.this}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='that'):
                trans=f"@{number}\nD=A\n@{self.that}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='pointer'):
                if(int(number)==0):
                    trans=f"@{number}\nD=A\n@{self.this}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
                else:
                    trans=f"@{number}\nD=A\n@{self.that}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

        else:
            if(segment=='local'):
                trans=f"@{number}\nD=A\n@{self.lcl}\n@A=M+D\n"
            elif(segment=='static'):
                trans=f"@{number}\nD=A\n@{self.lcl}\n@A=M+D\n"


                





    def funct_c_translate(self,commad,segment,num_vars):


    def get_comm_type(self,commad):
        if(i in arith_logic_commads):
            return 1
        elif(i in branch_commads):
            return 2
        elif (i in insert_del_commands):
            return 3
        elif (i in funct_commands):
            return 4
        

        