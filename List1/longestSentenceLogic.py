from common import get_stream_with_paragraphs_preserved, is_end_of_sentence, set_up_streams

def find_longest_sentence(is_sentence_valid):
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
            strippedSentence = currentSentence.strip()
            if strippedSentence:
                if is_sentence_valid(strippedSentence):
                    if maxLength < wordCount:
                        maxLength = wordCount
                        maxSentence = strippedSentence

            currentSentence = ""
            wordCount = 0
            inWord = False

    # sprawdzenie ostatniego zdania w pliku
    strippedSentence = currentSentence.strip()
    if strippedSentence:
        if is_sentence_valid(strippedSentence):
            if maxLength < wordCount:
                maxSentence = strippedSentence

    return maxSentence

