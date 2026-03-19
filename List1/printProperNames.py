from common import set_up_streams, get_sentences_stream, run_safely, echo


def print_proper_names(process_sentence, count_paragraphs):
    set_up_streams()

    def print_sentence(sentence):
        print(process_sentence(sentence))

    def print_empty_line():
        print()

    process_text_stream(print_sentence, print_empty_line, count_paragraphs)

def print_proper_names_from_sentence(process_sentence, sentence_text):
    current_word = ""
    in_word = False
    is_first_word = True
    proper_name = False

    for c in sentence_text:

        if c.isalpha():
            #jesli litera dodaje do obecnego wyrazu
            current_word += c
            # Jeśli właśnie zaczynamy nowe słowo
            if not in_word:
                in_word = True
                # Sprawdzamy czy zaczyna się wielką literą i nie pierwsze  slowo i ustawiamy flage properName
                if c.isupper() and not is_first_word:
                   proper_name = True

        else:
            # konczymy slowo jesli znak interpunkcyjny,
            if in_word:
                #jesli slowo bylo proper to printujemy
                if proper_name:
                    process_sentence(current_word)

                #zmieniamy flagi
                current_word = ""
                is_first_word = False
                in_word = False
                proper_name = False



def process_text_stream(process_sentence, on_paragraph_break, count_paragraphs):

    for item in get_sentences_stream():
        if item == '\n' and count_paragraphs:
            on_paragraph_break()

        print_proper_names_from_sentence(process_sentence, item)


if __name__ == "__main__":
    run_safely(lambda: print_proper_names(echo, False))