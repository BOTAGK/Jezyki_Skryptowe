
from common import  set_up_streams, run_safely, get_sentences_stream
def count_proper_names_sentences_percentage():
    set_up_streams()
    percentage = calculate_percentage_of_proper_sentences()
    print(percentage)

def has_proper_name(sentence_text):
    in_word = False
    is_first_word = True

    for c in sentence_text:
        if c.isalpha():
            # Jeśli właśnie zaczynamy nowe słowo
            if not in_word:
                in_word = True
                # Sprawdzamy czy zaczyna się wielką literą i nie pierwsze slowo
                if c.isupper() and not is_first_word:
                    return True
        else:
            #konczymy slowo jesli znak interpunkcyjny,
            if in_word:
                is_first_word = False
                in_word = False

    return False


def calculate_percentage_of_proper_sentences():
    all_sentence_counter = 0
    proper_names_sentences_counter = 0

    for item in get_sentences_stream():

        if item == '\n':
            continue

        all_sentence_counter += 1

        if has_proper_name(item):
            proper_names_sentences_counter += 1

    if all_sentence_counter == 0:
        return 0.0

    return (proper_names_sentences_counter / all_sentence_counter) * 100


if __name__ == "__main__":
    run_safely(count_proper_names_sentences_percentage)