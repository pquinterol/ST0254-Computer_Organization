//Set variable sum to cero
(HOLA)
    @sum
    M=0;
    @base
    D=M
    @ToSum
    M=D
    @i
    M=D-1
    @CHECKCERO
    @HOLA
    0;JMP

(CHECKCERO)

    @ENDONE
    D;JEQ
    @base
    D=M
    @sum
    M=D
    @pow
    M=M-1
    @LOOPONE
    0;JMP

(LOOPONE)
    @pow
    D=M
    @END
    D;JEQ
    @pow
    M=D-1
    @LOOPTWO
    0;JMP

(LOOPTWO)
    @i
    D=M
    @REFILLVAR
    D;JEQ
    @i
    M=D-1
    @ToSum
    D=M
    @sum
    M=D+M
    @LOOPTWO
    0;JMP

(REFILLVAR)
    @base
    D=M
    @i
    M=D-1
    @sum
    D=M
    @ToSum
    M=D
    @LOOPONE
    0;JMP

(ENDONE)
    @sum
    M=1

(END)
    @END
    0;JMP
