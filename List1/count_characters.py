import sys

from common import set_up_streams, run_safely, get_safe_char_stream

#mozna dodac rzucanie wyjaktu jesli nie ma wejscia
def countCharacters():
    set_up_streams()

    totalCharacters = calculateCharactersCount()

    print(totalCharacters)

def calculateCharactersCount():
     characterCounter = 0

     for c in get_safe_char_stream():
         if not c.isspace():
             characterCounter += 1

     return characterCounter

if __name__ == "__main__":
    run_safely(countCharacters)