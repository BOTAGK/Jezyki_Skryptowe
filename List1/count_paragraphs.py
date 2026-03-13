import sys

from List1.common import run_safely
from common import setupStreams

def countParagraphs():
    setupStreams()

    paragraphCount = 0
    consecutiveBlankLines = 0
    hasText = False

    while c := sys.stdin.read(1):
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

    print(paragraphCount)


if __name__ == "__main__":
    run_safely(countParagraphs())

