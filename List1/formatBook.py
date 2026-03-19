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
    preamble_buffer = format_preamble()

    sentence = ""
    consecutive_newlines = 0
    dashes_count = 0

    #tylko bóg wie co tutaj sie dzieje
    def handleCharacters(c):
        nonlocal sentence, consecutive_newlines, dashes_count

        if c == '-':
            dashes_count += 1
            if dashes_count >= 5:
                return False
        else:
            dashes_count = 0

        # Obsługa enterów i akapitów
        if c == '\n':
            consecutive_newlines += 1

            if consecutive_newlines == 2:
                if sentence:
                    clean_sentence = sentence.strip()
                    if clean_sentence:
                        # Wymuszamy kropkę na końcu akapitu
                        if not is_end_of_sentence(clean_sentence[-1]):
                            clean_sentence += "."
                        # 1. POPRAWKA: Wysyłamy clean_sentence, a nie sentence.strip()
                        on_sentence_found(clean_sentence)
                    sentence = ""

                on_paragraph_break()
            # Zamieniamy enter na spację
            c = ' '
        # 2. POPRAWKA: Zerujemy licznik, gdy trafimy na literę (nie-spację)
        elif not c.isspace():
            consecutive_newlines = 0

        # Budowanie zdań
        if is_end_of_sentence(c):
            sentence += c
        else:
            # Jeśli próbujemy dodać literę po znaku interpunkcyjnym
            if sentence and is_end_of_sentence(sentence[-1]):
                clean_sentence = sentence.strip()
                if clean_sentence:
                    on_sentence_found(clean_sentence)

                # Zaczynamy nowe zdanie ignorując spację po kropce
                if c.isspace():
                    sentence = ""
                else:
                    sentence = c
            else:
                # Redukcja spacji
                if c.isspace():
                    # 3. POPRAWKA: Dodajemy spację tylko, jeśli zdanie nie jest puste
                    # i nie kończy się już spacją. Inaczej po prostu ją ignorujemy (brak else).
                    if sentence and not sentence[-1].isspace():
                        sentence += c
                else:
                    sentence += c

        return True

    for char in preamble_buffer:
        if not handleCharacters(char):
            return

    for c in get_safe_char_stream():
        if not handleCharacters(c):
            break

    # Sprawdzenie ostatniego zdania
    if sentence:
        clean_sentence = sentence.strip()
        if clean_sentence:
            if not is_end_of_sentence(clean_sentence[-1]):
                clean_sentence += "."
            on_sentence_found(clean_sentence)




def format_preamble():
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