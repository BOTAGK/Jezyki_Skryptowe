import sys

from common import get_sentences_stream
from common import run_safely, is_end_of_sentence, echo, set_up_streams, get_stream_with_paragraphs_preserved

def filter_short_sentences_4(process_sentence, count_paragraphs):
    filter_short_sentences(process_sentence,4, False)

def filter_short_sentences(process_sentence,maxWordCount, count_paragraphs=False):
    def check_and_print_sentence(sentence_text, wordCount):
        if 0 < wordCount <= maxWordCount:
            print(process_sentence(sentence_text))

    def print_empty_line():
        print()

    process_text_stream(check_and_print_sentence, print_empty_line(), count_paragraphs)

def count_words_in_sentence(sentence_text):
    word_count = 0
    in_word = False

    for c in sentence_text:
        if c.isalpha():
            if not in_word:
                in_word = True
                word_count += 1
        else:
            in_word = False

    return word_count

def process_text_stream(on_sentence_found, on_paragraph_break, count_paragraphs):
    set_up_streams()

    for item in get_sentences_stream():
        if item == '\n' and count_paragraphs:
            on_paragraph_break()
            continue

        word_count = count_words_in_sentence(item)

        on_sentence_found(item, word_count)

if __name__ == "__main__":
    run_safely(lambda: filter_short_sentences_4(echo))