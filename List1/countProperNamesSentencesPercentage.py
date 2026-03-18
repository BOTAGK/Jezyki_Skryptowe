
from common import get_stream_with_paragraphs_preserved, set_up_streams, is_end_of_sentence, echo, run_safely
def count_proper_names_sentences_percentage():
    set_up_streams()
    percentage = calculate_percentage_of_proper_sentences()
    print(percentage)


def calculate_percentage_of_proper_sentences():
    allSentenceCounter = 0
    properNamesSentencesCounter = 0
    isTheFirstWord = True
    #szukane zdania z proper names
    sentenceCounted = False

    for c in get_stream_with_paragraphs_preserved():
        if c == "-":
            continue

        #jesli to koniec zdania
        if is_end_of_sentence(c):
            allSentenceCounter += 1
            isTheFirstWord = True
            sentenceCounted = False
        #jesli to wielka litera
        elif c.isupper():
            if isTheFirstWord:
                #ignorujemy pierwsze slowo
                isTheFirstWord = False
            elif not sentenceCounted:
                properNamesSentencesCounter += 1
                sentenceCounted = True
        #jesli mala
        elif c.islower():
            isTheFirstWord = False

    if allSentenceCounter == 0:
        return 0.0

    return (properNamesSentencesCounter / allSentenceCounter) * 100


if __name__ == "__main__":
    run_safely(count_proper_names_sentences_percentage())