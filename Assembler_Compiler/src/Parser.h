#include<string>
#include<map>
#include<iostream>
#include<bitset>
#include"Translator.h"

class Parser{

    private:
    std::map<std::string, int> instSymbolTable;              //Symbol table for instructions in the ROM
    std::map<std::string,std::string> destTable;
    std::map<std::string,std::string> compTable; 
    std::map<std::string,std::string> jmpTable;
    int varRegis;
    //Translator translator;

    int parseSymbol(const std::string& line, int& row);
    int parseCommands(const std::string& line);
    int parseAInstruction(const std::string& line);
    int parseCInstruction(const std::string& line);
    bool checkSymStx (const std::string& name);
    int checkVarStx(const std::string& name);
    int saveVar(const std::string& name);
    bool inAsciiNumRange(const char& c);
    bool inAsciiLetterRange(const char& c);
    bool isNotWhiteSpace(const char& c);
    bool isSpecialChar(const char& c);
    std::pair<std::string,int> getDestCode(const std::string& dest);
    std::pair<std::string,int> getCompCode(const std::string& comp);
    std::pair<std::string,int> getJMPCode(const std::string& jmp);
    bool isOperChar(const char& c);


    public:
    Parser();
    ~Parser();
    int parse(const std::string& line, unsigned int task,int& row);
};