#include "fileManager.h"

fileManager::fileManager(const std::string& _filePath):filePath(_filePath){
    parser = new Parser();
}

int fileManager::read(){

    std::ifstream file;
    std::string line;
    int row = 0;
    int exitStatus = 0;

    if(!checkExtension())
    { 
        return -1;
    }

    for(int i = 0; i<2; ++i){

       try
       {
            file.open(filePath,std::ios::in);
            if(file.fail()){
                throw -2;
            }
        }
        catch(int e)
        {
           return e;
        }
    

        while(!file.eof()){

            std::getline(file,line);
            exitStatus = (*parser).parse(line, i, row);
            switch (exitStatus)
            {
            case 0:
                row++;
                break;
            default:
                file.close();
                return exitStatus;
            }

        }
        file.close();
        row = 0; 
    }

    return exitStatus;
}

void fileManager::Write(){

    std::ofstream file;
    std::string name = filePath.substr(0, filePath.find(".asm")) +".hack";
    try
    {
        file.open(name);
        file<<Translator::getBinary();
    }
    catch(const std::exception& e)
    {
        std::cout << "Error Writing to the file" << '\n'<<std::endl;;
    }
    
}

bool fileManager::checkExtension(){

    if(filePath.find(".asm")!=std::string::npos){ return true;}

    return false;

}