from cmu_112_graphics import *
import time
import startings
import calculations
import scanner
import webscraping
import getUserInfo
import foodData
import intakeChecker
import requests
import cv2
from pyzbar import pyzbar

##############
# initializations, images, wrapper funtions for mouse press, key press, drawings
##############

def initializations(self):
    ####### Food Mode ########
    self.timerDelay = 80
    self.pages = ['home', 'askName', 'instructions','conditions', 'enterFood', 'scanBarcode', 'result', 'notFound', 'past']
    self.state = self.pages[0]
    self.listOfCond = ['Lactose Intolerant','Peanut Allergy', 'Tree Nut Allergy', 'Seafood Allergy','Egg Allergy','Soy Allergy','Wheat & Gluten Allergy']
    self.hasCondition = [False]*len(self.listOfCond)
    self.directory = 'User Database'
    self.name = self.text = ''
    self.conditions = dict() # ingredients data from txt file
    self.inputFood = self.inputIngredients = set()  # store user inputs
    self.scanUPC = self.productName = ''
    self.safe = True
    self.dataUSDA = set() # extract ingredient from USDA 
    self.unsafeList = self.unsafeFromCondition = self.unsafeFromInput = []  
    self.fruitCounter = 0
    ####### Intake Mode #########
    self.intakePages = ['home','basic info', 'inputGrams','display1', 'display2', 'display3', 'recommendations']
    self.intakeState = self.intakePages[0]
    self.gender = ''
    self.age = self.weight = self.peopleHeight = -1  # requires input
    self.allCals = self.allCarbs = self.allProtein = self.allFat = self.allGrams = 0  # all the products scanned
    self.activityLevel = self.getGrams = 0
    self.getCals = self.getCarbs = self.getProtein = self.getFat = 0  # in grams, out of 100grams of the product; for one input only
    self.projectCals = self.caloriesConsumed = 0
    self.BMR = 0
    self.recs = ''


def images(self):
    background = 'images/background.jpg'     
    clearBackground = 'images/background.jfif'   # Cite: https://unsplash.com/photos/36aGnv29Ss0
    conditionsBG = 'images/conditionsBG.jpg' 
    inputFoodBG = 'images/inputFoodBG.jpg'  
    notSafeBG = 'images/notsafe.jpg' 
    safeBG = 'images/safe.jpg'
    notFound = 'images/notfound.jpg'
    fruitImg = 'images/fruitSprite.png'          # Cite: https://www.pngjoy.com/fullpng/s1w8b4e6u3o0q0/
    food = 'images/food.jpg'                     # Cite: https://www.spriters-resource.com/wii/cookingmamacookoff/sheet/68468/
    mode2 = 'images/mode2.jpg'                   # Cite: https://wallpaperset.com/stars-in-the-sky-wallpaper
    self.backgroundImg = self.loadImage(background)
    self.backgroundScale = self.scaleImage(self.backgroundImg, 1)
    self.clearBackgroundImg = self.loadImage(clearBackground)
    self.clearBackgroundScale = self.scaleImage(self.clearBackgroundImg, 1)
    self.conditionsImg = self.loadImage(conditionsBG)
    self.conditionsScale = self.scaleImage(self.conditionsImg, 1)
    self.inputFoodImg = self.loadImage(inputFoodBG)
    self.inputFoodScale = self.scaleImage(self.inputFoodImg, 1)
    self.notSafeImg = self.loadImage(notSafeBG)
    self.notSafeScale = self.scaleImage(self.notSafeImg, 1)
    self.safeImg = self.loadImage(safeBG)
    self.safeScale = self.scaleImage(self.safeImg, 1)
    self.notFoundImg = self.loadImage(notFound)
    self.notFoundScale = self.scaleImage(self.notFoundImg, 1)
    self.foodImg = self.loadImage(food)
    self.foodScale = self.scaleImage(self.foodImg, 1)
    self.mode2Img = self.loadImage(mode2)
    self.mode2Scale = self.scaleImage(self.mode2Img, 1)
    self.fruitStripImg = self.loadImage(fruitImg)
    self.fruitStrip = self.scaleImage(self.fruitStripImg, 1)
    self.fruitWidth = self.fruitStrip.width/13
    self.fruitHeight = self.fruitStrip.height - 200
    self.fruitList = [ ]
    for i in range(13): # fruit img
        fruit = self.fruitStrip.crop((self.fruitWidth*i, 0, self.fruitWidth*(i+1), self.fruitHeight))
        self.fruitList.append(fruit)

def rgbString(r, g, b):  # Cite: https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return f'#{r:02x}{g:02x}{b:02x}'

