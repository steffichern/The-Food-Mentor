import requests

### Extracted data from the USDA website: https://fdc.nal.usda.gov/  ###

   
def checkExist(self):  # checks if the product is in the database
    upc = self.scanUPC
    while True:
        # response = requests.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query={upc}&pageSize=1")
        response = requests.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=kibddkSu8H15C96E5k3LmIqWGb06ekeDTIwQ2q0v&query={upc}&pageSize=1")
        try: 
            data = response.json()   # returns dict in key value pairs
            if data['totalHits'] == 0:  # product not found
                return None
            elif data['totalHits'] == 1:
                return data
        except:
            pass

def webscrapUSDA(self):   # for food checker
    data = checkExist(self)
    if data == None: 
        self.state = self.pages[7]
        return

    allIngredients = data['foods'][0]['ingredients']
    self.productName = data['foods'][0]['description']

    irrelevant = ['.','AND', ':','&','(',')','MADE FROM']
    # when only one ingredient, remove the period
    if ',' not in allIngredients:  
        self.dataUSDA = {allIngredients.replace('.','')}

    # remove irrelevant symbols for improving accuracy
    for ingredient in allIngredients.split(','):
        for ir in irrelevant:
            ingredient = ingredient.strip()
            if ir in ingredient:
                ingredient = ingredient.replace(ir, '').strip()
        self.dataUSDA.add(ingredient)
    print(self.dataUSDA)

def getDetailsUSDA(self):   # get calories and macros by scanning
    data = checkExist(self)
    if data != None:
        self.getCals = (data['foods'][0]['foodNutrients'][3]['value'])
        self.getCarbs = (data['foods'][0]['foodNutrients'][2]['value'])
        self.getProtein = (data['foods'][0]['foodNutrients'][0]['value'])
        self.getFat = (data['foods'][0]['foodNutrients'][1]['value'])  
        
            