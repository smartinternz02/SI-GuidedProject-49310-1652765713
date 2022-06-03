# Flask is a application
# used to run/serve our application
# request is used to access the file which is uploaded by the user in out application
# render_template is used for rendering the html pages
# pickle is used for serializing and de-serializing Python object structures
from flask import Flask, render_template, request 


app=Flask(__name__) # our flask app


import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "9EB9X8DRiIQWG5llaLV2my5fgqfgTXX_aTQUQxry1jgy"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/') # rendering the html template
def home():
    return render_template('home.html')
@app.route('/predict') # rendering the html template
def index() :
    return render_template("index.html")

@app.route('/data_predict', methods=['POST']) # route for our prediction
def predict():
    age = request.form['age'] # requesting for age data
    gender = request.form['gender'] # requesting for gender data
    tb = request.form['tb'] # requesting for Total_Bilirubin data
    db = request.form['db'] # requesting for Direct_Bilirubin data
    ap = request.form['ap'] # requesting for Alkaline_Phosphotase data
    aa1 = request.form['aa1'] # requesting for Alamine_Aminotransferase data
    aa2 = request.form['aa2'] # requesting for Aspartate_Aminotransferase data
    tp = request.form['tp'] # requesting for Total_Protiens data
    a = request.form['a'] # requesting for Albumin data
    agr = request.form['agr'] # requesting for Albumin_and_Globulin_Ratio data
    
    # coverting data into float format
    data = [[float(age), float(gender), float(tb), float(db), float(ap), float(aa1), float(aa2), float(tp), float(a), float(agr)]]
    
    
    
    # prediction= model.predict(data)[0]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [["age","gender","tb","db","ap","aa1","aa2","tp","a","agr"]], "values": data}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/adae71da-dc5b-4639-84cd-720aeba54f28/predictions?version=2022-06-03', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Response")
    # print(response_scoring.json())
    pred = response_scoring.json()['predictions'][0]['values'][0][0]
    print(pred)

    if (pred == 1):
        return render_template('chance.html', prediction='You have a liver disease problem, You must and should consult a doctor. Take care')
    else:
        return render_template('noChance.html', prediction='You dont have a liver disease problem')

if __name__ == '__main__':
    app.run()