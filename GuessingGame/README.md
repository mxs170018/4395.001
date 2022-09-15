## Guessing Game Description

by tokenizing it and removing all of the non alpha characters, while also removing all stop words and words that are of length 5 or less. Afterwards it is lemmatized and then marked with a Parts-of-speech tagger. It prints the first 20 unique lemmas, and then makes a list of those lemmas that are nouns and calculates the lexical diversity of the initial text. After all this, it starts a word guessing game, similiar to wheel of fortune/hang man, in which the user has to guess a word by trying different letters. The user starts with a score of 5 and if they guess a letter right the score increments and if the letter is wrong, the score decrements. The word bank is sourced from the top 50 unique nouns from the orignal text. One is choosen at random for the guessing game. The guessing game ends when the user enters a "!" or their score is negative.  

## How to run
run the python file with the path for the datafile as an argument
