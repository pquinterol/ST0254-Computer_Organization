
//#include<stdio.h>
#include<iostream>
#include<cstring>
#include"fileManager.h"

int errorOutput(int argcNum, const std::string& fileName, int exitStatus);

int main(int argc, char const *argv[])
{
    int exitStatus = 0;
    if(argc == 1){
        std::cout<<"Error.No arguments passed.No asm file to compile"<<std::endl;
    }else
    {
        for (int i = 1; i < argc; i++)
        {
            //std::cout<<argv[i]<<std::endl;
            fileManager* fileM = new fileManager(argv[i]);
            exitStatus = (*fileM).read();
            exitStatus = errorOutput(i,argv[i],exitStatus);
            if(exitStatus==0)
            {
                (*fileM).Write();
            }

        }
        
    }
    //system("pause");
    
    return exitStatus;
}

int errorOutput(int argcNum, const std::string& fileName, int exitStatus)
{
    int progExitStat = 1;
    switch (exitStatus)
    {
    case -1:
        std::cout<<"Invalid file. Not (.asm) found in the given file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -2:
        std::cout<<"An error happened trying to open the file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -3:
        std::cout<<"Syntax error due to invalid symbol name in file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -4:
        std::cout<<"Syntax error in a symbol declaration due to invalid characters outside of the parenthesis or an invalid use of them in file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -5:
        std::cout<<"Syntax error in a variable declaration due to chars reserved for C instructions in file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -6:
        std::cout<<"Syntax error in a variable declaration due to characters before the '@' char in file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -7:
        std::cout<<"Syntax error in a variable declaration due to an invalid combination of numbers and letters (R.E = l+n | n+ ) in file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -8:
        std::cout<<"Syntax error in a variable declaration due to white spaces between the variable name characters in file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -9:
        std::cout<<"Syntax error in a C instruction parsing due to invalid use or ausence of the '=' and ';' chars in file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    case -10:
        std::cout<<"Syntax error in a C instruction parsing due to invalid dest, comp or jmp command(s) in file number :"<<argcNum<<" with name: "<<fileName<<"\n"<<std::endl;
        break;
    default:
        progExitStat = 0;
        break;
    }

    return progExitStat;
}
