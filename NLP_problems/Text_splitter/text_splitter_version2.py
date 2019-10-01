import argparse
import re
from math import log
import wordninja

"""
    This version of the script is shorter as it calls the wordninja library created from
    the previous idea of cost dictionary by taking into account the Zupf's law and the cost probability.
"""


def text_splitting_version2(file_name):
    """
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
        splitted_words =wordninja.split(tokens)
        joined= ' '. join(splitted_words)
        print(joined)


def handle_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    
    return parser.parse_args()

def main():
    args = handle_parameters()
    text_splitting_version2(**vars(args))

#get_the_correction('corpus.txt', 'misspelled_words.txt')

if __name__ == "__main__":
    
    main()
