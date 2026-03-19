
from common import get_sentences_stream
from common import run_safely, echo, set_up_streams, count_words_in_sentence

def filter_short_sentences_4(process_sentence, count_paragraphs):
    filter_short_sentences(process_sentence,4, count_paragraphs)

def filter_short_sentences(process_sentence,max_word_count, count_paragraphs):
    def check_and_print_sentence(sentence_text, word_count):
        if 0 < word_count <= max_word_count:
            print(process_sentence(sentence_text))

    def print_empty_line():
        print()

    process_text_stream(check_and_print_sentence, print_empty_line, count_paragraphs)



def process_text_stream(on_sentence_found, on_paragraph_break, count_paragraphs):
    set_up_streams()

    for item in get_sentences_stream():
        if item == '\n' and count_paragraphs:
            on_paragraph_break()
            continue

        word_count = count_words_in_sentence(item)

        on_sentence_found(item, word_count)

if __name__ == "__main__":
    run_safely(lambda: filter_short_sentences_4(echo, True))