##############  Home Page ##############
def homePressed(self, event): # pressed any button on home 
    if 110 <= event.x and event.x <= 370 and 500 <= event.y and event.y <= 600 and \
        self.state == 'home':
        self.state = self.pages[1]  
    elif 400 <= event.x and event.x <= 640 and 500 <= event.y and event.y <= 600 and \
        self.state == 'home':
        self.intakeState = self.intakePages[1]
    elif 660 <= event.x and event.x <= 890 and 500 <= event.y and event.y <= 600 and \
        self.state == 'home':
        self.state = self.pages[2] 

def drawFruitImg(self, canvas):
    fruit = self.fruitList[self.fruitCounter]
    canvas.create_rectangle(530-self.fruitWidth/2, 330-self.fruitHeight/2, \
                            530+self.fruitWidth/2, 330+self.fruitHeight/2, fill = 'white', width = 10)
    canvas.create_image(530, 330, image=ImageTk.PhotoImage(fruit))

def drawHome(self, canvas):
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.backgroundScale))
    canvas.create_rectangle(110, 500, 370, 600, fill = rgbString(214, 248, 255), width = 3)
    canvas.create_rectangle(400, 500, 640, 600, fill = rgbString(214, 248, 255), width = 3)
    canvas.create_rectangle(660, 500, 890, 600, fill = rgbString(214, 248, 255), width = 3)
    canvas.create_text(240, 550, text="Ingredient Checker", font='Arial 20 bold', fill=rgbString(117,94,94))
    canvas.create_text(520, 550, text='Intake Checker', font='Arial 22 bold', fill=rgbString(117,94,94))
    canvas.create_text(775, 550, text='Instructions', font='Arial 22 bold', fill=rgbString(117,94,94))
    drawFruitImg(self, canvas)

############## Instructions Page ##############
def instructionsPressed(self, event):  
    if self.width/2-150 <= event.x and event.x <= self.width/2+150 and 510 <= event.y and event.y <= 610:
        self.state = self.pages[0]

def drawInstructions(self, canvas):
    text = foodData.drawInstructionsText()
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.clearBackgroundScale))
    canvas.create_text(self.width/2, self.height/4, text="Instructions", anchor="s",
                    fill="black", font="Times 40 bold italic")
    canvas.create_rectangle(200, 200, 800, 480, fill = 'white')
    canvas.create_text(500, 330, text = text, font = 'Arial 13 bold')
    canvas.create_rectangle(self.width/2-150, 510, self.width/2+150, 610, \
                            fill = 'white', width = 3)
    canvas.create_text(self.width/2, 560, text="Return Home", font='Arial 18 bold', fill='black')
    
############## Ask Name Page ##############
def askName(self, event):
    getUserInfo.namePressed(self, event)
    if getUserInfo.matchNames(self):
        self.state = self.pages[8]
    else:
        self.state = self.pages[3]

def drawAskName(self, canvas):
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.clearBackgroundScale))
    canvas.create_text(self.width/2, self.height/5, text="The Food Mentor", anchor="s",
                fill="white", font="Times 60 bold italic")
    # canvas.create_text(self.width/2, self.height/2, text='Enter your name: ', fill='black', font='Times 25 bold')
    # canvas.create_rectangle(self.width/2-100, self.height/2+50, self.width/2+100, self.height/2+100, fill='white')
   

############## Conditions Page ##############
def conditionsPressed(self, event):
    if 250 <= event.x and event.x <= 750 and 150 <= event.y and event.y <= 200:
        self.hasCondition[0] = not self.hasCondition[0]
    elif 250 <= event.x and event.x <= 750 and 200 <= event.y and event.y <= 250:
        self.hasCondition[1] = not self.hasCondition[1]
    elif 250 <= event.x and event.x <= 750 and 250 <= event.y and event.y <= 300:
        self.hasCondition[2] = not self.hasCondition[2]
    elif 250 <= event.x and event.x <= 750 and 300 <= event.y and event.y <= 350:
        self.hasCondition[3] = not self.hasCondition[3]
    elif 250 <= event.x and event.x <= 750 and 350 <= event.y and event.y <= 400:
        self.hasCondition[4] = not self.hasCondition[4]
    elif 250 <= event.x and event.x <= 750 and 400 <= event.y and event.y <= 450:
        self.hasCondition[5] = not self.hasCondition[5]
    elif 250 <= event.x and event.x <= 750 and 450 <= event.y and event.y <= 500:
        self.hasCondition[6] = not self.hasCondition[6]
    if submitPressed(self, event):
        self.state = self.pages[4]

