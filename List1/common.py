import os
import sys


def echo(sentence):
    return sentence


def get_sentences_stream():
    current_sentence = ""
    consecutive_newlines = 0

    for c in get_stream_with_paragraphs_preserved():

        if c == '\n':
            consecutive_newlines += 1
            if consecutive_newlines == 2:
                #wysylamy akapit
                yield '\n'
            c = ' '
        elif not c.isspace():
            consecutive_newlines = 0

        #problem wielu kropek
        if is_end_of_sentence(c):
            current_sentence += c
            continue

        if current_sentence and is_end_of_sentence(current_sentence[-1]):
            clean_sentence = current_sentence.strip()
            if clean_sentence:
                #wysylane cale zdanie
                yield clean_sentence

            current_sentence = c
        else:
            current_sentence += c

    #ostatnie zdanie
    if current_sentence and is_end_of_sentence(current_sentence[-1]):
        clean_sentence = current_sentence.strip()
        if clean_sentence:
            yield clean_sentence

def get_stream_with_paragraphs_preserved():
    pending_newlines = 0
    last_real_char = ''

    #wstawiamy kropke przy akapitach aby
    for c in get_safe_char_stream():
        if c == '\n':
            pending_newlines += 1
            if pending_newlines == 2:
                #jesli mielismy kropke to jej nie wstawiamy
                if last_real_char != '' and not is_end_of_sentence(last_real_char):
                    yield '.'
                yield '\n'
                yield '\n'
            elif pending_newlines > 2:
                yield '\n'
        else:
            if pending_newlines == 1:
                yield '\n'

            pending_newlines = 0

            if not c.isspace():
                last_real_char = c

            yield c
    #jakby caly plik zakonczyl sie jednym enterem
    if pending_newlines == 1:
        yield '\n'

def get_safe_char_stream():
    has_data = False

    while c := sys.stdin.read(1):
        if c == '\r':
            continue

        has_data = True
        yield c

    if not has_data:
        raise EOFError("Błąd: Strumień wejściowy jest pusty.")

def set_up_streams():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

def is_end_of_sentence(c):
    return c in ".?!"

def run_safely(main_func):
    try:
        main_func()

    except BrokenPipeError:
        os._exit(0)
    except EOFError as e:
        print(f"Blad wejscia: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Blad: {e}", file=sys.stderr)
        sys.exit(1)