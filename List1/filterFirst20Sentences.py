from contextlib import nullcontext

from common import set_up_streams


def filter_first_20_sentences(process_sentence):
    filter_first_x_sentences(process_sentence, 20)

def filter_first_x_sentences(process_sentence, x):
    set_up_streams()

def process_text_stream():
    return nullcontext