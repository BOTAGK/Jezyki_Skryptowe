from common import get_sentences_stream
from common import get_stream_with_paragraphs_preserved, is_end_of_sentence, set_up_streams

def find_longest_sentence(is_sentence_valid):
   set_up_streams()

   max_length = 0
   max_sentence = ""

   for item in get_sentences_stream():

       if item == "\n":
           continue

       char_count = len(item)

       if is_sentence_valid(item):

           if char_count > max_length:
               max_length = char_count
               max_sentence = item

   return max_sentence