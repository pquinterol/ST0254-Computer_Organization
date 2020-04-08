#include<string>
#include<bitset>

class Translator {
    private:
    static std::string binary;

    public:
    Translator() = delete;
    static void translateAInst(const int& toBinary);
    static void addCInstr(const std::string& fromOpTable);
    static std::string& getBinary();
};