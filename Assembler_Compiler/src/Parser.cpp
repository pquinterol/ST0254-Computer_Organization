#include "Parser.h"

Parser::Parser(){
    
    varRegis = 16;

    //Initialize the instruction symbol table with the deafault symbols.
    for(int i = 0; i<16; ++i)
    {
        instSymbolTable[(std::string)"R"+std::to_string(i)] = i;
    }

    instSymbolTable["SP"] = 0;
    instSymbolTable["LCL"] = 1;
    instSymbolTable["ARG"] = 2;
    instSymbolTable["THIS"] = 3;
    instSymbolTable["THAT"] = 4;
    instSymbolTable["SCREEN"] = 16384;
    instSymbolTable["KBD"] = 24576;

    //Initialize the tables containing the binary representation of each C instrucion component (dest,comp and jmp)

    //Initialize the destination table.
    destTable["null"] = "000";
    destTable["M"] = "001";
    destTable["D"] = "010";
    destTable["MD"] = "011";
    destTable["A"] = "100";
    destTable["AM"] = "101";
    destTable["AD"] = "110";
    destTable["AMD"] = "111";

    //Initialize the computation table
    compTable["0"] = "101010";
    compTable["1"] = "111111";
    compTable["-1"] = "111010";
    compTable["D"] = "001100";
    compTable["A"] = "110000";
    compTable["!D"] = "001101";
    compTable["!A"] = "110001";
    compTable["-D"] = "001111";
    compTable["-A"] = "110011";
    compTable["D+1"] = "011111";
    compTable["A+1"] = "110111";
    compTable["D-1"] = "001110";
    compTable["A-1"] = "110010";
    compTable["D+A"] = "000010";
    compTable["D-A"] = "010011";
    compTable["A-D"] = "000111";
    compTable["D&A"] = "000000";
    compTable["D|A"] = "010101";

    //Comptation commands for operations involving 'M'
    compTable["M"] = "110000";
    compTable["!M"] = "110001";
    compTable["-M"] = "110011";
    compTable["M+1"] = "110111";
    compTable["M-1"] = "110010";
    compTable["D+M"] = "000010";
    compTable["D-M"] = "010011";
    compTable["M-D"] = "000111";
    compTable["D&M"] = "000000";
    compTable["D|M"] = "010101";

    //Initialize the jump commands table
    jmpTable["null"] = "000";
    jmpTable["JGT"] = "001";
    jmpTable["JEQ"] = "010";
    jmpTable["JGE"] = "011";
    jmpTable["JLT"] = "100";
    jmpTable["JNE"] = "101";
    jmpTable["JLE"] = "110";
    jmpTable["JMP"] = "111";
}

int Parser::parse(const std::string& line, unsigned int task,int& row){

    int exitStatus = 0;;

    switch (task)
    {
    case 0:
        exitStatus = parseSymbol(line,row);
        break;
    
    case 1:
        exitStatus = parseCommands(line);
    default:
        break;
    }

    return exitStatus; 

}

/**
 * Method used to parse symbols of the asm language.
 * this method return a number that can take 0,-3 or -4 as values
 * 0 implies a succesfull parsing process
 * 0 implies that the given line is not a symbol declaration.Therefore,ParserCommand is responsable for the validation of this line
 * -3 implies a syntax error due to invalid characters in the symbol name (Ends the program)
 * -4 implies a syntax error due to invalid characters outside of the parenthesis or an invalid use of them (Ends the program)
*/
int Parser::parseSymbol(const std::string& line,int& row){

    int leftIndex = -1;
    int rightIndex = -1;
    int errorCode = 0;
    int invalidChar = 0;
    bool whiteSpaceL = true;
    std::string symbolName = "";

    if(line.empty())
    {
        row--;
        return errorCode;
    }

    for(int i = 0; i < line.length(); ++i)
    {
        if(line.at(i) == '(')
        {
            leftIndex = i;
        }
        else if(line.at(i) == ')')
        {
            rightIndex = i;
        }
        else if((i+1<line.length()) && line.at(i) == '/' && line.at(i+1)=='/')               //Check for comments
        {
           if(leftIndex+rightIndex == -2 && !invalidChar)                                    //Checks if the entire line is a comment
           {
               row--;
               return 0;
           }
           break;
           
        }
        else
        {
           if(line.at(i)!=32 && line.at(i)!='\t' && line.at(i)!='\r' && line.at(i)!='\n' && line.at(i)!=11)                       //Checks if the letter is not a white space, in which case it will be an invalid character
           {
              invalidChar++;
              if(invalidChar == 1) whiteSpaceL = false;
           }
        }
        
    }
    invalidChar-=(rightIndex-1-leftIndex);

    if(leftIndex>=0 && rightIndex>leftIndex+1 && invalidChar==0){
        symbolName = line.substr(leftIndex + 1,(rightIndex-1) - leftIndex);

        if(checkSymStx(symbolName))
        {
            instSymbolTable.insert(std::pair<std::string, int>(symbolName, row));
            row--;
            errorCode = 0;
        }
        else
        {
            errorCode = -3;
        }

    }
    else
    {
       if(invalidChar && !whiteSpaceL && (leftIndex+rightIndex == -2))
       {
          errorCode = 0;             //Can be 0
       }
       else if(whiteSpaceL && (leftIndex+rightIndex == -2)){                       //Check if this line is empty
           errorCode = 0;
           row--;
       }
      else
      {
          errorCode = -4;
      }
    }

    return errorCode;

}

