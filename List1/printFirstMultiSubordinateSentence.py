from common import get_sentences_stream
from common import set_up_streams, run_safely, echo

def print_first_multi_subordinate_sentence(process_sentence):
    print_first_n_subordinate_sentence(process_sentence, 2)

def print_first_n_subordinate_sentence(process_sentence, subordinates_num):
    def print_sentence(sentence_text):
        print(process_sentence(sentence_text))

    process_text_stream(print_sentence, subordinates_num)

def count_commas_in_sentence(sentence_text):
    comma_count = 0

    for c in sentence_text:
        if c == ',':
            comma_count += 1

    return comma_count

def process_text_stream(on_sentence_found, subordinates_num):
    set_up_streams()

    for item in get_sentences_stream():

        if item == '\n':
            continue


        comma_count = count_commas_in_sentence(item)

        if comma_count > subordinates_num:
            on_sentence_found(item)
            return

if __name__ == "__main__":
    run_safely(lambda: print_first_multi_subordinate_sentence(echo))
