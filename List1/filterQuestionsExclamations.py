from common import set_up_streams, get_safe_char_stream, is_end_of_sentence, run_safely, echo, get_sentences_stream


def filter_questions_and_exclamations(process_sentence, count_paragraphs):
    #dodanie oddzielenie odpowiedzialnosci
    def print_sentence(sentence):
        print(process_sentence(sentence))

    def print_empty_line():
        print()

    process_text_stream(print_sentence, print_empty_line, count_paragraphs)

def process_text_stream(on_sentence_found, on_paragraph_break, count_paragraphs):
    set_up_streams()

    for item in get_sentences_stream():
        if item == '\n' and count_paragraphs:
            on_paragraph_break()
            continue

        if item.endswith(("!", "?")):
            on_sentence_found(item)


if __name__ == "__main__":
    run_safely(lambda: filter_questions_and_exclamations(echo, True))