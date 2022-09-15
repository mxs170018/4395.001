# 4395.001
# Human Language Technologies

MXS170018
Manuel Salado Alvarado

## Portfolio O
You can see my brief description of NLP [here](NLP-P0-MXS170018.pdf)

## Employee Parse
You can see the [folder here](Employee Parse) which takes in a text file that holds employee data and it parses the data so that it can be cleaned and rectified afterwards it is puts the data into a dictionary and then pickles and unpickles it before printing

## Guessing Game
you can see the [folder here](Guessing Game) which takes in a path to a text file that holds a chapter of an anatomy text book. This program preprocess the text by tokenizing it and removing all of the non alpha characters, while also removing all stop words and words that are of length 5 or less. Afterwards it is lemmatized and then marked with a Parts-of-speech tagger. It prints the first 20 unique lemmas, and then makes a list of those lemmas that are nouns and calculates the lexical diversity of the initial text. After all this, it starts a word guessing game, similiar to wheel of fortune/hang man, in which the user has to guess a word by trying different letters. The user starts with a score of 5 and if they guess a letter right the score increments and if the letter is wrong, the score decrements. The word bank is sourced from the top 50 unique nouns from the orignal text. One is choosen at random for the guessing game. The guessing game ends when the user enters a "!" or their score is negative.  
