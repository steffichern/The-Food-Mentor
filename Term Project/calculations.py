import scanner
import cv2
from pyzbar import pyzbar
import requests
import webscraping

### Inputs and calculations for 'intake checker' mode #####
def basicInfo(self):
    inputGenderInfo(self)
    inputNumbersInfo(self)
    activityLevel(self)
        

def inputGenderInfo(self):
    while True:
        response = self.getUserInput('Enter your gender (male/female): ')
        try:
            self.gender = str(response)
            if self.gender == '':
                self.showMessage('Please enter one!')
            elif self.gender.lower() == 'male' or self.gender.lower() == 'female':
                return
            else:
                self.showMessage('Invalid gender!')
        except:
            self.showMessage('Please enter a valid gender!')

def inputNumbersInfo(self):  # age, height, weight
    while True:
        temp = []
        answer = self.getUserInput('Enter your age/height (in cm)/weight (in kg) \n(use commas to separate): ')
        try:
            for ans in answer.split(','):   
                ans = ans.strip()
                temp.append(ans)

            self.age = int(temp[0])
            self.peopleHeight = int(temp[1])
            self.weight = int(temp[2])
            if len(temp) > 3:  # too many inputs
                self.showMessage('Too many inputs! Try again.')
            elif self.age >= 0 and self.peopleHeight > 0 and self.weight > 0:
                return
        except:
               self.showMessage('Incorrect format or invalid input.')

def activityLevel(self):
    while True:
        response = self.getUserInput('Enter activity level (each week): \n 1: 0-2 days  2: 3-5 days  3: everyday ')
        try:
            self.activityLevel = int(response)
            if self.activityLevel == 0:
                self.showMessage('Please enter one!')
            elif self.activityLevel < 0 or self.activityLevel > 3:
                self.showMessage('Invalid input!')
            else:
                return
        except:
            self.showMessage('Please enter a valid number!')

def askGrams(self):
    while True:
        grams = self.getUserInput('How many grams of this product do u plan to eat?')
        try:
            self.getGrams = int(grams)
            if self.getGrams == 0:
                self.showMessage('Please enter one!')
            elif self.getGrams < 0:
                self.showMessage('Invalid input!')
            elif self.getGrams > 0:
                return
        except:
            pass


def calculateCalsForMen(self):
    if self.activityLevel == 1:
        self.projectCals = round(self.BMR*1.2, 1)
    elif self.activityLevel == 2:
        self.projectCals = round(self.BMR*1.35, 1)
    elif self.activityLevel == 3:
        self.projectCals = round(self.BMR*1.57, 1)

def calculateCalsForWomen(self):
    if self.activityLevel == 1:
        self.projectCals = round(self.BMR*1.085, 1)
    elif self.activityLevel == 2:
        self.projectCals = round(self.BMR*1.287, 1)
    elif self.activityLevel == 3:
        self.projectCals = round(self.BMR*1.5, 1)


def calculateRecs(self):  # projected calories, default
    if self.gender == 'male':
        self.BMR = 13.4*self.weight + 4.79*self.peopleHeight - 5.67*self.age + 88.362
        calculateCalsForMen(self)
        
    elif self.gender == 'female':
        self.BMR = 9.25*self.weight + 3.1*self.peopleHeight - 4.33*self.age + 447.59
        calculateCalsForWomen(self)

##### calculate recommended stats for macros, all in kcals #######
### self.projectCals is default cals (weight maintain)
def maintainMacros(self): # maintain weight
    projectCarbs = round(self.projectCals*0.3, 1)
    projectProtein = round(self.projectCals*0.4, 1)
    projectFat = round(self.projectCals*0.3, 1)
    return projectCarbs, projectProtein, projectFat

def lossMacros(self):
    projectCarbs = round(self.projectCals*0.75*0.25, 1)
    projectProtein = round(self.projectCals*0.75*0.55, 1)
    projectFat = round(self.projectCals*0.75*0.2, 1)
    return projectCarbs, projectProtein, projectFat

def gainMacros(self):
    projectCarbs = round(self.projectCals*1.3*0.50, 1)
    projectProtein = round(self.projectCals*1.3*0.25, 1)
    projectFat = round(self.projectCals*1.3*0.25, 1)
    return projectCarbs, projectProtein, projectFat

