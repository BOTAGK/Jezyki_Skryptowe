
from common import get_sentences_stream
from common import run_safely, set_up_streams

def count_paragraphs():
    set_up_streams()

    paragraphCount = calculate_paragraphs_count()

    print(paragraphCount)

def calculate_paragraphs_count():
    paragraph_count = 0
    has_text = False

    for item in get_sentences_stream():

        if item == '\n':

            if has_text:
                paragraph_count += 1
                has_text = False

        else:
            has_text = True

    if has_text:
        paragraph_count += 1

    return paragraph_count

if __name__ == "__main__":
    run_safely(count_paragraphs)

