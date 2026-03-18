from common import run_safely, set_up_streams, get_safe_char_stream, is_end_of_sentence, echo, get_stream_with_paragraphs_preserved

def filter_by_two_conjunctions():
    filter_by_conjunctions(2)

def filter_by_conjunctions(conjunctionLimit):
    def print_sentence(sentenceText):
        print(echo(sentenceText))

    process_text_stream(print_sentence, conjunctionLimit)

def process_text_stream(on_sentence_found, conjunctionLimit):
    set_up_streams()
    
    currentSentence = ""
    currentWord = ""
    conjunctionCount = 0
    
    for c in get_stream_with_paragraphs_preserved():
        currentSentence += c

        if c.isspace() or is_end_of_sentence(c):
            # delete whitespaces and punctuation
            cleanWord = currentWord.lower().strip()

            if cleanWord == "i" or cleanWord == "oraz" or cleanWord == "ale" or cleanWord == "że" or cleanWord == "lub":
                conjunctionCount += 1

            currentWord = ""
        else:
            if not is_end_of_sentence(c):
                currentWord += c

        # end of sentence
        if is_end_of_sentence(c):
            # print only if conjunctions count exceeds 2
            if conjunctionCount >= conjunctionLimit:
                on_sentence_found(currentSentence.strip())

            currentSentence = ""
            currentWord = ""
            conjunctionCount = 0

if __name__ == "__main__":
    run_safely(filter_by_two_conjunctions)


