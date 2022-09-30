#Homework3_1
# MXS170018, Manuel Salado Alvarado

from nltk.util import ngrams
import sys
import os 
from nltk import word_tokenize
import pickle

# Function that has a file path as an argument to get the unigrams and bigrams 
# of the lowercase alpha tokens and places them in two dictionaries where the value
# is the count of bigrams and unigrams associated with the bigram, unigram keys
def nGrams(fp):
    # a try statement to try to open the document at the path desribed in sys arg
    with open(os.path.join(os.getcwd(),fp),'r',encoding='utf-8') as f:
        # reads all of the text from the document into a variable
        raw_text = f.read()
    
    # replace all new lines with space
    raw_text.replace("\n"," ")

    # tokenize the text
    tokens = word_tokenize(raw_text)
    
    # sets everything to lowercase and 
    # tosses out anything that's not alpha
    tokens = [t.lower() for t in tokens]
    tokens = [t for t in tokens if t.isalpha()]

    # variables that hold the bigrams and unigrams
    bigrams = ngrams(tokens,2)
    unigrams = ngrams(tokens,1)

    # dictionaries that will hold the bigrams and unigram occurences
    bigramDict = {}
    unigramDict = {}

    # for every bigram in the unique set of bigrams 
    for bigram in set(bigrams):

        # if the bigram isnt already in the dictionary
        if bigram not in bigramDict:
            # we add it to the dictionary
            bi = bigram[0] + ' ' + bigram[1]
            # along with the number of occurences in the text
            bigramDict[bi] = raw_text.count(bi)

    # for every unigram in the unique set of unigrams
    for unigram in set(unigrams):

        #if the unigram inst already in the dictionary
        if unigram not in unigramDict:
            # we add it to the unigram dictionary 
            uni = unigram[0]
            # along with the number of occurences in the text
            unigramDict[uni] = raw_text.count(uni)
    
    # we return both dictionaries 
    return unigramDict,bigramDict

# Main method that takes in any number of LangId.train.XXXXXX files where XXXXX
# represents a language and the files contain a corpus of training data corresponding
# to the language. The main program then extracts the bigrams and unigrams of each 
# corpus and assigns them to a dictionary where the value represents the n-gram occurence
# in the provided corpus. The unigram and bigram occurence dictionary is pickled for 
# every language 
if __name__ == '__main__':

    # If the system arguments are less than 2, return an error
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        
    
    # otherwise, we can assume they did pass at least on language
    else: 

        # We assign the standard output to a variable
        # so it isn't lost when we write to a file
        original_stdout = sys.stdout

        # We place the argument list and the number of argumments
        # not including the calling file itself
        with open('arg.txt','w') as f:
            sys.stdout = f
            print((len(sys.argv)-1))
            print((sys.argv[1:]))
            # We reset standard output to the original
            # value
            sys.stdout = original_stdout
        
        # Two lists that will hold the unigram and bigram dictionaries
        uniList = []
        biList = []

        # For every language corpus passed 
        for i in range(1,len(sys.argv)):

            # we get the file name 
            fp = sys.argv[i]

            # get the unigram and bigram occurence count 
            uni,bi = nGrams(fp)

            # append them to their respsective lists
            uniList.append(uni)
            biList.append(bi)
            
        # Two strings that will be used for naming 
        # the pickle files
        uniG = 'Unix.pickle'
        biG = 'Bix.pickle'

        # for every language corpus passed
        for i in range(1,len(sys.argv)):

            # We replace the 'x' in the naming string
            # with a number, to differentiate which language
            # it is associated with
            uniG2 = uniG.replace('x',str(i))
            biG2 = biG.replace('x',str(i))

            # we write the unigram and bigram count dictionaries
            # to pickle files
            with open(uniG2,'wb') as handle:
                pickle.dump(uniList[i-1],handle)
            with open(biG2,'wb') as handle:
                pickle.dump(biList[i-1],handle)
