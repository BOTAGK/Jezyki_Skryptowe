import sys
from common import set_up_Streams, run_safely

#mozna dodac rzucanie wyjaktu jesli nie ma wejscia
def countCharacters():
    set_up_Streams()

    characterCounter = 0

    while c := sys.stdin.read(1):
        if not c.isspace():
            characterCounter += 1

    print(characterCounter)

if __name__ == "__main__":
    run_safely(countCharacters)