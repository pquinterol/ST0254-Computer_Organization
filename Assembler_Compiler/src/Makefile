
output: main.o fileManager.o Parser.o Translator.o
	g++ -o Assembler main.o fileManager.o Parser.o Translator.o

main.o: main.cpp
	g++ -c main.cpp
fileManager.o: fileManager.h fileManager.cpp
	g++ -c fileManager.cpp fileManager.h
Parser.o: Parser.h Parser.cpp
	g++ -c Parser.cpp Parser.h
Translator.o: Translator.h Translator.cpp
	g++ -c Translator.cpp Translator.h
clean:
	rm *.o Assembler