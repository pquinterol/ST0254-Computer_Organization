


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
        self.return_addrss=0

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
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M'
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
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M'
        elif(commad == 'or'):
            trans = '@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M'
        else:                                           #Not command
            trans = '@SP\nAM=M-1\nM=!M'
        
        return trans
            
    def branch_c_translate(self,command,etiq,file_name):
        trans = ''
        if(command == 'label'):
            trans = f"({file_name.upper()}.{etiq.upper()})"
        elif(command == 'goto'):
            trans = f"@{file_name.upper()}.{etiq.upper())}\n0;JMP"
        else:                                          #if-goto command
            trans = f"@SP\nAM=M-1\nD=M\n@{file_name.upper()}.{etiq.upper()}\nD;JNE"

        return trans

    def push_pop_c_translate(self,command, segment, number,file_name):
        trans = ''
        if(command == 'push'):
            if(segment=='local'or segment=='argument'or segment=='this' or segment=='that'):
                trans=f"@{number}\nD=A\n@{self.hack_mem_segments[segment]}\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='constant'):
                trans=f"@{number}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='static'):
                trans=f"@{file_name}.{number}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='temp'):
                trans=f"@{number}\nD=A\n@{self.temp}\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif(segment=='pointer'):
                if(int(number)==0):
                    trans=f"@{number}\nD=A\n@{self.this}\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
                else:
                    trans=f"@{number}\nD=A\n@{self.that}\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

        else:
            if(segment=='local' or segment=='argument' or segment=='this' or segment=='that'):
                trans=f"@{number}\nD=A\n@{self.hack_mem_segments[segment]}\nD=D+M\n@value\nM=D\n@SP\nAM=M-1\nD=M\n@value\nM=D"
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
        
    def funct_c_translate(self,commad,funct_name,num_args):

        trans = ''
        if(commad=='call'):
            #
            funct_ref = f"{funct_name.upper()}RETURN{self.return_addrss}"
            self.return_addrss+=1
            trans = self.callPushAddrss()+
                    self.callPushLCL_ARG_THIS_THAT('LCL')+self.callPushLCL_ARG_THIS_THAT('ARG')+
                    self.callPushLCL_ARG_THIS_THAT('THIS')+self.callPushLCL_ARG_THIS_THAT('THAT')+
                    self.callSetARG(num_args)+
                    

        elif(command=='function'):
        else:
    
    def callPushAddrss():
        return 'D=A\n@SP\nA=M\nM=D\@SP\nM=M+1\n'
    def callPushLCL_ARG_THIS_THAT(segment):
        return f"@{segment}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    def callSetARG(num_args):
        steps_back = int(num_args) + 5
        return f"@SP\nD=M\n@{steps_back}\nD=D-A\n@ARG\nM=D\n"
    def callSetLCL()
    


        