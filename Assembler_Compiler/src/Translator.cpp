#include "Translator.h"

std::string Translator::binary = "";

void Translator::translateAInst(const int& toBinary){

    if(binary.empty()) binary = "";  
    binary+="0"+std::bitset<15>(toBinary).to_string()+"\n";
}

void Translator::addCInstr(const std::string& fromOpeTable){

    if(binary.empty()) binary = "";
    binary+="111"+fromOpeTable+"\n";
}

std::string& Translator::getBinary(){
    if(binary.empty()) binary = "";
    return binary;
}