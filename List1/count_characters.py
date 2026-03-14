import sys

from List1.common import get_safe_char_stream
from common import set_up_Streams, run_safely

#mozna dodac rzucanie wyjaktu jesli nie ma wejscia
def countCharacters():
    set_up_Streams()

    characterCounter = 0

    for c in get_safe_char_stream():
        if not c.isspace():
            characterCounter += 1

    print(characterCounter)

if __name__ == "__main__":
    run_safely(countCharacters)