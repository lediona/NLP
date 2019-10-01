
# python script that given a file with enitities can remove the duplicates by using methphone algortithm
# that gives the phonetics to a word or string


import pandas as pd
import numpy as np
import re
import unicodedata
from metaphone import doublemetaphone
import sys
import argparse
#read the file



# 1. Normalize the data
# - remobve special characters and spaces 
def normalize_unicode_to_ascii(data):

    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    result = normal.decode("utf-8")
    result = re.sub('[^A-Za-z0-9 ]+', ' ', result)
    result = re.sub(' +', ' ', result)
    #removing the digits
    result = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", result)
    return result

def sort_list(list_):

    new_organization = sorted(list_)
    return  new_organization

# Doublemetaphone method returns a tuple of two characters key, which are a phonetic translation of the passed in wordphonetic key generator methods 
def double_metaphone(value):
    print(doublemetaphone(value))
    return doublemetaphone(value)

def create_list_of_tuples( sorted_organization)
# Create a list with all the correspoinding tuples for each entities
    list_of_enitity_tuples = []
    for i in sorted_organization:
        tuples = double_metaphone(i)
         list_of_enitity_tuples.append(tuples)

    return  list_of_enitity_tuples

def er_solution(filename):
    organizations_df = pd.read_csv(filename)
    norm_organization = []
    for i in organizations_list:
        organization = normalize_unicode_to_ascii(i)
    #remive the non aplhanumberic terms
        organizat =''.join(filter(lambda x: not x.isdigit(), organization))
    
        norm_organization.append(organizat)
        #remove the empty strings
        norm_organization = filter(None, norm_organization)
        # sort the entitites
        sorted_organization= sort_list(norm_organization)

        list_of_enitity_tuples= create_list_of_tuples( sorted_organization)

        #create a dataframe that contains the enitites and the corresponding tupes
        list_of_tuples = list(zip(sorted_organization, list_of_enitity_tuples)) 
        df = pd.DataFrame(list_of_tuples, columns = ['entities', 'tuples']) 

        # filter the dataframe based on the function double_metaphone_compare(tuple1,tuple2)
        organizations_resolved=[]
        for (indx1,row1),(indx2,row2) in zip(filtered_organization[:-1].iterrows(),filtered_organization[1:].iterrows()):
            # this is the case that they have a strong match
            # where both tuples are equal
            if row1[0][0] == row2[0][0]:
                organizations_resolved.append(row1)
                 #this is the case where tuples have minimum match so append them both

        
        # delete the second item of tuple and keep it as an ID  (j[0][0])
        organization_id = []
        for i, j in enumerate(organizations_resolved):
            organization_id.append((j[1], j[0][0]))

        #b convert the list of tuples and entities in a dataframe
        organization_id_df = pd.DataFrame(organization_id, columns=['name','id' ])

        return  organization_id_df




def handle_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    return parser.parse_args()

def main():
    args = handle_parameters()
    er_solution(**vars(args))

#get_the_correction('corpus.txt', 'misspelled_words.txt')

if __name__ == "__main__":
    
    main()
