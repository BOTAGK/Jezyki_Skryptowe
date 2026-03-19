from common import run_safely, set_up_streams, get_safe_char_stream, is_end_of_sentence, echo, get_stream_with_paragraphs_preserved, get_sentences_stream

def filter_by_two_conjunctions(process_sentence, count_paragraphs):
    filter_by_conjunctions(process_sentence,2, count_paragraphs)

def filter_by_conjunctions(process_sentence, conjunctionLimit, count_paragraphs):
    def print_sentence(sentenceText):
        print(process_sentence(sentenceText))

    def print_empty_line():
        print()

    process_text_stream(print_sentence,print_empty_line, conjunctionLimit, count_paragraphs)

def count_conjunctions_in_sentence(sentence_text):
    conjunction_count = 0
    current_word = ""

    for c in sentence_text:
        if c.isalpha():
            current_word += c
        else:
            # Jesli spacja lub interpunkcja
            if current_word:
                clean_word = current_word.lower()
                if clean_word == "i" or clean_word == "oraz" or clean_word == "ale" or clean_word == "że" or clean_word == "lub":
                    conjunction_count += 1
                current_word = ""

    # Sprawdzenie ostatniego słowa w zdaniu
    if current_word:
        clean_word = current_word.lower()
        if clean_word == "i" or clean_word == "oraz" or clean_word == "ale" or clean_word == "że" or clean_word == "lub":
            conjunction_count += 1

    return conjunction_count

def process_text_stream(on_sentence_found,on_paragraph_break, conjunctionLimit, count_paragraphs):
    set_up_streams()

    for item in get_sentences_stream():

        if item == '\n' and count_paragraphs:
            on_paragraph_break()
            continue

        if count_conjunctions_in_sentence(item) >= conjunctionLimit:
            on_sentence_found(item)

if __name__ == "__main__":
    run_safely(lambda: filter_by_two_conjunctions(echo, True))


