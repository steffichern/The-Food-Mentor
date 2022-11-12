from cmu_112_graphics import *
import startings
import scanner
import webscraping
import getUserInfo
import calculations
import requests
import cv2
from pyzbar import pyzbar



######### Basic info ##########
def getBasicInfo(self, event):
    calculations.basicInfo(self)
    calculations.calculateRecs(self)
    self.intakeState = self.intakePages[2]
    scanner.runBarcode(self)
    if webscraping.checkExist(self) != None: 
        webscraping.getDetailsUSDA(self)
        calculations.askGrams(self)
            
            
            

def background(self, canvas):
    canvas.create_rectangle(0, 0, self.width, self.height, fill = 'light gray')

def drawBasicInfo(self, canvas):
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.mode2Scale))
    canvas.create_text(self.width//2, 100, text = 'Basic Info', fill = 'lavender', font = 'Arial 40 bold')


############## Input Grams ################
def getGrams(self, event): 
    if self.width-150 <= event.x and event.x <= self.width-10 and self.height-60 \
        <= event.y and event.y <= self.height: # to show display
        calculations.userConsumed(self)
        self.intakeState = self.intakePages[3]
        
    if self.width-340 <= event.x and event.x <= self.width-180 and self.height-60 \
        <= event.y and event.y <= self.height: # to scan more
        calculations.accumulate(self)
        calculations.scanMore(self)
        scanner.runBarcode(self) 
        webscraping.getDetailsUSDA(self)
        calculations.askGrams(self)

def drawGrams(self, canvas):
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.mode2Scale))
    canvas.create_text(self.width//2, 100, text = 'Enter grams', fill = 'lavender', font = 'Arial 40 bold')
    canvas.create_rectangle(self.width-150, self.height-60, self.width-10, self.height, fill = 'white', width = 2)
    canvas.create_text(self.width-80, self.height-30, text = "See Results",  
                        fill = 'black', font = 'Arial 15 bold')
    canvas.create_rectangle(self.width-340, self.height-60, self.width-180, self.height, fill = 'white', width = 2)
    canvas.create_text(self.width-260, self.height-30, text = "Scan More",  
                        fill = 'black', font = 'Arial 15 bold')
############## Display 1, weight maintain ################

def draw1(self, canvas, cals, carbs, protein, fat, color): # the common parts for each display 
    background(self, canvas)
    text = ['Calories', 'Carbs', 'Protein', 'Fat']
    for i in range(len(text)):
        canvas.create_text(170, 150+i*100, text = text[i], fill = color[i], font = 'Helvetica 22 bold underline')
        canvas.create_rectangle(250, 125+i*100, 750, 175+i*100, fill = 'white' )
    canvas.create_rectangle(250, 125, 250+(cals*500), 175, fill = color[0], width = 0)
    canvas.create_rectangle(250, 225, 250+(carbs*500), 275, fill = color[1], width = 0)
    canvas.create_rectangle(250, 325, 250+(protein*500), 375, fill = color[2], width = 0)
    canvas.create_rectangle(250, 425, 250+(fat*500), 475, fill = color[3], width = 0)
    canvas.create_line(250, 100, 250, 500, fill = 'black', width = 4)

def draw2(self, canvas, caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed, projectCals, gramsOfCarbs, gramsOfProtein, gramsOfFat):
    canvas.create_text(850, 150, text = f'{caloriesConsumed}/{projectCals} kcal', font = 'Helvetica 15 bold') 
    canvas.create_text(850, 250, text = f'{carbsConsumed}/{gramsOfCarbs} grams', font = 'Helvetica 15 bold')
    canvas.create_text(850, 350, text = f'{proteinConsumed}/{gramsOfProtein} grams', font = 'Helvetica 15 bold')
    canvas.create_text(850, 450, text = f'{fatConsumed}/{gramsOfFat} grams', font = 'Helvetica 15 bold')
    

def drawDisplay1(self, canvas):  
    color = ['red', 'blue', 'orange', 'green']
    projectCarbs, projectProtein, projectFat = calculations.maintainMacros(self)
    caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed = calculations.userConsumed(self)
    # fill color based on percentage, convert all to kcal
    cals = caloriesConsumed/self.projectCals
    carbs = (carbsConsumed*4)/self.projectCals  # 4kcal/g
    protein = (proteinConsumed*4)/self.projectCals # 4kcal/g
    fat = (fatConsumed*9)/self.projectCals   # 9kcal/g
    draw1(self, canvas, cals, carbs, protein, fat, color)
    canvas.create_text(500, 580, text = 'Maintain Weight', font = 'Helvetica 25 bold')  

    # draw text of how far from recommneded goal
    projectCals = round(self.projectCals, 2)
    gramsOfCarbs, gramsOfProtein, gramsOfFat = calculations.projMaintainGrams(self)
    draw2(self, canvas, caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed, projectCals, gramsOfCarbs, gramsOfProtein,gramsOfFat)

# def drawNext(self, canvas):

############## Display 2, loss weight ################
def drawDisplay2(self, canvas):
    color = ['red', 'blue', 'orange', 'green']
    projectCarbs, projectProtein, projectFat = calculations.lossMacros(self)
    caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed = calculations.userConsumed(self)  
   
    # fill color based on percentage, convert all to kcal
    cals = caloriesConsumed/(self.projectCals*0.75)   # based on loss weight, projected cals is smaller
    carbs = (carbsConsumed*4)/(self.projectCals*0.75)  
    protein = (proteinConsumed*4)/(self.projectCals*0.75) 
    fat = (fatConsumed*9)/(self.projectCals*0.75)  
    draw1(self, canvas, cals, carbs, protein, fat, color)
    canvas.create_text(500, 580, text = 'Lose Weight', font = 'Helvetica 25 bold')
    # how far from recommneded goal
    projectCals = round(self.projectCals*0.75, 2)
    gramsOfCarbs, gramsOfProtein, gramsOfFat = calculations.projLossGrams(self)
    draw2(self, canvas, caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed, projectCals, gramsOfCarbs, gramsOfProtein,gramsOfFat)

############## Display 3, gain weight ##########
def drawDisplay3(self, canvas):
    color = ['red', 'blue', 'orange', 'green']
    projectCarbs, projectProtein, projectFat = calculations.gainMacros(self)
    caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed = calculations.userConsumed(self)
    
    # convert all to kcal
    cals = caloriesConsumed/(self.projectCals*1.3)   # based on gain weight, projected cals is higher
    carbs = (carbsConsumed*4)/(self.projectCals*1.3)  
    protein = (proteinConsumed*4)/(self.projectCals*1.3)
    fat = (fatConsumed*9)/(self.projectCals*1.3)
    draw1(self, canvas, cals, carbs, protein, fat, color)
    canvas.create_text(500, 580, text = 'Gain Weight', font = 'Helvetica 25 bold')  
    
    projectCals = round(self.projectCals*1.3, 2)
    gramsOfCarbs, gramsOfProtein, gramsOfFat = calculations.projGainGrams(self)
    draw2(self, canvas, caloriesConsumed, carbsConsumed, proteinConsumed, fatConsumed, projectCals, gramsOfCarbs, gramsOfProtein,gramsOfFat)

############## Recs ##########
def rgbString(r, g, b):  # Cite: https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return f'#{r:02x}{g:02x}{b:02x}'

def recs(self):
    calculations.storeRecs(self)
    calculations.recListToStr(self)
def drawRecs(self, canvas):  
    canvas.create_rectangle(0,0, self.width, self.height, fill = 'white')
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.foodScale))
    canvas.create_rectangle(200, 150, 800, 480, fill = rgbString(230, 169, 2), width = 2)
    canvas.create_text(self.width//2, 175, text = 'Your Recommendation List', font = 'Arial 20 underline bold', fill = 'brown' )
    canvas.create_text(500, 320, text = str(self.recs), font = 'Arial 15 bold')
    startings.drawExitButton(self, canvas)
    