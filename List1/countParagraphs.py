import sys


from common import run_safely, set_up_streams, get_safe_char_stream

def count_paragraphs():
    set_up_streams()

    paragraphCount = calculate_paragraphs_count()

    print(paragraphCount)

def calculate_paragraphs_count():
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
    run_safely(count_paragraphs)

