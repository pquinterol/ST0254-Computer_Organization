


class VMTranslator:

    arith_logic_commads = ['add','sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    binary_commands = {'add': 'add','sub': 'sub', 'eq':'seq', 'gt':'sgt', 'lt':'slt', 'and':'and', 'or':'or'}
    unary_commands = {'not':'not', 'neg':'negu'}

    branch_commads = ['goto','if-goto','label']
    insert_del_commands = ['push','pop']
    funct_commands = ['function','call','return']

    mem_segments = {'local':'$t0', 'argument':'$t1', 'this':'$t2', 'that':'$t3', 'temp': '$t4', 'constant':None, 'static': '$t5', 'pointer': '$t6'}
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

    def translate(self,lines,file_name):

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
                    trans_lines.append(self.branch_c_translate(command,i[1],file_name))
                elif(command_type == 3):
                    #push_pop
                    trans_lines.append(self.push_pop_c_translate(command,i[1],i[2],file_name))

                else:
                    #funct
                    self.funct_c_translate(command,i[1],i[2])
        return trans_lines

    def init_MIPS_ASM(self):
        commands = ''
        commands+=('move $t0,$sp\n')   #LOCAL
        commands+=('subiu $sp,$sp,4\n')
        commands+=('move $t1,$sp\n')   #ARGUMENT
        commands+=('subiu $sp,$sp,4\n')
        commands+=('move $t2,$sp\n')   #THIS
        commands+=('subiu $sp,$sp,4\n')
        commands+=('move $t3,$sp\n')   #THAT
        commands+=('subiu $sp,$sp,4\n')
        commands+=('move $t4,$sp\n')   #TEMP
        commands+=('subiu $sp,$sp,32\n')
        commands+=('move $t5,$sp\n')   #STATIC
        commands+=('subiu $sp,$sp,952\n')
        commands+=('move $t6,$sp\n')   #POINTER
        commands+=('subiu $sp,$sp,12\n')
        return commands   

    def arith_c_translate(self,command):
        trans = ''
        if(command in self.binary_commands.keys()):
            lines = self.getBinaryCommands(command)
            for i in lines:
                trans+=i
        else:
            lines = self.getUnaryCommands(command)
            for i in lines:
                trans+=i

        return trans
            
    def branch_c_translate(self,command,etiq,file_name):
        trans = ''
        if(command == 'label'):
            trans += f"{file_name}_{etiq})"
        elif(command == 'goto'):
            trans += f"j {file_name}_{etiq}\n"
        else:                                          #if-goto command
            trans+= 'addiu $sp,$sp,4\n'
            trans+= 'lw $t8,0($sp)\n'
            trans+= f"bge $t8,1,{file_name}_{etiq}\n"

        return trans

    def push_pop_c_translate(self,command, segment, number,file_name):
        trans = ''
        if(command == 'push'):
            if segment=='argument' or segment=='local': 
                trans+=f"lw $t8,'{str(int(number)*-4)}({self.mem_segments[segment]})\n"
                trans+='sw $t8,0($sp)\n'                   #check
                trans+='subiu $sp,$sp,4\n'
            elif segment == 'constant':
                trans+=f"li $t8,{number}\n"
                trans+='sw $t8,0($sp)\n'
                trans+='subiu $sp,$sp,4\n'
            else:
                trans+=f"lw $t8,{str(int(number)*4)}({self.mem_segments[segment]})\n"
                trans+='sw $t8,0($sp)\n'
                trans+='subiu $sp,$sp,4\n'

        else:
            if segment=='argument' or segment=='local': 
                trans+='addiu $sp,$sp,4\n'
                trans+='lw $t7,0($sp)\n'
                trans+=f"sw $t7,{str(int(number)*-4)}({self.mem_segments[segment]})\n"
            else:
                trans+='addiu $sp,$sp,4\n'
                trans+='lw $t8,0($sp)\n'
                trans+=f"sw $t8,{str(int(number)*4)}({self.mem_segments[segment]})\n"
        
        return trans
        
    def funct_c_translate(self,command,funct_name,num_args_vars):

        trans = ''
        if(command=='call'):
            #
            self.return_addrss+=1
            push_mem_segments = self.callPushLCL_ARG_THIS_THAT('LCL')+self.callPushLCL_ARG_THIS_THAT('ARG')+self.callPushLCL_ARG_THIS_THAT('THIS')+self.callPushLCL_ARG_THIS_THAT('THAT')
            trans = self.callPushAddrss(funct_name) + push_mem_segments + self.callSetARG(num_args_vars) + self.callSetLCL() + self.callGotoFunc(funct_name)
            self.return_addrss+=1
            return trans 

        elif(command=='function'):
            return self.funct_trans_commands(funct_name,num_args_vars)
        else:
            lines = self.return_trans_commands()
            for i in lines:
                trans+=i+'\n'
            return trans

    def funct_trans_commands(self,funct_name,num_vars):
        trans = ''
        trans+=('\n#function start\n')
        trans+= f"{funct_name}:\n"
        trans+='   li $t8,0\n'
        for i in range(int(num_vars)):
            trans+='   subi $sp,$sp,4\n'
            trans+='   sw $t8,0($sp)\n'
        return trans
    
    def return_trans_commands(self):

        commands = []
        commands+='move $t8,$t0\n' # endFrame is stored in t8
        commands+='addiu $t7,$t8,20\n'# the return address is stored in t7
        commands+='lw $t7,0($t8)\n'

        commands+='add $sp,$sp,4\n'
        commands+='lw $t9,0($sp)\n' 
        commands+='sw $t9,0($t1)\n' # ARG = pop (?)

        commands+='subiu $sp,$t1,4\n' #SP = ARG + 1
        commands+='addiu $t3,$t8,4\n' #THAT = endFrame-1T

        commands+='addiu $t2,$t8,8\n' #THIS = endFrame-2
        commands+='addiu $t1,$t8,12\n' #ARG = endFrame-3
        commands+='addiu $t0,$t8,16\n' #LCL = endFrame-4
        commands+='jr $t7\n' #jump to the return address

        return commands

    def getBinaryCommands(self,command):
        lines = []
        lines.append('addiu $sp,$sp,4\n')
        lines.append('lw $t8,0($sp)\n')
        lines.append('addiu $sp,$sp,4\n')
        lines.append('lw $t9,0($sp)\n')
        lines.append(f"{self.binary_commands[command]} $t8,$t8,$t7\n")
        lines.append('sw $t9,0($sp)\n')
        lines.append('subiu $sp,$sp,4\n')
        return lines

    def getUnaryCommands(self,command):
        lines = []
        lines.append('addiu $sp,$sp,4\n')
        lines.append('lw $t9,0($sp)\n')
        lines.append(f"{self.unary_commands[command]} $t8,$t8\n")
        lines.append('sw $t9,0($sp)\n')
        lines.append('subiu $sp,$sp,4\n')
        return lines
    
    def get_comm_type(self,command):
        if(command in self.arith_logic_commads):
            return 1
        elif(command in self.branch_commads):
            return 2
        elif (command in self.insert_del_commands):
            return 3
        elif (command in self.funct_commands):
            return 4
    

    def callPushAddrss(self,funct_name):
        trans=f"{funct_name}RETURN{self.return_addrss}:\n"
        trans+='  sw $t10($sp)\n'                       
        trans+='  sub $sp,$sp,4\n'
        return trans

    def callPushLCL_ARG_THIS_THAT(self,segment):
        trans = ''
        trans+=f"  sw ${self.mem_segments[segment]},0($sp)\n"
        trans+="  sub $sp,$sp,4\n"
        return trans

    #ARG = SP - 5 - numArgs
    def callSetARG(self,num_args):
        steps_back_MIPS=(int(num_of_args)*4)+20       #MIPS architecture equivalent
        return f"  subiu $t1,$sp,{steps_back_MIPS}\n"

    def callSetLCL(self):
        return '  move $t0,$sp\n'

    def callGotoFunc(self,funct_name):
        return f"  j {funct_name}_{self.return_addrss}\n"

        