bool Parser::checkSymStx(const std::string& symbolName){
    char c;
    bool hasValidLet = false;
    for (int i = 0; i < symbolName.length(); ++i)
    {
        c = symbolName.at(i);

        if(i == 0 && inAsciiNumRange(c))
        {
            break;
        }
        else if(isSpecialChar(c) || inAsciiLetterRange(c) || inAsciiNumRange(c))
        {
            hasValidLet = true;
        }
        else
        {
            hasValidLet = false;
            break;
        }
        
        
    }
    return hasValidLet;
    
}
/**
 * This method detects if the given line is an A instruction or a C instruction.
 * 
 * A instruction: returns 0,-5,-6,-7 or -9 depending in the validation error returned while checking the instruction. 0 implies success.
 * If '(' is found: returns 0 given that every line with parenthesis characters is responsability of parseSymbol method.
 * C instruction: returns ----------- 
 */
int Parser::parseCommands(const std::string& line){

    if(line.find('@')!=std::string::npos)
    {
        return parseAInstruction(line);
    }
    else if(line.find('(')!=std::string::npos)
    {
        return 0;
    }
    else
    {
        return parseCInstruction(line);
    }
}


/**
 * This method searchs for invalid characters in the given A instruction. Returning one of the following integers, which represents the error status.
 * returned value from saveVar(0,-7,-8 or -9): this value contains the validation status of the given number or variable name after '@'.
 * -5 implies that charactes which belong to a C Instruction where found.
 * -6 implies that there are characters before the '@'.
 */
int Parser::parseAInstruction(const std::string& line){

    bool foundAt = false;                                                                                   //@
    std::string asmVar = "";
    int exitStatus = 0;

    if(line.find('=')!=std::string::npos || line.find(';')!=std::string::npos) return -5;

    for(int i = 0; i<line.length();++i)
    {
        if(line.at(i)!='@' && isNotWhiteSpace(line.at(i)) && !foundAt)
        {
            return -6;     //Invalid Character in the A instruction
        }
        else if(line.at(i) == '@' && !foundAt)
        {
            foundAt = true;
        }
        else if(foundAt && (inAsciiLetterRange(line.at(i)) || inAsciiNumRange(line.at(i)) || isSpecialChar(line.at(i))))
        {
            asmVar+=line.at(i);
        }
        
    }

    return saveVar(asmVar);
}


/**
 * This method is responsable for saving the declared variable in the instruction symbols table(instSymbolTable)
 * and for passing to Translator, the needed instruction to translate into binary
 * This method depends on checkVatStxs output, which returns an integer representing the validation status of the given number or variable name.
 * Return Values:
 * 0 if the process has been successfull.
 * -7 implies that the given name has a number followed by a string
 * -8 implies that the given name or number contains spaces between its characters
 * -9 if the name or number validation was unsuccessfull  
 */
int Parser::saveVar(const std::string& name){


    switch (checkVarStx(name))
    {
    case 1:
        if(instSymbolTable.find(name)==instSymbolTable.end())
        {
            instSymbolTable.insert(std::pair<std::string, unsigned int>(name, varRegis));
            varRegis++;
        }

        Translator::translateAInst(instSymbolTable.find(name)->second);
        return 0;
    case 2:
        
        Translator::translateAInst(std::stoi(name));
        return 0;

    case -1:
    
        return -7;
    case -2:
        return -8;     
    default:
        return -9;              //Never gonna happen
    }
}

