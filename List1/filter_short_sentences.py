import sys
from common import run_safely, is_end_of_sentence, echo, set_up_streams, get_stream_with_paragraphs_preserved

def filterShortSentences4():
    filterShortSentences(4, False)

def filterShortSentences(maxWordCount, countParagraphs=False):
    def check_and_print_sentence(sentence_text, wordCount):
        if 0 < wordCount <= maxWordCount:
            print(echo(sentence_text))

    def print_empty_line():
        print()

    if countParagraphs:
        process_text_stream(check_and_print_sentence, print_empty_line)
    else:
        process_text_stream(check_and_print_sentence)

def process_text_stream(on_sentence_found, on_paragraph_break=None):
    set_up_streams()

    currentSentence = ""
    wordCount = 0
    inWord = False
    consecutiveNewLine = 0

    for c in get_stream_with_paragraphs_preserved():

        #oblsuga akapitow
        if c == '\n':
            consecutiveNewLine += 1
            #jesli mamy on_paragraph to wykonujemy
            if consecutiveNewLine == 2 and on_paragraph_break is not None:
                on_paragraph_break()

            c = ' '
        elif not c.isspace():
            consecutiveNewLine = 0

        currentSentence += c

        if c.isalpha():
            if not inWord:
                inWord = True
                wordCount += 1
        elif c.isspace() or is_end_of_sentence(c):
            inWord = False

        if is_end_of_sentence(c):
            if currentSentence.strip() != "":
                on_sentence_found(currentSentence.strip(), wordCount)

            currentSentence = ""
            wordCount = 0
            inWord = False


if __name__ == "__main__":
    run_safely(filterShortSentences4)