def submitPressed(self, event): 
    if self.width/2-150 <= event.x and event.x <= self.width/2+150 and 540 <= event.y \
        and event.y <= 610:
        return True
    return False

def drawSubmitButton(self, canvas):
    canvas.create_rectangle(self.width/2-150, 540, self.width/2+150, 610, \
                            fill = 'white', width = 3)
    canvas.create_text(self.width/2, 575, text="Submit", font='Arial 22 bold', fill='black')

def drawConditions(self, canvas):
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.conditionsScale))
    for c in range(len(self.listOfCond)): # 7
        if self.hasCondition[c] == False:
            canvas.create_rectangle(250, 150+50*c, 750, 200+50*c, fill = 'white', width = 2)
        else:
            canvas.create_rectangle(250, 150+50*c, 750, 200+50*c, fill = 'lightblue', width = 2)
        canvas.create_text(500, 175+50*c, text = self.listOfCond[0+c], font = 'Arial 15 bold')
    drawSubmitButton(self, canvas)

############## Enter Food Page ##############
def enterFoodPressed(self, event):
    getUserInfo.userInputFood(self)
    self.state = self.pages[5]

def drawEnterFood(self, canvas):
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.inputFoodScale))

############## Scan Barcode ##############
def scanning(self):
    scanner.runBarcode(self)
    webscraping.webscrapUSDA(self)
    if self.productName == '':  # no product
        self.state = self.pages[7]
    else:
        foodData.isSafe(self)
        self.state = self.pages[6]

def drawScanBarcode(self, canvas):
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.clearBackgroundScale))
    canvas.create_text(self.width//2, self.height//2, text = "Press 'B' to start scanning your product's barcode!", \
                        font = 'Arial 23 bold', fill = 'white')

############## Result Page ##############
def scanMore(self):
    self.scanUPC = self.productName = ''
    self.dataUSDA = set()  
    self.inputIngredients = set()
    self.safe = True
    self.unsafeList = self.unsafeFromCondition = self.unsafeFromInput = []

def drawResult(self, canvas):
    if self.safe == False:
        canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.notSafeScale))
        canvas.create_text(self.width//2, 310, text = "This product includes: ", font = 'Arial 20 bold', \
                            fill = 'white')
        for num in range(len(self.unsafeList)):
            canvas.create_text(self.width//2, 360+20*num, text = f'{self.unsafeList[num]}\n', \
            font = 'Arial 15 bold', fill = 'white')
        canvas.create_text(self.width//2, 500, text = "Press 'S' to scan more!", \
                            font = 'Arial 18 bold') 
        drawExitButton(self, canvas) 
    else:
        canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.safeScale))
        canvas.create_text(self.width//2, 450, text = "Press 'S' to scan more!", \
                            font = 'Arial 25 bold')
        drawExitButton(self, canvas)

def drawExitButton(self, canvas):
    canvas.create_rectangle(self.width-75, 3, self.width-3, 50, fill = 'light gray', width = 3)
    canvas.create_text(self.width-39, 29, text='Exit', fill=rgbString(117,94,94), font='Arial 15 bold')
    
############## Not Found ##############
def userIngredients(self):
    getUserInfo.getUserIngredients(self)
    foodData.isSafe(self)
    self.state = self.pages[6]
    getUserInfo.developFile(self)

def drawNotFound(self, canvas):
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.notFoundScale))

############## Past ################
def pastPressed(self, event):
    if 700 <= event.x and event.x <= 800 and 430 <= event.y and event.y <= 480: # update 
        self.state = self.pages[3]
    if 700 <= event.x and event.x <= 800 and 150 <= event.y and event.y <= 200: # start scan
        getUserInfo.matchPastData(self)
        self.state = self.pages[5]

def drawPast(self, canvas):
    canvas.create_rectangle(0, 0, self.width, self.height, fill = 'yellow')
    canvas.create_rectangle(150, 150, 800, 480, fill = 'white', width = 2)
    canvas.create_text(500, 330, text = str(self.text), fill = 'black', font = 'Arial 11 bold')
    canvas.create_rectangle(700, 430, 800, 480, fill = rgbString(214, 248, 255), width = 2)
    canvas.create_text(750, 455, text = 'Update', fill = rgbString(117,94,94), font = 'Arial 14 bold')
    drawExitButton(self, canvas)
    drawSave(self, canvas)

def drawSave(self, canvas):
    canvas.create_rectangle(700, 150, 800, 200, fill = rgbString(214, 248, 255), width = 2)
    canvas.create_text(750, 175, text = 'Save', fill = rgbString(117,94,94), font = 'Arial 14 bold')