int Parser::checkVarStx(const std::string& name){

    bool num = false;
    bool str = false;
    bool hasSpace = false;
    for(int i = 0; i < name.length(); ++i)
    {
        if(inAsciiNumRange(name.at(i)))
        {
            if(i==0) num=true;
            if(hasSpace) return -2;
        }
        else if (inAsciiLetterRange(name.at(i)))
        {
            if(num) return -1;
            if(hasSpace) return -2;
            str = true;
        }
        else
        {
            
            if((num || str) && !isNotWhiteSpace(name.at(i)))
            {
                
                hasSpace = true;
            }
            else if(i==0 && !isNotWhiteSpace(name.at(i)))
            {
                return -2;
            }
            else return -67;
        }
        
    }

    if(str) return 1;
    return 2;
}

/**
 * This method parses the C instructions.
 * It searchs for '=' and ';' and then do the respectictive division of the dest, comp and jump.
 * Return Values:
 * 0 if the operation was succesfull
 * -9 if the char that follows '=' is ';' or if the appear in an incorrect order.
 * -10 implies an error in the c commands syntax
*/
 int Parser::parseCInstruction(const std::string& line){

     int equalsIndx = line.find('=');
     int semicolIndx = line.find(';');
     std::string dest = "";
     std::string comp = "";
     std::string jmp = "";
     std::string binInstr = "";
     int errorStatus = 0;
     int commentIndx = line.find("//");

     if(commentIndx!=std::string::npos && equalsIndx==std::string::npos && semicolIndx==std::string::npos) return 0;                 //Comment line.
     if(commentIndx==std::string::npos && equalsIndx==std::string::npos && semicolIndx==std::string::npos) return 0;                 //Empty Line. Probably some damn whitespaces waiting to crash the f@$&% program
     if(equalsIndx==std::string::npos) equalsIndx=-1;
     if(semicolIndx==std::string::npos) semicolIndx=-1;


     for(int i = 0; i < line.length(); ++i)
     {
         if (inAsciiLetterRange(line.at(i)) || inAsciiNumRange(line.at(i)) || isOperChar(line.at(i)))
         {
             if(i<equalsIndx)
             {
                 dest+=line.at(i);
             }
             else if(i>equalsIndx && (i<semicolIndx || semicolIndx==std::string::npos))
             {
                 comp+=line.at(i);
             }
             else if(i>semicolIndx && semicolIndx!=std::string::npos)
             {
                 jmp+=line.at(i);
             }
             else return -9;
         }            
     }

     std::pair<std::string,int> destCode = getDestCode(dest);
     std::pair<std::string,int> compCode = getCompCode(comp);
     std::pair<std::string,int> jmpCode = getJMPCode(jmp);

     if(destCode.second || compCode.second || jmpCode.second)
     {
         errorStatus = -10;
     }
     else
     {
         binInstr+= compCode.first + destCode.first + jmpCode.first;
         Translator::addCInstr(binInstr);
     }
     return errorStatus;
}

std::pair<std::string,int> Parser::getDestCode(const std::string& dest){

    std::string toReturn = "";
    int errorCode = 1;
    if(dest.empty())
    {
        toReturn = destTable.find("null")->second;
        errorCode = 0;
    }
    else if (destTable.find(dest)!=destTable.end())
    {
        toReturn = destTable.find(dest)->second;
        errorCode = 0;
    }

    return std::pair<std::string, int>(toReturn,errorCode);  
}

std::pair<std::string,int> Parser::getCompCode(const std::string& comp)
{
    std::string toReturn = "0";
    int errorCode = 1;

    if(comp.empty()) return std::pair<std::string, int>("null",errorCode);
    if(comp.find('M')!=std::string::npos) toReturn = "1";

    if (compTable.find(comp)!=compTable.end())
    {
        toReturn += compTable.find(comp)->second;
        errorCode = 0;
    }

    return std::pair<std::string, int>(toReturn,errorCode);  
}

std::pair<std::string,int> Parser::getJMPCode(const std::string& jmp)
{
    std::string toReturn = "";
    int errorCode = 1;
    if(jmp.empty())
    {
        toReturn = jmpTable.find("null")->second;
        errorCode = 0;
    }
    else if (jmpTable.find(jmp)!=jmpTable.end())
    {
        toReturn = jmpTable.find(jmp)->second;
        errorCode = 0;
    }

    return std::pair<std::string, int>(toReturn,errorCode);  
}


bool Parser::inAsciiNumRange(const char& c){
    return (c>=48 && c<=57);
}

bool Parser::inAsciiLetterRange(const char& c){
    return (c>=65 && c<=90) || (c>=97 && c<=122);
}


bool Parser::isNotWhiteSpace(const char& c){
    return c!=32 && c!='\t' && c!='\r' && c!='\n' && c!=11;
}

bool Parser::isSpecialChar(const char& c){
    return c == '_' || c == '$' || c == ':' || c == '.';
}

bool Parser::isOperChar(const char& c){
    return c=='-' || c=='+' || c=='|' || c=='&';
}
