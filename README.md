# The-Food-Mentor
* Short description of what the project does:
   * The application features two powerful modes: the 'Ingredient Checker' and the 'Intake Checker,' designed to enhance your dietary awareness and support your health goals.
     With the 'Ingredient Checker,' effortlessly scan the food products you have or manually enter specific food items while considering your unique dietary needs and allergens.
     The system intelligently analyzes the ingredients, providing valuable insights on which foods you should or shouldn't consume. It precisely highlights the specific ingredients
     that may not align with your dietary restrictions or preferences, empowering you to make informed choices. In the 'Intake Checker' mode, simply scan the barcode of your food items
     to uncover essential nutritional information. Delve into details such as calories, carbohydrates, protein, and fat content, gaining a comprehensive understanding of your macros
     intake. The system then generates insightful graphs, presenting a clear visualization of your progress towards your dietary goals. Additionally, a curated recommendation list of
     suitable food options is provided to assist you in maintaining an optimal balance and staying on track with your calorie objectives.
   * Goal: gain deeper understanding of the foods consumed, enabling people to make healthier choices that align with their individual dietary needs and goals.
     Good for people managing allergies, striving for weight management, or simply seeking a balanced lifestyle.
* How to run the project: 
   * Run the main.py file in the python editor
   * The ‘images’ (with all the images), ‘User Database’ (an empty folder), and ‘Recs’ (with myRecs.txt) folder should be ready under the same folder with all the other .py files
   * The ‘conditions.txt’  and ‘myRecs.txt’ need to be saved in the correct folder (‘conditions.txt’ is located in the same folder as all the other .py files, whereas ‘myRecs.txt’ is under the ‘Recs’ folder)
      * I.e. “...(directory) / main.py”  & “...(directory) / conditions.txt”  &  ‘’...(directory) / Recs / myRecs.txt”
* Libraries used: 
   * Below is what you should install through your terminal
      * pip3 install --upgrade opencv-python
      * pip install pyzbar
      * pip install requests
* Short Commands:
   * For the “Intake Checker” mode, when you reach the graph about ‘weight maintain’, press “1” to see the next slide about ‘lose weight’. When you reach the graph about ‘lose weight’, press ‘2’ to see the next graph about ‘gain weight’. When you reach ‘gain weight’, press ‘3’ to see the food recommendation list.
