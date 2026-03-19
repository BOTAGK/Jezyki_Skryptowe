from common import get_sentences_stream
from common import get_stream_with_paragraphs_preserved, is_end_of_sentence, set_up_streams, echo, run_safely

def filter_first_20_sentences(process_sentence):
    filter_first_x_sentences(process_sentence, 20, False)

def filter_first_x_sentences(process_sentence, x, count_paragraphs=False):
    def print_sentence(sentence):
        print(process_sentence(sentence))

    def print_empty_line():
        print()

    if count_paragraphs:
        process_text_stream(print_sentence, x, print_empty_line)
    else:
        process_text_stream(print_sentence,x)

def process_text_stream(on_sentence_found, limit, on_paragraph_break=None):
    set_up_streams()
    sentenceCount = 0

    for item in get_sentences_stream():

        if item == '\n' and on_paragraph_break:
            on_paragraph_break()
            continue

        on_sentence_found(item)
        sentenceCount += 1

        if sentenceCount >= limit:
            break


if __name__ == "__main__":
    run_safely(lambda: filter_first_20_sentences(echo))