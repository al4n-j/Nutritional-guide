from flask import Flask, render_template, request,redirect,url_for,flash
import pymysql
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf
from PIL import Image
import csv

ussr='hj'
conn = pymysql.connect( 
	host='localhost', 
	user='root', 
	password = "", 
	db='nutritional_guide', 
	) 
	
cur = conn.cursor() 

app = Flask(__name__)
app.config['SECRET_KEY'] = "kjboujbjubsdfgsdfgs"
from tensorflow.keras.models import load_model

# Load your trained model with error handling
try:
    model_path = 'C:/Users/blind/Programs/Projects/Nutritional_guide/fruits_veg_trained_model.h5'
    model = load_model(model_path)
except Exception as e:
    print("Error loading the model:", e)


@app.route('/upload')
def upload():
    return render_template('upload1.html')

@app.route('/',methods=['GET','POST'])
def login():
    global ussr
    if request.method == 'POST':
        usr = request.form.get("username")
        ussr=usr        
        print(usr)
        pswrd = request.form.get("password")
        print(pswrd)
        cur.execute(f"select password from allergy where username ='{usr}';")
        res = cur.fetchall()
        if len(res)==0:
            flash("Username not valid")
            return redirect(url_for('create'))
        if pswrd==res[0][0]:
            if ussr=="admin@a5":
                return redirect(url_for('admin'))
            else :
                return redirect(url_for('upload'))
        else:
            flash("Password invalid")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/create',methods=['GET','POST'])   
def create():
    global ussr
    if request.method == 'POST':
        usr = request.form.get("username")
        print(usr)
        ussr=usr
        name = request.form.get("name")
        psd = request.form.get("password")
        cur.execute(f"select password from allergy where username ='{usr}';")
        res = cur.fetchall()
        if len(res)==0:
            cpsd = request.form.get("confirmPassword")
            if psd==cpsd:
                pollen = request.form.get('pollen')
                pollen.lower()
                latex = request.form.get('latex')
                latex.lower()
                brichpollen = request.form.get('brichpollen')
                brichpollen.lower()
                citrus = request.form.get('citrus')
                citrus.lower()
                grasspollen = request.form.get('grasspollen')
                grasspollen.lower()
                soy = request.form.get('soy')
                soy.lower()
                nightshade = request.form.get('nightshade')
                nightshade.lower()
                mugwortpollen = request.form.get('mugwortpollen')
                mugwortpollen.lower()
                cur.execute(f"insert into allergy values ('{usr}','{brichpollen}','{citrus}','{grasspollen}','{latex}','{mugwortpollen}','{nightshade}','{pollen}','{soy}','{psd}','{name}');")
                conn.commit()
                flash("New user created")
                return redirect(url_for('login'))
            else :
                flash("Password not matched")
        else:
            flash("User already exist")
            return redirect(url_for('login'))
    return  render_template("create1.html")

