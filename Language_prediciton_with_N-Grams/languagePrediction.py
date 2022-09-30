# Homework3_2.py
# MXS170018
# Manuel Salado Alvarad
from argparse import RawDescriptionHelpFormatter
import pickle
import sys 
import math
import nltk
import os
from nltk.util import ngrams
from nltk import word_tokenize


# A function for calculating the laplace probability
# that a line of text is a given language. It returns 
# the log of the probability  
def lang_prob(text, uniDict, biDict,V):
    
    # V is the vocabulary size in the training data (unique tokens all languages)

    # first we tokenize the input text
    # and lowercase everything as well as remove anything that is not alpha
    unigrams_test = word_tokenize(text)
    unigrams_test = [t.lower() for t in unigrams_test]
    unigrams_test = [t for t in unigrams_test if t.isalpha()]

    # We then extract the bigrams from the text
    bigrams_test = list(ngrams(unigrams_test, 2))

    # variables that will hold the probabilities 
    p_laplace = 1  # calculate p using Laplace smoothing
    p_log = 0      # add log(p) to prevent underflow

    # for every test bigram 
    for bigram in bigrams_test:

        # we see if it is located in the given languages 
        # occurency bigram dictionary, if it is not 
        # we set this value to 0 to denote 0 occurences
        n = biDict[bigram] if bigram in biDict else 0
        
        # we see if the first word from the bigram is in the
        # given language occurency unigram dictionary, if it is not
        # we set this value to 0 to denote 0 occurences 
        d = uniDict[bigram[0]] if bigram[0] in uniDict else 0
        
        # the laplace smoothing as well as its log counterpart
        p_laplace = p_laplace * ((n + 1) / (d + V))
        p_log = p_log + math.log((n + 1) / (d + V))
    # returns the log of the laplace smoothing
    return p_log


# Main method that unpickles n-gram occurency dictionaries to see
# which lines in a test document correspond to a certain language
# This needs the part1 file to run first, because it depends on 
# its argument list and pickled documents
if __name__ == '__main__':

    # Opens the argument text file created by part one
    with open('arg.txt','r') as f:
        raw_text = f.readlines()
    
    # a variable that holds the number of languages according to
    # the arg file
    languageNum = int(raw_text[0])

    # We parse out the languages from the argument list 
    langArg = raw_text[1]
    langArg = langArg.replace("[","")
    langArg = langArg.replace("'","")
    langArg = langArg.replace("]","")
    langArg = langArg.replace(","," ")
    langArg = langArg.replace("LangId.train.","")
    
    # and we tokenize it so we can get 
    # a list of the languages passed in part 1
    languages = word_tokenize(langArg)
    
    # naming strings with an X to be replaced 
    # by a number for opening the pickle files
    uniG = 'Unix.pickle'
    biG = 'Bix.pickle'
    
    # Two lists for holding the unpickled dictionaries
    # that hold the n-grams of the languages 
    uniList= []
    biList = []

    # For every language in the arguments
    for i in range(1,languageNum+1):

        # we rename the strings to open the file
        # that corresponds to a certain language 
        uniG2 = uniG.replace('x',str(i))
        biG2 = biG.replace('x',str(i))

        # We unpickle these dictionaries and append them
        # to their corresponding lists
        with open(uniG2,'rb') as handle:
            uni = pickle.load(handle)
            uniList.append(uni)
        with open(biG2,'rb') as handle:
            bi = pickle.load(handle)
            biList.append(bi)

    # We open the test text file at the file path provided
    with open(os.path.join(os.getcwd(),sys.argv[1]),'r',encoding='utf-8') as f:
        testText = f.readlines()

    # we open the solution text file at the file path provided
    with open(os.path.join(os.getcwd(),sys.argv[2]),'r',encoding='utf-8') as f:
        solText = f.readlines()

    # we get rid of all the new lines in the solution
    for i in range(len(solText)):
        solText[i] = solText[i].replace("\n","")
    
    # V is equal to the unique set of tokens in all given language corpa
    v = 0
    for i in range(languageNum):
        v += len(uniList[i])

    # The list that holds the predicted language for 
    # every line
    finalOut = []

    # for every line in the test text
    for tests in testText:

        # we create a temporary list
        # for storing the probability 
        # of each of the languages 
        outList = []
        # for every language 
        for i in range(languageNum):
            # we get the probability of the given text being a 
            # certain language 
            prob = lang_prob(tests,uniList[i],biList[i],v)
            
            # we append it to the list 
            outList.append((prob,languages[i]))
        
        # And then we append language with the best 
        # probability to that list
        finalOut.append(min(outList)[1])
    
    # We set standard output to a variable
    # so it doesn't get lost when we write to a file
    original_stdout = sys.stdout
    with open('predictions.txt','w') as f:

        # We write our predictions to a solutionfile
        sys.stdout = f
        i = 1
        for sol in finalOut:
            print(i,finalOut[i-1])
            i=i+1
        sys.stdout = original_stdout
    
    # Afterwards we get the accuracy
    # by comparing the actual solution
    # to our predictions
    i = 0
    accuracy = 0
    for test in finalOut:
        if test in solText[i]:
            accuracy += 1
        i += 1


    # We print the number of test lines
    # and our accuracy over those tests
    print("Number of test lines",i)
    print("Accuracy:",(accuracy/i)*100, "%")