import datetime
import startings
import os

def namePressed(self, event):  # requires user to enter a name
    while True:
        response = self.getUserInput('Enter your name: ')
        try:
            self.name = str(response)
            if self.name == '':
                self.showMessage('You did not enter a name! Please try again.')
            else:
                return
        except:
                self.showMessage('Not a valid name! Please try again!')


   
def userInputFood(self):  # add food by user
    inputFood = self.getUserInput("Enter other specific food you can't/don't want to eat: ")

    if inputFood == '':  # no input
        self.inputFood = set()
    if ',' not in inputFood and inputFood != '':  # only one food input
        inputFood = inputFood.strip().upper()
        self.inputFood = {inputFood}
    elif ',' in inputFood and inputFood != '':  # multiple food input
        for food in inputFood.split(','):
            food = food.strip().upper()
            self.inputFood.add(food)

def getUserIngredients(self):
    getProductName(self)
    while True:
        ingredients = self.getUserInput('Enter the ingredients in the product: ')
        try:
            ingredients = str(ingredients)
            if ingredients == '':
                self.showMessage('Please enter something!')
            else:
                formatInput(self, ingredients)
                return
        except:
                self.showMessage('Not a valid ingredient!')

def getProductName(self):
    while True:
        product = self.getUserInput("Enter the product's name: ")
        try:
            product = str(product)
            if product == '':
                self.showMessage('Please enter something!')
            else:
                self.productName = product
                return
        except:
                self.showMessage('Not a valid ingredient!')

def formatInput(self, ingredients):
    if ',' not in ingredients:  # user did not enter commas
        ingredients = ingredients.strip().upper()
        self.inputIngredients.add(ingredients)
    elif ',' in ingredients:  # user entered commas
        for ingr in ingredients.split(','):
            ingr = ingr.strip().upper()
            self.inputIngredients.add(ingr)
        return

# build profile for user
def developFile(self): 
    with open(f"{self.directory}/{self.name}.txt", "w+") as file:   # make filename the same as username
        file.write(f"Hi {self.name}! Nice to see you again! Here's what we have for you... \n\n")
        file.write("Your past conditions: \n")
        for ind in range(len(self.listOfCond)):
            
            if self.hasCondition[ind] == True:
                file.writelines(f"{self.listOfCond[ind]}\n") 

        file.write("\nYour past food inputs: \n")
        if self.inputFood != set():
            for food in self.inputFood:
                file.writelines(f"{food} \n")
        else:       
            file.write('None \n' )
            
        # Cite: https://stackoverflow.com/questions/7999935/python-datetime-to-string-without-microsecond-component
        file.write(f'\nLast product you scanned on {datetime.datetime.now().replace(microsecond = 0)}: \n')
        if self.safe == True: 
            answer = 'Good to eat!'
        else: 
            answer = 'Not good to eat!'
        file.writelines(f'{self.productName} ~~ {answer}')
    
    
    file.close()

# recursively list out all the possible files
def getPastFiles(directory):
    if os.path.isfile(directory):
        return [directory]

    elif os.path.isdir(directory):
        directories = os.listdir(directory)
        filenames = []
        for index in range(len(directories)):
            filenames += (getPastFiles(directory + '/' + directories[index]))
        return filenames

def matchNames(self): # search all available txt files and see if the name is there
    directories = getPastFiles(self.directory)
    fullName = str(self.directory + '/' + self.name + '.txt')
    for i in range(len(directories)):  
        if fullName == directories[i]:
            text = open(directories[i], "r")
            self.text = text.read() # in strings for printing 
            text.close()
            return True
    return False

def matchPastData(self): # retrieve data
    lineList = []
    countConditions = 0
    with open(f"{self.directory}/{self.name}.txt", "r") as file:
        words = file.readlines()
        for word in words:
            word = word.replace('\n', '').strip()
            lineList += [word]
        
        for i in range(3, len(lineList)-2):  # ignore first 3 lines and last 2 lines
            for ind in range(len(self.listOfCond)):
                if lineList[i] == self.listOfCond[ind]: # map condition
                    countConditions += 1
                    self.hasCondition[ind] = True

        for j in range(countConditions+3, len(lineList)-2): # map inputfood
            if lineList[j] == 'Your past food inputs:' or lineList[j] =='':
                continue
            else:
                self.inputFood.add(lineList[j])
    file.close()   
                    
                
                    
                  


            
