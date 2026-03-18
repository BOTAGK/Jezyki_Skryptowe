from common import set_up_streams, get_stream_with_paragraphs_preserved, is_end_of_sentence, run_safely, echo

def print_first_multi_subordinate_sentence(process_sentence):
    print_first_n_subordinate_sentence(process_sentence, 2)

def print_first_n_subordinate_sentence(process_sentence, subordinatesNum):
    def print_sentence(sentence_text):
        print(process_sentence(sentence_text))

    process_text_stream(print_sentence, subordinatesNum)

def process_text_stream(on_sentence_found, subordinatesNum):
    set_up_streams()

    currentSentence = ""
    commaCount = 0

    for c in get_stream_with_paragraphs_preserved():
        currentSentence += c

        if c == ',':
            commaCount += 1

        if is_end_of_sentence(c):
            # sprawdz czy znaleziono wystarczajaco zdan podrzednych
            if commaCount >= subordinatesNum:
                cleanSentence = currentSentence.strip()
                if cleanSentence:
                    on_sentence_found(cleanSentence)
                    return

            currentSentence = ""
            commaCount = 0

    # sprawdz dla ostatniego zdania
    if commaCount >= subordinatesNum:
        cleanSentence = currentSentence.strip()
        if cleanSentence:
            on_sentence_found(cleanSentence)

if __name__ == "__main__":
    run_safely(lambda: print_first_multi_subordinate_sentence(echo))
