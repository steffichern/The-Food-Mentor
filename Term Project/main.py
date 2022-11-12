#####################################
# Term Project 15-112
# Title: The Food Mentor
# Name: Steffi Chern (steffic)
#####################################
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

def appStarted(self):
    startings.initializations(self)
    startings.images(self)


def timerFired(self): # for moving fruit img
    self.fruitCounter = (self.fruitCounter+1) % len(self.fruitList)

def exitButtonPressed(self, event): 
    if self.width-75 <= event.x and event.x <= self.width-3 and 3 <= event.y and event.y <= 50:
        appStarted(self)

#####################   
def mousePressed(self, event):
    if self.state == 'home':
        startings.homePressed(self, event)
    if self.state == 'instructions':
        startings.instructionsPressed(self, event)
    if self.state == 'askName':
        startings.askName(self, event)
    if self.state == 'conditions':
        startings.conditionsPressed(self, event)
    if self.state == 'enterFood':
        startings.enterFoodPressed(self, event)
    if self.state == 'result':
        exitButtonPressed(self, event)
    if self.state == 'past':
        startings.pastPressed(self, event)
        exitButtonPressed(self, event)
    if self.intakeState == 'basic info':
        intakeChecker.getBasicInfo(self, event)
    if self.intakeState == 'inputGrams':
        intakeChecker.getGrams(self, event)
    if self.intakeState == 'recommendations':
        exitButtonPressed(self, event)
   
    
def keyPressed(self, event):
    if self.state == 'scanBarcode' and event.key == 'b':  
        startings.scanning(self)
    if self.state == 'notFound':
        startings.userIngredients(self)
    if self.state == 'result':   
        getUserInfo.developFile(self)
        if event.key == 's':  # scan more products
            startings.scanMore(self)
            self.state = self.pages[5]
    if self.intakeState == 'display1' and event.key.isnumeric() and event.key == '1':  # to see next slide
        self.intakeState = self.intakePages[4]
    if self.intakeState == 'display2' and event.key.isnumeric() and event.key == '2':
        self.intakeState = self.intakePages[5]
    if self.intakeState == 'display3'and event.key.isnumeric() and event.key == '3':
        self.intakeState = self.intakePages[6]
    if self.intakeState == 'recommendations':
        intakeChecker.recs(self)
        if event.key == 'r':
            intakeChecker.recs(self)
            
   
def redrawAll(self, canvas):
    if self.state == 'home':
        startings.drawHome(self, canvas)
    if self.state == 'askName':
        startings.drawAskName(self, canvas)
    if self.state == 'instructions':
        startings.drawInstructions(self, canvas)
    if self.state == 'conditions':
        startings.drawConditions(self, canvas)
    if self.state == 'enterFood':
        startings.drawEnterFood(self, canvas)
    if self.state == 'scanBarcode':
        startings.drawScanBarcode(self, canvas)
    if self.state == 'notFound':
        startings.drawNotFound(self, canvas)
    if self.state == 'result':
        startings.drawResult(self, canvas)
    if self.state == 'past':
        startings.drawPast(self, canvas)
    if self.intakeState == 'basic info':
        intakeChecker.drawBasicInfo(self, canvas)
    if self.intakeState == 'inputGrams':
        intakeChecker.drawGrams(self, canvas)
    if self.intakeState == 'display1':
        intakeChecker.drawDisplay1(self, canvas)
    if self.intakeState == 'display2':
        intakeChecker.drawDisplay2(self, canvas)
    if self.intakeState == 'display3':
        intakeChecker.drawDisplay3(self, canvas)
    if self.intakeState == 'recommendations':
        intakeChecker.drawRecs(self, canvas)
    

def main():
    runApp(width=1000, height=650)

if __name__ == '__main__':
    main()
    




