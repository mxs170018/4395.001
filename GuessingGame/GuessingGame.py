# Manuel Salado Alvarado 
# MXS170018, CS 4395.001

# This python file takes in a path to a text file that holds a chapter of an anatomy text book. 
# This program preprocess the text by tokenizing it and removing all of the non alpha characters,
# while also removing all stop words and words that are of lenth 5 or less. Afterwards it is lemmatized 
# and then marked with a Parts-of-speech tagger. It prints the first 20 unique lemmas, and then makes a list 
# of those lemmas that are nouns and calculates the lexical diversity of the text. After all this, it starts 
# a word guessing game, similiar to wheel of fortune/hang man, in which the user has to guess a word by trying 
# different letters. The user starts with a score of 5 and if they guess a letter right the score increments and if 
# the letter is wrong, the score decrements. The word bank is sourced from the top 50 unique nouns from the orignal text
# One is choosen at random for the guessing game. The guessing game ends when the user enters a "!" or their score is negative.  
import nltk
import os 
import re
import sys
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import operator
from random import seed
from random import randint


# Seed to enhance reproductability of results 
seed(1234)

# Function for preprocessing, it takes the tokenized text extracted from the file and returns
# the lemmatized list of preprocessed tokens and the list of tagged nouns isolated from the former list
# The function preprocesses by removing any token that is non-alpha, a stopword, or 5 characters or smaller
# afterwards, it lemmatizes the preprocessed list and creates a unique set of them 
# it then uses nltk to tag the unique lemmas with Parts of Speech, and prints the first 20
# it then isolates the nouns from this list and returns the list of preprocessed lemmas, and isolated nouns
def preprocess(raw_text):

    # Lowercases every token in the text and places it into a list
    tokenAnat = [t.lower() for t in raw_text]

    # A list of every token in text that is alpha, not in stopwords, and is bigger than 5 characters
    tokenAnat = [t for t in tokenAnat if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
    
    # declares WordNet Lemmatizer to lemmatize all of the tokens in the preprocessed list
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokenAnat]

    # creates a seperate list of the unique lemmas
    lemmas_unique = list(set(lemmas))

    # creates a list of the unique lemmas along with their POS tag
    tags = nltk.pos_tag(lemmas_unique)

    # it then prints the first 20 tags
    print("First 20 unique lemmas: ")
    print(tags[:20])

    # A new list is created to isolate all of the nouns in the tagged preprocessed lis
    tag_nouns = [t for t, pos in tags if "NN" in pos]

    # Prints out the number of tokens in the first preprocessed list 
    print("Number of tokens that are alpha, not in NLTK stopword list, and have length >5: ", end="")
    print(len(tokenAnat))

    # prints out the number of nouns 
    print("Number of nouns: ",end="")
    print(len(tag_nouns))

    # returns the lemmatized list and the list of tagged nouns isolated from the former list
    return lemmas, tag_nouns
    
    
