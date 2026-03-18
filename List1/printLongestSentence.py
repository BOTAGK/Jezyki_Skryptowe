from common import set_up_streams, get_stream_with_paragraphs_preserved, is_end_of_sentence, run_safely, echo


def print_longest_sentence(process_sentence):
    def print_sentence(sentence):
        print(process_sentence(sentence))

    process_text_stream(print_sentence)

def process_text_stream(on_sentence_found):
    set_up_streams()

    currentSentence = ""
    wordCount = 0
    inWord = False

    maxLength = 0
    maxSentence = ""

    for c in get_stream_with_paragraphs_preserved():
        currentSentence += c

        if c.isalpha():
            if not inWord:
                inWord = True
                wordCount += 1
        elif c.isspace() or is_end_of_sentence(c):
            inWord = False

        if is_end_of_sentence(c):
            # sprawdź czy zdanie nie jest puste
            if currentSentence.strip():
                if maxLength < wordCount:
                    maxLength = wordCount
                    maxSentence = currentSentence.strip()

            currentSentence = ""
            wordCount = 0
            inWord = False

    # sprawdź dla ostatniego zdania w pliku
    if currentSentence.strip():
        if maxLength < wordCount:
            maxSentence = currentSentence.strip()

    on_sentence_found(maxSentence)


if __name__ == "__main__":
    run_safely(lambda: print_longest_sentence(echo))