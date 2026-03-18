from common import echo, run_safely, is_end_of_sentence
from longestSentenceLogic import find_longest_sentence


def print_longest_sentence_with_unique_starts(process_sentence):
    def check_unique_starts(sentence, wordCount):
        lastStart = None
        inWord = False

        for c in sentence:
            if c.isalpha():
                if not inWord:
                    inWord = True
                    currStart = c.lower()
                    if lastStart is not None and currStart == lastStart:
                        return False
                    lastStart = currStart
            elif c.isspace() or is_end_of_sentence(c):
                inWord = False
        return True

    longestSentence = find_longest_sentence(check_unique_starts)

    if longestSentence:
        print(process_sentence(longestSentence))


if __name__ == "__main__":
    run_safely(lambda: print_longest_sentence_with_unique_starts(echo))