# Guessing game function, takes in the list of 50 preprocessed nouns, 
# A word guessing game, similiar to wheel of fortune/hang man, in which the user has to guess a word by trying 
# different letters. The user starts with a score of 5 and if they guess a letter right the score increments and if 
# the letter is wrong, the score decrements. The word bank is sourced from the top 50 unique nouns from the orignal text
# One is choosen at random for the guessing game. The guessing game ends when the user enters a "!" or their score is negative.  
def guessingGame(guess_list):

    # prompt for the guessing game 
    print("\n\n\nLet's play a word guessing game!")
    
    # variable that holds a random int between 0 and the size of the list
    num = randint(0,len(guess_list))

    # initializes the score variable to 5
    score = 5

    # A list that holds the correctly guessed letters and the letter place holders
    letters = []

    # initializes the user input variable
    inputs = ""

    # boolean variable used to check if the word has been guessed
    guessed = False

    # list that holds the letters that have been guessed, initially has " " or "" in case user misinputs
    let_guessed = [" ",""]

    # while score is non-negative:
    while score >= 0:

        # we get a word to guess from a random index in the noun list
        answer = guess_list[num]

        # for every letter in the answer, we add a placeholder "_" to denote
        # the actual length of the answer, like hangman
        for i in range(0,len(answer)):
            letters.append("_")
        
        # we then print this list so that a word like "Words" would appear as "_ _ _ _ _"
        print(letters)

        # while the user has not guessed the word, and the score is non-negative:
        while not guessed and score >= 0:    
            
            # We get an input letter from the user and lowercase it
            inputs = input("Guess a letter: ")
            inputs = inputs.lower()

            # if the input is "!", we halt the game, print the score, and return to main
            if inputs == "!":
                print("Game Halted")
                print("Final Score: " + str(score))
                return

            # in case the user entered a non-alpha character, we loop here
            # asking the user for a new input until it is alpha    
            while not inputs.isalpha():

                # we append the non-alpha characters to letters guessed so they can't
                # do it again in the next loop
                let_guessed.append(inputs)
                inputs = input("Please enter an alpha character: ")
                inputs = inputs.lower()
                if inputs == "!":
                    break

            # in case the user enters a letter they have already case 
            # We loop here asking the user for new input until it is a letter they have not guessed 
            while inputs in let_guessed:
                inputs = input("Already guessed, try again: ")
                inputs = inputs.lower()
            
            # If we pass these two steps, if the input is "!", 
            # we halt the game, print the score, and return to main
            if inputs == "!":
                print("Game Halted")
                print("Final Score: " + str(score))
                return
            
            # if the input is in the answer
            if inputs in answer:
                
                # we increment score by 1 and print out the score
                score += 1 
                print("Right! Score is " + str(score))
                
                # for every letter in the range the answers index
                for j in range(0,len(answer)):

                    # we check to see if the guessed letter is equal to the letter at index j of the answer
                    if inputs == answer[j]:

                        # we then turn the underscore to the actual letter
                        letters[j] = inputs
            # otherwise     
            else: 
                # we decrement the score by 1 and print it out
                score -= 1
                print("Wrong! Score is " + str(score))
            
            # we print out the list that holds the unguessed underscores and correctly guessed letters
            print(letters)

            # we also append the letter that was guessed to the letters guessed list
            let_guessed.append(inputs)

            # we check to see if the answer has been guessed by scanning 
            # if there are any underscores left in the list, if there are none then:
            if "_" not in letters:

                # guessed boolean is set to true
                guessed = True

                # printout the score, and a prompr congratulating the player
                print("You solved it!")
                print("\nCurrent score is: " + str(score)+"\n")
                print("Guess another word")
        # if the score is negative, the actual word is displayed, and they get a game over prompt
        if score < 0:
            print("Actual Word: " + answer)
            print("\n\n\nGAME OVER!!!\n\n\n")
        
        # End of the while loop and resetting the variables for a new word
        # a new random number is generated to serve as an index for the noun list
        num = randint(0,len(guess_list))

        # Lists and the boolean are set back to their original values
        letters = []
        inputs = ""
        guessed = False
        let_guessed = [" ",""]
            



# MAIN: reads in a path to the file to be preprocessed, tokenizes it, sets it all to lowercase 
# calculates the lexical diversity of the text, calls the preprocessing function makes a list of
# how frequent unique nouns are in the text, sorts that list in descending order so the most common 
# are at the top, then passses that into the guessing game function
if __name__ == '__main__':

    # If the system arguments are less than 2, then the user didn't specify a file name as sys arg
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    
    # otherwise, we can assume they did pass a path
    else: 
        # variable to hold the name of the path
        fp = sys.argv[1]

        # a try statement to try to open the document at the path desribed in sys arg
        with open(os.path.join(os.getcwd(),fp),'r') as f:
            # reads all of the text from the document into a variable
            raw_text = f.read()

    # tokenizes the raw text from the document
    raw_text = word_tokenize(raw_text)

    # lowercases every word in the tokenizes text
    tokenAnat = [t.lower() for t in raw_text]

    # creates a set of unique words from the tokenized text
    setAnat = set(tokenAnat)
    
    # prints the lexical diversity by dividing the unique words/total words
    print("Lexical Diversity: " + str(round(len(setAnat)/len(tokenAnat),2)))
    
    # calls the preprocess function with the tokenized text as an argument, 
    # sets two variables to handle the return information from the function
    lemmas, tag_nouns = preprocess(raw_text)

    # defines an empty dictionary
    token_noun_freq = {}

    # Here we are trying to count the frequency of nouns in the text
    # for every token in the returned preprocessed list 
    for token in lemmas: 

        # If the token is not a key in the dictionary yet, and is a token in the nouns list
        if token not in token_noun_freq and token in tag_nouns:

            # then we should add it to the dictionary with value of 1
            token_noun_freq[token] = 1
        
        # else if, the token is in the dictionary, then we can increment it by 1 to denote frequency
        elif token in token_noun_freq:
            token_noun_freq[token] += 1

    # We sort the dictionary in descending order so the most frequent nouns are at the top
    # here we do this by converting to a set so that the values can be compared and sorted
    sorted_tuples = sorted(token_noun_freq.items(), key=operator.itemgetter(1), reverse =True)
    
    # we create a dictionary that takes in the tuple list, setting the corresponding key and value 
    sorted_dict ={noun:count for noun,count in sorted_tuples}

    print("Top 50 most frequent nouns in the text: ")
    
    # we create a list that holds just the nouns in descending order by frequency
    sorted_list = [noun for noun,count in sorted_tuples]

    # we set the list to only include the top 50 frequent nouns
    sorted_list = sorted_list[:50]

    # We then print out this list of nouns, along with its frequency in the text
    for noun in sorted_list:
        
        print(noun, end=", ")
        print(sorted_dict[noun])
        
    # finally, we call the guessing game with the sorted list as the argument.     
    guessingGame(sorted_list)
