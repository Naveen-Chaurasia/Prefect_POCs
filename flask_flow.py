import requests
from prefect import flow, task
import json
import csv

from flask import Flask, jsonify, request


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
           t = jsonify(row) + jsonify(call_api(num))
           return jsonify({'data': t})    



def call_api(num):
    url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/' + num + '/JSON/?heading=Component+Compounds'
    response = requests.get(url,headers={'Content-Type':'application/json'})    
    print(response.status_code)
    return response.json()

    

# driver function
if __name__ == '__main__':
  
    app.run(debug = True)


#prefect orion start
#http://127.0.0.1:4200
#https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest-tutorial#_Toc458584416
#https://www.slideshare.net/SunghwanKim95/how-can-you-access-pubchem-programmatically-96003851
#https://chemspipy.readthedocs.io/en/latest/
#https://www.slideshare.net/SunghwanKim95/how-can-you-access-pubchem-programmatically-96003851
#FOR FINDING COMPONENT TCOMPOUNDS
#https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/169944/JSON/?heading=Component+Compounds
#https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/epoxy resin/JSON/?heading=Component+Compounds
#https://v38.ecoquery.ecoinvent.org/Details/LCIA/98ba622f-7696-478e-816f-a9a5640cfd91/290c1f85-4cc4-4fa1-b0c8-2cb7f4276dce