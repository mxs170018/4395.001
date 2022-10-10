# MXS170018
# Manuel Salado Alvarado
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import pickle
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import sent_tokenize
import operator


# Function that scrapes the text from a URL 
# and adds the text to a raw file while removing the HTML Style, script, head, title, etc
def webScraper(url, count):
    

    # function to determine if an element is visible
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html,features="lxml")
    data = soup.findAll(text=True)
    result = filter(visible, data)
    temp_list = list(result)      # list from filter
    temp_str = ' '.join(temp_list)
    file = "raw" + str(count) + ".txt"
    text = str(temp_str.encode('utf-8'))
    with open(file,'w') as f:
        f.write(text)
    
    return file

# Function processes the scraped text from the webScrapper
# It processes it by getting rid of the first line and the last 5 lines 
# as well as lowercasing everything 
def processScrape(file):
    with open(file,'r') as f:
        
        raw_text = f.read()
        
    raw_text = sent_tokenize(raw_text)
    

    all_text= ""
    for texts in raw_text[1:-5]:
        
        texts = texts.replace("when modifying attributes of this phoenix-super-link, make sure you also set attributes in superLink in card/main.js", "")
        tokens = word_tokenize(texts)
        tokens = [t.lower() for t in tokens]
        tokens = [t for t in tokens if t.isalpha()]
        if len(tokens) != 0:
            for tok in tokens:
                all_text += " " +tok
            all_text += "\n"

    newFile = file.replace("raw","processed")
    with open(newFile,'w') as f:
        f.write(all_text)
    


# Main function that takes in 2 George Washington related URLS and crawls on them to find relevant URLS
# Afterwards it scrapes the text and processes it and outputs a file for each of file
# Then it creates a knowledge base on 10 relevant frequent words where each word has a list of correlated sentences 
# it pickles the knowledge base for usage on another program
if __name__ == '__main__': 

    beg_url = "https://www.history.com/topics/us-presidents/george-washington"

    
    r = requests.get(beg_url)

    data = r.text
    soup = BeautifulSoup(data,features="lxml")


    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            #print(link_str)
            if 'washington' in link_str or 'america' in link_str:# or 'president' in link_str
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                    print('MOD:', link_str)
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if 'image' not in link_str and 'timeline' not in link_str:
                    
                    if link_str.startswith('http') and 'google' not in link_str:
                        f.write(link_str + '\n')

    beg_url = "https://www.biography.com/us-president/george-washington"

    #
    r = requests.get(beg_url)

    data = r.text
    soup = BeautifulSoup(data,features="lxml")
    with open('urls.txt', 'a') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            #print(link_str)
            if 'washington' in link_str or 'america' in link_str:# or 'president' in link_str
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                    print('MOD:', link_str)
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if 'image' not in link_str:
                    
                    if link_str.startswith('http') and 'google' not in link_str:
                        f.write(link_str + '\n')
    

    counter = 0
    
    with open('urls.txt','r') as f:
        while f:
            line = f.readline()
            if line == '':
                break
            #file = webScraper(line,counter)
            #processScrape(file)
            counter += 1
    all_text = ""
    for i in range(0,counter):
        newFile = "processed" + str(i) +".txt"
        with open(newFile,'r') as f:
            stuff = f.read()
        all_text += stuff
    
    
    tokens = word_tokenize(str(all_text))
    tokens = [t.lower() for t in tokens if t not in stopwords.words('english')]
    freq = {}
    for token in tokens:
        
        if token not in freq:
            freq[token]=1
        elif token in freq:
            freq[token] += 1

    # We sort the dictionary in descending order so the most frequent nouns are at the top
    # here we do this by converting to a set so that the values can be compared and sorted
    sorted_tuples = sorted(freq.items(), key=operator.itemgetter(1), reverse =True)
    
    # we create a dictionary that takes in the tuple list, setting the corresponding key and value 
    sorted_dict ={word:count for word,count in sorted_tuples}

    print("Top 40 most frequent words in the pages: ")
    
    # we create a list that holds just the nouns in descending order by frequency
    sorted_list = [noun for noun,count in sorted_tuples]

    # we set the list to only include the top 50 frequent nouns
    sorted_list = sorted_list[:40]

    # We then print out this list of nouns, along with its frequency in the text
    for noun in sorted_list:
        
        print(noun, end=", ")
        print(sorted_dict[noun])
    
    kb_Words = ["american","war","president","revolutionary","independence","colonies","united","government","virginia","british"]
    # American, war, President, General, Revolutionary, Independence, colonies, United, government, virginia
    sentences = all_text.replace("\n",".")
    all_sent = sent_tokenize(sentences)

    knowledgeBase = {}
    knowledgeBase["american"] = ["George Washington was an american"]
    knowledgeBase["war"] = ["George Washington fought in many wars"]
    knowledgeBase["president"] = ["George Washington became a president"]
    knowledgeBase["revolutionary"] = ["George Washington was an avid revolutionary"]
    knowledgeBase["independence"] = ["George Washington fought for independence from the british rule"]
    knowledgeBase["colonies"] = ["George Washington was the first president of the former colonies"]
    knowledgeBase["united"] = ["George Washington helped create the united states of america"]
    knowledgeBase["government"] = ["George Washington thought that a limited government was best"]
    knowledgeBase["virginia"] = ["George Washington was born in virginia"]
    knowledgeBase["british"] = ["George Washington was formerly british"]
    
    
    for sent in all_sent:
        for word in kb_Words:
            if word in sent:
                if "george" in sent or "washington" in sent:
                    knowledgeBase[word] =knowledgeBase[word] + [sent]
                    
    pickle.dump(knowledgeBase,open('knowledgeBase.p','wb'))

    

   
    

        
