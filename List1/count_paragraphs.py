import sys


from common import run_safely, set_up_Streams, get_safe_char_stream

def countParagraphs():
    set_up_Streams()

    paragraphCount = calculateParagraphsCount()

    print(paragraphCount)

def calculateParagraphsCount():
    paragraphCount = 0
    consecutiveBlankLines = 0
    hasText = False

    for c in get_safe_char_stream():
        if c == '\n':
            consecutiveBlankLines += 1

            if consecutiveBlankLines >= 2 and hasText:
                paragraphCount += 1
                hasText = False

        elif c.isspace():
            consecutiveBlankLines = 0

        else:
            consecutiveBlankLines = 0
            hasText = True

    if hasText:
        paragraphCount += 1

    return paragraphCount

if __name__ == "__main__":
    run_safely(countParagraphs)

