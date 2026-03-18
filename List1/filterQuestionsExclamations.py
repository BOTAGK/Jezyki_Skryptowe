from common import set_up_streams, get_safe_char_stream, is_end_of_sentence, run_safely, echo


def filter_questions_and_exclamations(process_sentence):
    #dodanie oddzielenie odpowiedzialnosci
    def print_sentence(sentence):
        print(process_sentence(sentence))

    process_text_stream(print_sentence)

def process_text_stream(on_sentence_found):
    set_up_streams()

    current_sentence = ""

    for c in get_safe_char_stream():
        current_sentence += c

        if is_end_of_sentence(c):
            clean_sentence = current_sentence.strip()

            if clean_sentence.endswith(("!", "?")):
                on_sentence_found(clean_sentence)

            current_sentence = ""

if __name__ == "__main__":
    run_safely(lambda: filter_questions_and_exclamations(echo))