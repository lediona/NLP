import argparse
import re
from math import log

"""
    Create a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
    Assume that all words are independently distributed and calculate the relative frequency of all words.
    Assumimg that they follow Zipf's law: the word with rank n in the list of words has a  probability estimated 1/(n log N)
    where N refers to the number of words in the dictionary.
    The file words_by_frequency is produced from a small subset of Wikipedia and downloaded from : https://www.wordfrequency.info/top5000.asp
"""
corpus= open("20k.txt").read().split()
word_cost = dict((k, log((i+1)*log(len(corpus)))) for i,k in enumerate(corpus))
max_word = max(len(x) for x in corpus)


def split_the_text(s):
    """ Predict the location of spaces in a string
        without spaces with dinamic programming."""
    
    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-max_word):i]))
        return min((c + word_cost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)
    
    # create the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)
    
    # find the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k
    
    return " ".join(reversed(out))


def text_splitting(file_name):
    """
        The function that reads the input file and calls the split_the_text function to split to infer the spaces in the text
        Input: list of social media hashtags
        Output: words splitted into tokens
        """
    # read the file
    with open(file_name, 'r') as file:
        content = file.readlines()
    #print(content)

    # remove the hashtag with regex
    for hashtag in content:
        tokens = hashtag.replace("#", "").replace("_", " ")
        
        # split the word with the based on Zipf law and cost
        splitted_words =split_the_text(tokens)
        print(splitted_words)


def handle_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    
    return parser.parse_args()

def main():
    args = handle_parameters()
    text_splitting(**vars(args))

#get_the_correction('corpus.txt', 'misspelled_words.txt')

if __name__ == "__main__":
    
    main()
