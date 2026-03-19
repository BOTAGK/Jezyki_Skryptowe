from common import get_stream_with_paragraphs_preserved, is_end_of_sentence, set_up_streams

def find_longest_sentence(is_sentence_valid):
    set_up_streams()

    currentSentence = ""
    characterCount = 0

    maxLength = 0
    maxSentence = ""

    for c in get_stream_with_paragraphs_preserved():
        currentSentence += c

        if not c.isspace():
            characterCount += 1

        if is_end_of_sentence(c):
            strippedSentence = currentSentence.strip()
            if strippedSentence:
                if is_sentence_valid(strippedSentence):
                    if maxLength < characterCount:
                        maxLength = characterCount
                        maxSentence = strippedSentence

            currentSentence = ""
            characterCount = 0

    # sprawdzenie ostatniego zdania w pliku
    strippedSentence = currentSentence.strip()
    if strippedSentence:
        if is_sentence_valid(strippedSentence):
            if maxLength < characterCount:
                maxSentence = strippedSentence

    return maxSentence

