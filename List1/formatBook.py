import sys


from common import is_end_of_sentence, run_safely, set_up_streams, echo, get_safe_char_stream

def main_format_book(process_sentence):
    set_up_streams()

    if sys.stdin.isatty():
        print("---Oczekiwanie na wejście standardowe (ctrl + d aby zakonczyc)", file=sys.stderr)


    def print_formatted_sentence(sentence_text):
        print(process_sentence(sentence_text))


    def print_paragraph_break():
        print()


    process_book_stream(
        on_sentence_found=print_formatted_sentence,
        on_paragraph_break=print_paragraph_break
    )

def process_book_stream(on_sentence_found, on_paragraph_break):
    preamble_buffer = formatPreamble()

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
                    on_sentence_found(sentence.strip())
                    sentence = ""

                on_paragraph_break()
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

            if is_end_of_sentence(c):
                on_sentence_found(sentence.strip())
                sentence = ""
                needs_space = False

        return True

    for char in preamble_buffer:
        if not handleCharacters(char):
            return

    for c in get_safe_char_stream():
        if not handleCharacters(c):
            break

    if sentence:
        on_sentence_found(sentence.strip())




def formatPreamble():
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
    run_safely(lambda: main_format_book(echo))