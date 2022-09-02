#MXS170018, Manuel Salado Alvarado
#CS 4395.001

# This python file takes in a text file that holds employee data
# and it parses the data so that it can be cleaned and rectified
# afterwards it is puts the data into a dictionary and then 
# pickles and unpickles it before printing
import re
import sys
import os
import pickle

# Person class that holds the employee informtaion
class person:
    # Initialization in which the employee's first and last names
    # their middle initial, their ID, and their phone number is set 
    def __init__(self,fname,lname,mInit,pId,phone):
        self.fname = fname
        self.lname = lname
        self.mInit = mInit
        self.pId = pId
        self.phone = phone
    
    # function that displays the information about the person
    def display(self):
        print("Employee id: "+self.pId)
        print("\t"+self.fname+" "+self.mInit+" "+self.lname)
        print("\t" + self.phone)
        
# function that parses the file that was passed in and cleans
# and modifies the information so that the correct data gets
# sent into the dictionary of people        
def parseFile(people):

    # the RegEx pattern for the input phone number
    pnumber = re.compile(r'\d{3}[ .]\d{3}[ .]\d{4}')

    # the RegEx pattern for the output phone number
    pnumberMod = re.compile(r'\d{3}[-]\d{3}[-]\d{4}')

    # the RegEx pattern for the person ID
    personId = re.compile(r'[A-Z]{2}\d\d\d\d')

    # splits the input data by new lines into a list
    listA = people.split("\n")
    
    # dictionary to hold the people
    peoples = {}

    # iterates through every line from the input CSV
    for t in listA:
        
        # splits the line by the commas into another list
        tempList = t.split(",")
        
        # the first element in the list is the first name
        # this sets the entire name to lower case and then 
        tempList[0] = tempList[0].lower()

        # capitalizes the first letter
        tempList[0] = tempList[0].capitalize()

        # the 2nd element in the list is the last name
        # this sets the entire name to lower case and then 
        tempList[1] = tempList[1].lower()

        # capitalizes the first letter
        tempList[1] = tempList[1].capitalize()

        # the 3rd element in the list is the middle initial
        # if it is not empty, then it is capitalized
        if tempList[2]:
            tempList[2] = tempList[2].capitalize()

        #otherwise it is set to an X
        else:
            tempList[2] = 'X'
        
        # the 4th element in the list is the person ID
        # This compares the regex pattern against the string    
        matches = personId.fullmatch(tempList[3])

        # this sets a temp variable to the ID
        newID = tempList[3]

        # while the regex pattern and the personID don't match
        # then we continue asking the user for input until it does
        while not matches:
            print("ID invalid: " + newID)
            print("ID is two letters followed by 4 digits")
            print("please enter a valid id: ",end=" ")
            newID = input()
            matches = personId.fullmatch(newID)
            
        
        # the 5th element is a phone number
        # If the phone number is of length 10 and they are all digits
        # then it is safe to say it is a valid phone number
        if len(tempList[4])==10 and tempList[4].isdigit():
            # We add the dashes here for display purposes
            tempList[4] = tempList[4][:3]+"-"+tempList[4][3:6] + "-" + tempList[4][6:10]
        #otherwise
        else:

            # we compare the regex pattern for phonenumber
            matches2 = pnumber.fullmatch(tempList[4])
            newPhone = tempList[4]

            # if it does not match then we prompt the user for anew
            # one until it does match
            while not matches2:
                print("Phone " + newPhone +"  is invalid")
                print("Enter phone number in form 123-456-7890")
                print("Enter phone number: ",end=" ")
                newPhone = input()
                matches2 = pnumberMod.fullmatch(newPhone)
            # We add the dashes here for display purposes
            tempList[4] = tempList[4][:3]+"-"+tempList[4][4:7] + "-" + tempList[4][8:12]
        
        # when it is all clean we initialize a new person object
        # and we add it to the dictionary defined above with their
        # key corresponding to the person ID
        peoples[tempList[3]]= person(tempList[0],tempList[1],tempList[2],tempList[3],tempList[4])

    #return the dictionary of people
    return peoples

# Main function
if __name__ == '__main__':
    # if the command line didn't include arguments 
    # the program ends
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')

    # otherwise
    else:
        # we try to open a file with the name of the argument
        fp = sys.argv[1]
        with open(os.path.join(os.getcwd(),fp),'r') as f:

            # we discard the header line
            f.readline()
            
            # the rest we store in a string
            text_in = f.read()
        # the function is called with the unparsed text    
        peoples = parseFile(text_in)

        # the people dictionary that was returned is pickled
        pickle.dump(peoples,open('dict.p','wb'))

        # then it is unpickled
        picklePeople = pickle.load(open('dict.p','rb'))
        
        # and then the entire dictionary is printed via
        # the display function of the people in the dictionary
        print("Employee List: \n")
        for x in picklePeople:
            picklePeople[x].display()
        
