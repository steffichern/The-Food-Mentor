* A short description of the project's name and what it does. 
   * Project’s Name: The Food Mentor
   * What it does: It has 2 main modes, one called ‘Ingredient Checker’ and the other called ‘Intake Checker’. For ‘Ingredient checker’, it allows users to scan the food product they have and select their food conditions/allergens or manually enter other food that they don’t want/can’t eat. The system will then check if the user should/shouldn’t eat and list out what exactly (the specific food ingredients) is in the food product that the user should avoid. For ‘Intake Checker’, it also allows the user to scan their food’s barcode, but this time checking their calories and macros (carbs, protein, fat) intake. Based on that, the system checks and displays graphs of how the user is doing with their intake. There’s a recommendation list of food in the end for users to see what other food they can eat to stay on track of their calories goal.
* How to run the project. 
   * Run the main.py file in the python editor
   * The ‘images’ (with all the images), ‘User Database’ (an empty folder), and ‘Recs’ (with myRecs.txt) folder should be ready under the same folder with all the other .py files
   * The ‘conditions.txt’  and ‘myRecs.txt’ need to be saved in the correct folder (‘conditions.txt’ is located in the same folder as all the other .py files, whereas ‘myRecs.txt’ is under the ‘Recs’ folder)
      * I.e. “...(directory) / main.py”  & “...(directory) / conditions.txt”  &  ‘’...(directory) / Recs / myRecs.txt”
* Which libraries you're using that need to be installed, if any. 
   * Below is what you should install through your command prompt
      * pip3 install --upgrade opencv-python
      * pip install pyzbar
      * pip install requests
* A list of any shortcut commands that exist. 
   * For the “Intake Checker” mode, when you reach the graph about ‘weight maintain’, press “1” to see the next slide about ‘lose weight’. When you reach the graph about ‘lose weight’, press ‘2’ to see the next graph about ‘gain weight’. When you reach ‘gain weight’, press ‘3’ to see the food recommendation list.