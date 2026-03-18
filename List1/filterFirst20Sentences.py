from common import get_stream_with_paragraphs_preserved, is_end_of_sentence, set_up_streams, echo, run_safely

def filter_first_20_sentences(process_sentence):
    filter_first_x_sentences(process_sentence, 20)

def filter_first_x_sentences(process_sentence, x):
    def print_sentence(sentence):
        print(process_sentence(sentence))

    process_text_stream(print_sentence, x)

def process_text_stream(on_sentence_found, x):
    set_up_streams()
    sentenceCount = 0
    current_sentence = ""


    for c in get_stream_with_paragraphs_preserved():

        if sentenceCount >= x:
            break

        if is_end_of_sentence(c):
            current_sentence += c
            continue

        #reagowanie na koniec kropek znakow zapytania itd (litery, spacje)
        if current_sentence and is_end_of_sentence(current_sentence[-1]):
            clean_sentence = current_sentence.strip()
            #jesli nie pusty printujemy
            if clean_sentence:
                on_sentence_found(clean_sentence)
                sentenceCount += 1

                #sprawdzamy jescze raz czy przekroczylismy x
                if sentenceCount >= x:
                    break

            #resetujemy zdanie i bierzemy obecny znak jako poczatek
            current_sentence = c
        else:
            #jesli ostatni znak to nie kropka poprstu dodajemy c
            current_sentence += c

    #jesli plik ma mniej zdan niz x to printujemy ostatnie zdanie
    if sentenceCount < x and current_sentence and is_end_of_sentence(current_sentence[-1]):
        clean_sentence = current_sentence.strip()
        if clean_sentence:
            on_sentence_found(clean_sentence)

if __name__ == "__main__":
    run_safely(lambda: filter_first_20_sentences(echo))