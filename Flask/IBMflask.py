
from flask import Flask, render_template, request
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "gkjhE4WffcjgPlrh1jgi8A8RZb4XoukgecxptkBl34Sl"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app=Flask(__name__)
@app.route('/')#binds to an url
def helloworld():
    return render_template("index.html")

@app.route('/login', methods =['POST'])#binds to an url
def login():
    p =request.form["ms"]
    q= request.form["as"]
    r= request.form["rd"]
    s= request.form["s"]
    if (s=="cal"):
        s1,s2,s3=1,0,0
    if (s=="flo"):
        s1,s2,s3=0,1,0
    if (s=="ny"):
        s1,s2,s3=0,0,1
    t=[[int(s1),int(s2),int(s3),int(p),int(q),int(r)]]

# NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["f0","f1","f2","f3","f4","f5"], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7240070c-0b7b-4d63-be9e-a1377cc0672b/predictions?version=2023-03-15', json=payload_scoring,
                                     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    #print(response_scoring.json())
    pred =response_scoring.json()
    print(pred)
    output=pred['predictions'][0]['values'][0][0]
    print(output)
    return render_template("index.html",y = "the predicted profit is  " + str(output) )

if __name__ == '__main__' :
    app.run(debug= False)
