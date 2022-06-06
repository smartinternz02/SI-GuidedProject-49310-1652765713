import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "9EB9X8DRiIQWG5llaLV2my5fgqfgTXX_aTQUQxry1jgy"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [["age","gender","tb","db","ap","aa1","aa2","tp","a","agr"]], "values": [[62,0,10.9,5.5,699,64,100,7.5,3.2,0.74]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/adae71da-dc5b-4639-84cd-720aeba54f28/predictions?version=2022-06-03', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Response")
# print(response_scoring.json())
pred = response_scoring.json()['predictions'][0]['values'][0][0]
print(pred)