########### calculate recommended stats for macros, all in grams #####
def projMaintainGrams(self):
    gramsOfCarbs = int(self.projectCals*0.3+40)
    gramsOfProtein = int(self.projectCals*0.4+25)
    gramsOfFat = int(self.projectCals*0.3+20)
    return gramsOfCarbs, gramsOfProtein, gramsOfFat

def projLossGrams(self):
    gramsOfCarbs = int(self.projectCals*0.2+10)
    gramsOfProtein = int(self.projectCals*0.6+30)
    gramsOfFat = int(self.projectCals*0.2+20)
    return gramsOfCarbs, gramsOfProtein, gramsOfFat

def projGainGrams(self):
    gramsOfCarbs = int(self.projectCals*0.5+40)
    gramsOfProtein = int(self.projectCals*0.25+35)
    gramsOfFat = int(self.projectCals*0.25+20)
    return gramsOfCarbs, gramsOfProtein, gramsOfFat

# calculate how much calories/macros the user consumed
# calories: in kcal
# macros: in grams
#  4kcal/g, 4kcal/g, 9kcal/g

def userConsumed(self):  # the very last scan, adds up everything
    caloriesConsumed = round(self.allCals+(self.getGrams/100)*self.getCals, 2)
    carbsConsumed = round(self.allCarbs+(self.getGrams/100)*self.getCarbs, 2)
    proteinConsumed = round(self.allProtein+(self.getGrams/100)*self.getProtein, 2)
    fatConsumed = round(self.allFat+(self.getGrams/100)*self.getFat, 2)
    return caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed

def accumulate(self): # temps
    self.allCals += (self.getGrams/100)*self.getCals
    self.allCarbs += (self.getGrams/100)*self.getCarbs
    self.allProtein += (self.getGrams/100)*self.getProtein
    self.allFat += (self.getGrams/100)*self.getFat


def scanMore(self):
    self.getCals = self.getCarbs = self.getProtein = self.getFat = self.getGrams = 0
    self.scanUPC = ''

 # based on maintaining weight
 # Cite: based on http://pennstatehershey.adam.com/graphics/pdf/en/19996.pdf
def recs(self):
    caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed = userConsumed(self)
    self.caloriesConsumed = caloriesConsumed
    diff = remainCalories = 0
    newDataList = []
    newDataFood = []
    s = set()
    newDataDict = dict() # newdata for all data
    if self.caloriesConsumed < self.projectCals:   # only suggest if underconsumption
        diff = int(self.projectCals - self.caloriesConsumed)  # remaining calpries
        with open('Recs/myRecs.txt', "r") as file:  # food, calories
            lines = file.readlines()
            for i in range(len(lines)):
                newDataList += (lines[i].split(','))
                
            for c in range(0, len(newDataList), 2):  # calories in odd idexes, food in even indexes
                newDataList[c+1] = (newDataList[c+1].strip()).replace('\n','')
                newDataList[c+1] = int(newDataList[c+1])
                newDataDict[newDataList[c]] = newDataList[c+1] # map to the dict

            for i in newDataDict:  # to randomnize
                s.add(i)

            for key in s:  
                remainCalories += newDataDict[key]  # accumulate calories
                
                if remainCalories <= diff+80:
                    newDataFood.append((key, newDataDict[key]))  # add tuples to list..(food, calories)
                    if remainCalories >= abs(diff-80):  # plus minus 80 calories of leeway
                        return newDataFood

                    
                elif remainCalories > diff+80:
                    remainCalories = 0  # recalculate
                    newDataFood = []
                    
    else:
        return list()

def storeRecs(self):   # store to a txt file for displaying purposes
    newDataFood = recs(self)
    with open(f'Recs/finalRecs.txt', "w+") as file:
        if newDataFood == list():
            file.write('You are overeating already!')  # simply print out you are overeating
            file.close()
        else:
            for (food, calories) in newDataFood:
                file.writelines(f"{food} --- {calories} kcal\n")

def recListToStr(self):  
    with open(f'Recs/finalRecs.txt', "r") as f:
        self.recs = f.read()
        
