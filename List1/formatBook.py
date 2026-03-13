import sys

def echo(sentence):
    return "("+sentence+")"


def main(process_sentence):
    setupStreams()
    preamble_buffer = formatPremble()

    sentence = ""
    consecutive_newlines = 0
    dashes_count = 0
    needs_space = False

    def handleCharacters(c):
        nonlocal sentence, consecutive_newlines, dashes_count, needs_space

        if c == '-':
            dashes_count += 1
            if dashes_count >= 5:
                return False
        else:
            dashes_count = 0

        if c == '\n':
            consecutive_newlines += 1
            needs_space = True

            if consecutive_newlines >= 2:
                if sentence:
                    print(process_sentence(sentence.strip()))
                    sentence = ""
                print()
                needs_space = False
        elif c.isspace():
            needs_space = True
            consecutive_newlines = 0
        else:
            consecutive_newlines = 0

            if needs_space and sentence:
                sentence += " "
            needs_space = False

            sentence += c

            if c in ".?!":
                print(process_sentence(sentence.strip()))
                sentence = ""
                needs_space = False

        return True

    for char in preamble_buffer:
        if not handleCharacters(char):
            return

    while True:
        c = sys.stdin.read(1)
        if not c: break
        if not handleCharacters(c):
            break



def setupStreams():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

def formatPremble():
    preambleLength = 10
    lineCounter = 0
    blankLinesInARow = 0
    lineIsBlank = True
    stillSearching = True
    buffor = ""

    while stillSearching:
        c = sys.stdin.read(1)
        if not c: break

        buffor += c

        if c == '\n':
            lineCounter += 1

            if lineIsBlank:
                blankLinesInARow += 1
            else:
                blankLinesInARow = 0

            if blankLinesInARow >= 2:
                buffor = ""
                stillSearching = False
                break

            if lineCounter >= preambleLength:
                stillSearching = False

            lineIsBlank = True

        elif not c.isspace():
            lineIsBlank = False

    return buffor

if __name__ == "__main__":
    main(echo)


