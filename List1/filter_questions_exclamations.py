from common import set_up_streams, get_safe_char_stream, is_end_of_sentence, run_safely


def filter_questions_and_exclamations():
    set_up_streams()

    current_sentence = ""

    for c in get_safe_char_stream():
        current_sentence += c

        if is_end_of_sentence(c):
            clean_sentence = current_sentence.strip()

            if clean_sentence.endswith(("!", "?")):
                print(clean_sentence)

            current_sentence = ""

if __name__ == "__main__":
    run_safely(filter_questions_and_exclamations)