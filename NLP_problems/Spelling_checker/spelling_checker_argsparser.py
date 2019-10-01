from collections import Counter
import sys
import argparse

#corpus_filename = 'corpus.txt' or plain_text.txt
#miss_spelled_word = 'misspelled_words.txt'

# I tested the script first with a list of english words from Webster Dictionary (corpus.txt) and with a plain text from Wikipedia (plain_text)
# The result with the enlglish_words was:
#cotan
#servius
#note
#asdfasdf

#while the result with the plain_text was more accurate:
#contain
#serious
#note
#asdfasdf

#Conclusion: it needed more corpus of plain text to be trained in order to achieve maximum accuracy in spelling


def load_words(filename):
    """
        function that reads the corpus containg words that contain only letters not symbols
        Input: path to the file
        Output: counter of words
        """
    with open(filename) as word_file:
        valid_words = Counter(word_file.read().split())
    
    return valid_words

def get_the_correction(corpus_filename, miss_spelled_word):
    
    corpus=load_words(corpus_filename)
    miss_spelled= load_words(miss_spelled_word)
    
    def P(word, N=sum(corpus.values())):
        "find the probability of the word in the corpus"
        return corpus[word] / N

    corrected_spelling = ''
    for word in miss_spelled:
        
        if word in corpus:
            corrected_spelling= word
        else:
            
            edited_strings = get_edits1(word)
            
            # narrow down and filter the edited strings to only meaningful words that can
            # be found in the corpus
            
            close_matches = set([word for word in edited_strings if word in corpus])
            candidates = (close_matches or [word] or match )
            corrected_spelling = max(candidates, key=P)

        print(corrected_spelling)

def get_edits1(word):
    """
        All types of edits that are one edit away from original word
        “Edits” can be:
        removed character,
        added character,
        character replaced with another one,
        two consecutive character switched places.
        
        Return : set of all the edited strings that can be made with one edit away from original:
        """
    alphabet_letters = 'abcdefghijklmnopqrstuvwxyz'
    splited_word =  [(word[:i], word[i:])    for i in range(len(word) + 1)]
    removed_character    = [a + b[1:] for a, b in splited_word if b]
    transposed_character = [a + b[1] + b[0] + b[2:] for a, b in  splited_word if len(b)>1]
    replaced_character   = [a + c + b[1:] for a, b in  splited_word for c in alphabet_letters if b]
    added_character    = [a + c + b     for a, b in  splited_word for c in alphabet_letters]
    
    return set(removed_character + transposed_character + replaced_character + added_character)


def handle_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus_filename', type=str)
    parser.add_argument('miss_spelled_word', type=str)
    return parser.parse_args()

def main():
    args = handle_parameters()
    get_the_correction(**vars(args))

#get_the_correction('corpus.txt', 'misspelled_words.txt')

if __name__ == "__main__":
    
    main()

