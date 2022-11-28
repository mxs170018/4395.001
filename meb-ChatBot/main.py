#ChatBot main
#Manuel Salado Alvarado
#MXS170018

import json
import string
import random 
import sys 
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np 
import tensorflow as tf 

from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Dropout
nltk.download("punkt")
nltk.download("wordnet")
riddles =0
correctRiddle = 0
jokes = 0 
laughs = 0


def bag(text,vocab):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    bow = [0] * len(vocab)
    for w in tokens:
        for idx, word in enumerate(vocab):
            if word == w:
                bow[idx] = 1
    
    return np.array(bow)

def pred_class(text,vocab, labels):
    global riddles
    global correctRiddle
    global jokes
    global laughs
    bow = bag(text, vocab)
    result = model.predict(np.array([bow]),verbose=0)[0]
    thresh = 0.5
    y_pred = [[indx,res] for indx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)

    return_list = []

    for r in y_pred:
        return_list.append(labels[r[0]])
    
    if 'riddle' in return_list:
        riddles += 1
    elif 'answers' in return_list:
        correctRiddle += 1
    elif 'jokes' in return_list:
        jokes += 1
    elif 'haha' in return_list:
        laughs += 1

    return return_list

def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        result = "Sorry, I don't understand"
        list_of_intents = ""
    else:
        tag = intents_list[0]
        list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break

    return result 


