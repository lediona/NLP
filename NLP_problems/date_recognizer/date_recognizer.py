from dateutil import parser
from datetime import datetime
import argparse
import re


def date_recognizer(filename):
    """
        Input: document of line of strings
        
        Output: extracted space separated dates in format of YYYY-MM-DD
        """
    # read the file per line
    
    with open(filename, 'r') as file:
        content = file.readlines()
    
    for line in content:
        
        """
            Extract the date of one line based on the formats by using respectively
            5 regex for each type of format
        
        """
        list_of_regex = []
        regex1 = r"((?:1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th|13th|14th|15th|16th|17th|18th|19th|20th|21st|22nd|23rd|24th|25th|26th|27th|28th|29th|30th|31st)\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s[\d]{4})"
        regex2 = r"[\d]{1,2}/[\d]{1,2}/[\d]{4}"
        regex3 = r"[\d]{1,2}-[\d]{1,2}-[\d]{2}"
        regex4= r"([\d]{1,2}\s(?:Jan|Feb|Mar|Apr|May|Ju|Jul|Aug|Sep|Oct|Nov|Dec)\s[\d]{4})"
        regex5= r"([\d]{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s[\d]{4})"
        # create a list of regex in order to loop them and find the right regex for format
        list_of_regex=[regex1,regex2,regex3,regex4,regex5]
        
        for regex in list_of_regex:
            dates = re.findall(regex, line)
            #print(dates)
            if dates !=[]:
                for s in dates:
                    # make use of  dateutil parser to convert the date string into datetime.datetime object
                    dt = parser.parse(s)
                    
                    # convert the datetime object back to the required format YYYY-MM-DD
                    # and print it
                    timestampStr = dt.strftime("%Y-%m-%d")
                    print(timestampStr)
        else:
            # if the none of the regex can not extract the date print NULL- and break one NULL only for one line
            print('NULL')
            break


def handle_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    
    return parser.parse_args()

def main():
    args = handle_parameters()
    date_recognizer(**vars(args))

#get_the_correction('corpus.txt', 'misspelled_words.txt')

if __name__ == "__main__":
    
    main()
