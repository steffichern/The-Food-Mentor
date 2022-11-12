
import requests
import webscraping
import getUserInfo


def drawInstructionsText():
    text = """
    Welcome! You will be asked to enter your name in the first step.
    Then, there is a list of the most common digestive problems/food 
    disorders to choose from if that applies to you. If you decide to 
    skip this step, you have the option to enter what specific kind of
    ingredients you are allergic to (or doesn't want in your food). You 
    will now be asked to scan the barcode on your food product to see if 
    that product contains the ingredients that you don't want/cannot eat. 
    It will then display if that product is safe for you or not. All the 
    products you scanned will be stored and lebeled safe or unsafe in a 
    txt file in your laptop for future references. Enjoy :)
    """
    return text

# extract ingredients data from txt file based on chosen condition; build up the dict()
def getConditionIngredients(self):  
    conditions = dict()  # {condition:{ingredient}, condition2: {ingredient}...}
    countLines = 0
    file = open("conditions.txt", "r")
    file.seek(0, 0)
    lines = file.readlines()  # returns a list

    for ind in range(len(self.listOfCond)):
        conditions[self.listOfCond[ind]] = set() 

    for lactoseWord in lines:
        countLines += 1
        lactoseWord = (lactoseWord.replace('\n','').upper())  # remove extra stuff for accuracy
        if lactoseWord == 'LACTOSE INTOLERANT:':
            continue
        if lactoseWord == '----------':
            break
        elif conditions != dict():
            conditions[self.listOfCond[0]].add(lactoseWord)
        else:
            conditions[self.listOfCond[0]] = {lactoseWord} # convert to set for efficiency purposes

    file.seek(0, 1)   # current location
    index = 1
    cond = self.listOfCond[index]
    for i in range(countLines, len(lines)):
        word = lines[i].replace('\n','').upper()
        if word == 'PEANUT ALLERGY:' or word == 'TREE NUT ALLERGY:' or word == 'SEAFOOD ALLERGY:' \
            or word == 'EGG ALLERGY:' or word == 'SOY ALLERGY:' or word == 'WHEAT & GLUTEN ALLERGY:':
            continue
        elif word == '----------':
            cond = self.listOfCond[index + 1]
            index += 1
            continue
        if conditions[cond] != set():
            conditions[cond].add(word)
        else:
            conditions[cond] = {word}

    #print(file.tell())
    return conditions

# check each case (condition), determine safe, unsafe
def matchingCondition(self):   
    self.conditions = getConditionIngredients(self)
    safety = True
    temp = set()
    if self.hasCondition == [False]*len(self.listOfCond):
        return True
    for index in range(len(self.listOfCond)):
        if self.hasCondition[index]:
            temp = self.conditions[self.listOfCond[index]]
            for forbidden in temp: 
                for ingredient in self.dataUSDA:
                    if forbidden == ingredient:
                        safety = False
                        self.unsafeFromCondition.append(ingredient)
                        print(self.unsafeFromCondition)
                    
    return safety

# check user inputs, determine safe/unsafe
def matchingInputFood(self):   
    safety = True
    if self.inputFood != set():
        for ingredient in self.dataUSDA:
            for userInput in self.inputFood:
                if ingredient == userInput:
                    safety = False
                    self.unsafeFromInput.append(ingredient)
                    print(self.unsafeFromInput)

    return safety

def checkIngredient(self):  # check based on inputted ingredients when product not found
    self.conditions = getConditionIngredients(self)
    safety = True
    # for ind in range(len(self.listOfCond)):
    #     for cond in self.conditions[self.listOfCond[ind]]:
    #         for inputFood in self.inputFood:
    #             for ingre in self.inputIngredients:
    #                 if inputFood == ingre:
    #                     safety = False
    #                     self.unsafeFromInput.append(ingre)
    #                     print(self.unsafeFromInput)
    #                 elif cond == ingre:
    #                     safety = False
    #                     self.unsafeFromCondition.append(ingre)
    #                     print(self.unsafeFromCondition)
    # return safety
    for ind in range(len(self.listOfCond)):
        for cond in self.conditions[self.listOfCond[ind]]:
            for ingre in self.inputIngredients:
                if cond == ingre:
                    safety = False
                    self.unsafeFromCondition.append(ingre)
                    print(self.unsafeFromCondition)

    for inputFood in self.inputFood:
        for ingre in self.inputIngredients:
            if inputFood == ingre:
                        safety = False
                        self.unsafeFromInput.append(ingre)
                        print(self.unsafeFromInput)

    return safety
def isSafe(self):  # final verdict
    result = webscraping.checkExist(self)
    if result != None:
        isSafeCondition = matchingCondition(self)
        isSafeFood = matchingInputFood(self)
        if (isSafeCondition == False) or (isSafeFood == False):
            self.safe = False
    if result == None:
        isSafeIngredient = checkIngredient(self)
        if isSafeIngredient == False:   
            self.safe = False
        # self.pastSafe.append(self.safe)

def getAllergens(self):
    if self.state == 'result':
        for i in self.unsafeFromCondition:
            for j in self.unsafeFromInput:
                self.unsafeList.append(self.unsafeFromInput[j])
            self.unsafeList.append(self.unsafeFromCondition[i])

# def hasPressedCondition(self):
#     if self.state == 'result':
#         for i in range(len(self.hasCondition)):
#             if self.hasCondition[i] == True:
#                 return True
#         return False