if __name__ == '__main__':
    
    with open('intents.json',"r") as fp:
        data_file = fp.read()

    data = json.loads(data_file)

    users = {}
    with open("users.txt","r") as fp:
        for line in fp.readlines():
            user = ""
            likes = []
            dislikes = []
            wisdom = ""
            humor = ""
            opinions = []

            model = line.split()
            user = model[0]
            model.remove(model[0])
            model.remove(model[0])
            while model.index("Dislikes:") != 0:
                likes.append(model[0].replace("_"," "))
                model.remove(model[0])
            model.remove(model[0])
            while model.index("StatsW-H:") != 0:
                dislikes.append(model[0].replace("_"," "))
                model.remove(model[0])

            model.remove(model[0])
            wisdom = model[0]
            model.remove(model[0])
            humor = model[0]
            model.remove(model[0])
            model.remove(model[0])
            while len(model) != 0:
                opinion = model[0]
                opinion = opinion.replace("_"," ")
                opinion = opinion.replace("I ","You ")
                opinion = opinion.replace("my ","your ")
                opinion = opinion.replace("am ","are ")
                model.remove(model[0])
                opinions.append(opinion)
            
            userList = []
            userList.append(likes)
            userList.append(dislikes)
            userList.append(wisdom)
            userList.append(humor)
            userList.append(opinions)

            users[user] = userList
    
    words = []
    classes = []
    data_X = []
    data_Y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            tokens = nltk.word_tokenize(pattern)
            words.extend(tokens)
            data_X.append(pattern)
            data_Y.append(intent["tag"])
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

    lemmatizer = WordNetLemmatizer()

    words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]

    words = sorted(set(words))
    classes = sorted(set(classes))

    training = []
    out_empty = [0]*len(classes)

    for idx, doc in enumerate(data_X):
        bow = []
        
        text = lemmatizer.lemmatize(doc.lower())
        for word in words:
            if word in text:
                bow.append(1)
            else:
                bow.append(0)
        output_row = list(out_empty)
        output_row[classes.index(data_Y[idx])] = 1

        training.append([bow,output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)

    train_X = np.array(list(training[:,0]))
    train_Y = np.array(list(training[:,1]))

    model = Sequential()
    model.add(Dense(128,input_shape=(len(train_X[0]),),activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64,activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_Y[0]),activation="softmax"))

    adam = tf.keras.optimizers.Adam(learning_rate=0.01,decay=1e-6)
    model.compile(loss='categorical_crossentropy',optimizer=adam, metrics=["accuracy"])

    print(model.summary())
    model.fit(x=train_X,y=train_Y,epochs=150,verbose=0)

    wisdom = 0.0
    humor = 0.0
    print("enter EXIT to exit chatbot")
    beenHere = input("Have you been here before? [Yes/No] ")
    been = False
    print()
    if beenHere.lower() == "yes" or beenHere.lower()=="y":
        print("Welcome back")
        been = True
    else:
        print("Hello Hello")

    userName = input("What is your name?\n")
    print()
    if been:
        while userName not in users:
            print("I don't remember you, try again\n")
            userName = input("What is your name?\n")

    if been:
        
        thisUser = users[userName]
        if len(thisUser[0]) == 0:
            print("You didn't tell me what you liked")
        else:
            print("I remember a thing you like is",random.choice(thisUser[0]))
        if len(thisUser[1]) == 0:
            print("you didn't tell me what you disliked")
        else: 
            print("I remember a thing you dislike is ",random.choice(thisUser[1]))
        wisdom = float(thisUser[2])
        humor = float(thisUser[3])
        if wisdom >= 1:
            print("You are very wise, you solved every riddle")
        elif wisdom >=.8:
            print("You are pretty wise, you got most of my riddles")
        elif wisdom >= .5:
            print("Your wisdom is mid, you got some of my riddles")
        elif wisdom < .5:
            print("You're not the sharpest tool in the tool shed")
        
        if humor >= 1:
            print("You enjoy lauging at my lame jokes, I like you")
        elif humor >= .8:
            print("You enjoy some of my dumb jokes")
        elif humor >= .5:
            print("Your sense of humor is somewhat lacking, I thought my jokes were funny")
        elif humor <.5:
            print("How have you gotten this far without a sense of humor?")

    else:
        print("Nice to meet you,",userName,"I'll remember your likes, dislikes, opinions, wisdom, and sense of humor")
    print("\nAnyways, greet me, don't be rude\n")
    likes = []
    dislikes = []
    
    opinions = []

    if not been:
        userData = []
        userData.append(likes)
        userData.append(dislikes)
        userData.append(1.0)
        userData.append(0.0)
        userData.append(opinions)
        users[userName] = userData
    
    riddleBool = False
    while True:
        message = input(userName+": ")
        if message == "EXIT":
            break
        message = message.replace("'","")
        message = message.lower()
        messag = message.split()
        

        if messag[0] == "i" and (messag[1] == "like" or messag[1] == "love"):
            

            op = message[7:].replace(" ","_")
            op = op.replace("you ","Meb ")
            op = op.replace("i ","You ")
            users[userName][0].append(op)
            print("Meb: I will remember that you like",message[7:])
            print()
        elif messag[0] == "i" and (messag[1] == "dislike" or messag[1] == "hate" or messag[1] =="dont" or messag[1] == "don't"):
            aLine = ""
            for stuff in messag:
                if stuff != "i" and stuff != "dislike" and stuff!= "hate" and stuff != "dont" and stuff != "like":
                    aLine += stuff +" "
            aLine = aLine[0:-1]
            aLine = aLine.replace("you ","Meb ")
            aLine = aLine.replace("i ","You ")
            aLine = aLine.replace(" ","_")
            users[userName][1].append(aLine)
            print("Meb: I will remember that you dislike",aLine.replace("_"," "))
            print()
        elif messag[0] == "i" and messag[1] == "think":
            indx =0
            if messag[2] == "that":
                indx= 13
                
            else:
                indx = 8
            op = message[indx:]
            op = op.lower()
            op = op.replace("you ","Meb ")
            op = op.replace("i ","You ")
            op = op.replace("my ","your ")
            op = op.replace("am ","are ")
            users[userName][4].append(op)
            print("Meb: I will remember that you think that",op)
            print()
            
        else:
            if "riddle" in messag:
                riddleBool = True 
            

            intents = pred_class(message,words, classes)
            result = get_response(intents, data)
            if result == "GGG":
                result = userName
            elif result == "LIKES":
                result = ""
                for like in users[userName][0]:
                    result += like+", "
                if result == "":
                    result = "You haven't told me what you like yet"
                
            elif result == "DISLIKES":
                result = ""
                for dislike in users[userName][1]:
                    result += dislike+", "
                if result =="":
                    result = "You haven't told me what you dislike yet"
                
            elif result == "OPINIONS":
                result = ""
                for op in users[userName][4]:
                    result += op+", "
                if result == "":

                    result = "You haven't told me what you think ye"
            elif result == "RANDOM":
                result =""
                listOP = []
                for u in users:
                    if len(users[u][4]) != 0:
                        listOP.append(u) 
                person = random.choice(listOP)
                aResult = random.choice(users[person][4])
                aResult = aResult.replace("You","they")
                result = person +" thinks that "+aResult
            print("Meb: "+result)
            print()

            if riddleBool:
                theRiddle = result 
            while riddleBool:
                message = input(userName+": ")
                
                
                if message == "EXIT":
                    break
                if message == "QUITTER":
                    print("Meb: you actually gave up? I am still not going to tell you the answer, but you can do other things now")
                    riddleBool = False
                    print()
                    break 
                message = message.lower()
                intents = pred_class(message,words, classes)
                if "givingup" in intents or "hintTime" in intents or "idk" in intents:
                    result = get_response(intents, data)
                    print("Meb: "+result)
                    print()
                elif "answers" in intents:
                    result = get_response(intents, data)
                    riddleBool = False
                    print("Meb: finally, you got the riddle correct")
                    print()
                else:
                    print("Meb: Nah that's not it, If you want to stop guessing just say QUITTER")
                    print("Meb:",theRiddle)
                    print()
                    
                    
                

    
    if riddles == 0:
        wisdom = float(users[userName][2])
    else:
        wisdom = ((correctRiddle/riddles) + float(users[userName][2])/2)
    if jokes == 0:
        humor = float(users[userName][3])
    else:
        humor = ((laughs/jokes) + float(users[userName][3])/2)

    users[userName][2] = round(wisdom,1)
    users[userName][3] = round(humor,1)


    with open("users.txt","w") as fp:
        for us in users:
            strToWrite ="" 
            strToWrite += us
            strToWrite += " Likes: "
            for like in users[us][0]:
                strToWrite += like +" "
            
            strToWrite += "Dislikes: "
            for dislike in users[us][1]:
                strToWrite += dislike.replace(" ","_") +" "
            strToWrite+= "StatsW-H: "
            strToWrite += str(users[us][2]) +" "+ str(users[us][3]) +" "

            strToWrite += "Opinions:"
            for opinion in users[us][4]:
                opinionLine = opinion.replace(" ","_")
                opinionLine = opinionLine.replace("You","I")
                opinionLine = opinionLine.replace("your","my")
                opinionLine = opinionLine.replace("are","am")
                strToWrite += " "+opinionLine

            strToWrite += "\n"
            fp.write(strToWrite)
    print(userName+":")
    print("Likes: "+str(users[userName][0]))
    print("Dislikes: "+str(users[userName][1]))
    print("Wisdom: "+ str(users[userName][2]))
    print("Sense of Humor: "+ str(users[userName][3]))
    print("Opinions: "+ str(users[userName][4]))