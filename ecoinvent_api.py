from flask import Flask, jsonify, request
import requests
from prefect import flow, task
import json
import csv
  

app = Flask(__name__)
  
# on the terminal type: curl http://127.0.0.1:5000/

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})
    
@app.route('/lcia/<string:num>', methods = ['GET'])
def lcia(num):
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\Cut-off Cumulative LCIA v3.9.csv", 'r') as file:
       csvreader = csv.reader(file)
       for row in csvreader:
          if row[3]== num:
           return jsonify({'data': row})    
           
@app.route('/chemInfo/<string:num>', methods = ['GET'])
def chemicalInfo(num):
    url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+num+'/cids/JSON'
    record_number=requests.get(url,headers={'Content-Type':'application/json'})
    return record_number.json()['IdentifierList']['CID'][0]
  
    
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)