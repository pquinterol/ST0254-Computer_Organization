#include<iostream>
#include<fstream>
#include<cstdlib>
#include<string>
#include"Parser.h"

class fileManager{

    private:

    const std::string& filePath;
    Parser* parser;

    public:
    fileManager(const std::string& _filePath);
    ~fileManager();
    int read();
    void Write();
    bool checkExtension();

};