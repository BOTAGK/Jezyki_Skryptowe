from common import echo, run_safely
from longestSentenceLogic import find_longest_sentence


def print_longest_sentence(process_sentence):
    # bez dodatkowych wymagan
    def always_valid(sentence, wordCount):
        return True

    longestSentence = find_longest_sentence(always_valid)
    if longestSentence:
        print(process_sentence(longestSentence))


if __name__ == "__main__":
    run_safely(lambda: print_longest_sentence(echo))