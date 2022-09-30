# Predicting a language with N-Grams

## Description
This [python file](languageNGram.py) takes in N number of files LangId.train.XXXX files where XXXX represents a language. The files provided are corpora of languages for the file to extract bigram and unigrams. They are each placed into a dictionary where the key is the N-gram and the value is the occurence in the corpora. These dictionaries are pickled for extraction in the second file. Two pickle files should be created per language as well as a single arg.txt file (which holds the arg[v] for this file and N)

This [python file](languagePrediction.py) takes in two files, one that holds sentences of different languages and the other holds the correct solution corresponding to the line numbers. The program will unpickle the pickled files from before based on the languages in arg.txt. It will predict the language for every line in the test file by running LaPlace smoothing and extracting the best match. It then checks the predictions against the solution and outputs an accuracy

## Running
run [python file](languageNGram.py) with any number of LangId.train.XXXX files as arguments

### $: python languageNGram.py LangId.train.English LangId.train.French LangId.train.Italian


afterwards run [python file](languagePrediction.py) with a test file and a solution file as arguments

### $: python languagePrediction.py LangId.test LangId.sol