@app.route('/home')
def home():
    cur.execute(f"select name from allergy where username='{ussr}';")
    nam=cur.fetchone()
    cur.execute(f"select birch_pollen,citrus,grass_pollen,latex,mugwort_pollen,nightshade, pollen,soy from allergy where username='{ussr}';")
    na=cur.fetchall()

    return render_template("home.html",na=na,user=ussr,nam=nam[0])

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img = Image.open(file.stream)
        image = img.resize((64,64))
        #input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([image]) # Converting single image to batch
        prediction = model.predict(input_arr)
        test_set=tf.keras.utils.image_dataset_from_directory('C:/Users/blind/Programs/Projects/Nutritional_guide/test',
                                                         labels='inferred',
                                                         label_mode='categorical',
                                                         class_names=None,
                                                         color_mode='rgb',
                                                         batch_size=32,
                                                         image_size=(64,64),
                                                         shuffle =True,
                                                         seed=None,
                                                         validation_split=None,
                                                         subset=None,
                                                         interpolation='bilinear',
                                                         follow_links=False,
                                                         crop_to_aspect_ratio=False
                                                         )
        result_index = np.where(prediction[0]==max(prediction[0]))
        print(result_index[0][0])
        print('It is a {}'.format(test_set.class_names[result_index[0][0]]))
        predict = test_set.class_names[result_index[0][0]]
        """img = img.resize((64, 64))  # Resize image to match model input size
        img_array = np.array(img)
        img_array = img_array / 255.0  # Normalize image data
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        prediction = model.predict(img_array)
        result_index = np.where(prediction[0]==max(prediction[0]))
        print(result_index[0][0])
        predict=set[result_index[0][0]]"""
        cur.execute(f"select * from allergy where username ='{ussr}';")
        res = cur.fetchall()
        print("user=",ussr)
        print("result=",res)
        #print(res[0])
        #print(res[0][2])
        def check_word(file_path, word):
            try:
                with open(file_path, 'r') as file:
                    # Read the entire contents of the file
                    contents = file.read()
                    # Check if the word is in the file
                    if word in contents:
                        return True
                    else:
                        return False
            except FileNotFoundError:
                print("File not found.")
                return False
        reccomendation = "No allergies detected."
        c1='C:/Users/blind/Programs/Projects/Nutritional_guide/allergy/Birch_Pollen_allergy.txt'
        c2='C:/Users/blind/Programs/Projects/Nutritional_guide/allergy/citrus_allergy.txt'
        c3='C:/Users/blind/Programs/Projects/Nutritional_guide/allergy/grass_pollen_allergy.txt'
        c4='C:/Users/blind/Programs/Projects/Nutritional_guide/allergy/latex_allergy.txt'
        c5='C:/Users/blind/Programs/Projects/Nutritional_guide/allergy/mugwort_pollen_allergy.txt'
        c6='C:/Users/blind/Programs/Projects/Nutritional_guide/allergy/Nightshade_sensitivity.txt'
        c7='C:/Users/blind/Programs/Projects/Nutritional_guide/allergy/pollen_allergies.txt'
        c8='C:/Users/blind/Programs/Projects/Nutritional_guide/allergy/soy_allergy.txt'
        allergy=''
        if len(res)!=0:
            if res[0][1]=='True':
                if check_word(c1, predict):
                    allergy+='Birch Pollen allergy '
                    reccomendation ="Not Reccomended"
            if res[0][2]=='True':
                if check_word(c2, predict):
                    allergy+='Citrus allergy '
                    reccomendation ="Not Reccomended"
            if res[0][3]=='True':
                if check_word(c3, predict):
                    allergy+='Grass pollen allergy '
                    reccomendation ="Not Reccomended"
            if res[0][4]=='True':
                if check_word(c4, predict):
                    allergy+='Latex allergy '
                    reccomendation ="Not Reccomended"
            if res[0][5]=='True':
                if check_word(c5, predict):
                    allergy+='Mugwort pollen allergy '
                    reccomendation ="Not Reccomended"
            if res[0][6]=='True':
                if check_word(c6, predict):
                    allergy+='Nightshade sensitivity '
                    reccomendation ="Not Reccomended"
            if res[0][7]=='True':
                if check_word(c7, predict):
                    allergy+='Pollen allergy '
                    reccomendation ="Not Reccomended"
            if res[0][8]=='True':
                if check_word(c8, predict):
                    allergy+='Soy allergy '
                    reccomendation ="Not Reccomended"
        else:
            flash("User timed out")
            return redirect(url_for('login'))

        def extract_info(food_name):
            with open('C:/Users/blind/Programs/Projects/Nutritional_guide/fruits_and_vegetables_calorie.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Food'].lower() == food_name.lower():
                        return row
                return None

        food_name = predict
        food_info = extract_info(food_name)
        if food_info:
            print(f"Nutritional information for {food_name}:")
            
            # Store each piece of information in variables
            energy = float(food_info['Energy (kcal)'])
            protein = float(food_info['Protein (g)'])
            total_fat = float(food_info['Total Fat (g)'])
            carbohydrate = float(food_info['Carbohydrate (g)'])
            sugar = float(food_info['Sugar (g)'])
            fiber = float(food_info['Fiber (g)'])
            vitamin_c = float(food_info['Vitamin C (%)'])
            vitamin_a = float(food_info['Vitamin A (%)'])
            vitamin_k = float(food_info['Vitamin K (%)'])
            iron = float(food_info['Iron (%)'])
            calcium = float(food_info['Calcium (%)'])
            magnesium = float(food_info['Magnesium (%)'])
            
            # Print or use the variables as needed
            print(f"Energy: {energy} kcal")
            print(f"Protein: {protein} g")
            print(f"Total Fat: {total_fat} g")
            print(f"Carbohydrate: {carbohydrate} g")
            print(f"Sugar: {sugar} g")
            print(f"Fiber: {fiber} g")
            print(f"Vitamin C: {vitamin_c}%")
            print(f"Vitamin A: {vitamin_a}%")
            print(f"Vitamin K: {vitamin_k}%")
            print(f"Iron: {iron}%")
            print(f"Calcium: {calcium}%")
            print(f"Magnesium: {magnesium}%")
        else:
            print(f"No information found for {food_name}.")
        
        # Assuming your model returns probabilities for each class
        # You can format the response as per your requirement
        return render_template('result1.html',predict=predict,energy=energy,protein=protein,total_fat=total_fat,carbohydrate=carbohydrate,sugar=sugar,fiber=fiber,vitamin_c=vitamin_c,vitamin_a=vitamin_a,vitamin_k=vitamin_k,iron=iron,calcium=calcium,magnesium=magnesium, reccomendation=reccomendation,allergy=allergy)

if __name__ == '__main__':
    app.run(debug=True)
