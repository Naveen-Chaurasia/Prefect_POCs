from flask import Flask, jsonify, request,redirect
import requests

import json
import csv
import os
import jellyfish  
  
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'D:\pythone\JUPYTER NOTEBOOKS\Prefecte'
app.config['ALLOWED_EXTENSIONS'] = set(['csv']) 
      

 
@app.route('/chemInfo/<string:num>', methods = ['GET'])
def chemicalInfo(num):
    cidurl='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+num+'/cids/JSON'
    record_number=requests.get(cidurl,headers={'Content-Type':'application/json'})
    cid = str(record_number.json()['IdentifierList']['CID'][0])
    chemInfourl='https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/'+cid+'/JSON/'
    chemInfo=requests.get(chemInfourl,headers={'Content-Type':'application/json'})
    print("********************************************************")
    print(type(chemInfo.content.json()))
    return chemInfo.json()['Record']['Section']
    
    
@app.route('/lcia/<string:num>', methods = ['GET'])
def lcia(num):
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\Cut-off Cumulative LCIA v3.9.csv", 'r') as file:
       csvreader = csv.reader(file)
       print(csvreader)
       for row in csvreader:
        #   print("______________________________________________________++++++++++++++++")
        #   print(row)
        #   print("_________________________________________________________________________")
          print(type(row))
        # if num == row[3]:
           
          return jsonify({'data': row})  

          elif num in row[3]:
           return jsonify({'data': row})  
           
#############################################################################      
@app.route('/similarity_lcia/<string:num>', methods = ['GET'])
def similarity_lcia(num):
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\Cut-off Cumulative LCIA v3.9.csv", 'r') as file:
       csvreader = csv.reader(file)
       maxdis=0
       max_sim_row=[]
       for row in csvreader:
           dis=jellyfish.jaro_distance(num, str(row[3]))
           if(dis>maxdis):
            maxdis=dis
            max_sim_row=row
       return jsonify({'data': max_sim_row,'score':maxdis})  



@app.route('/similarity_lcia1/<string:num>', methods = ['GET'])
def similarity_lcia1(num):
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\Cut-off Cumulative LCIA v3.9.csv", 'r') as file:
       csvreader = csv.reader(file)
       list_of_similar_materials=[]
       list_of_similar_materials1={}
       for row in csvreader:
          if num in row[3]:
           dis=jellyfish.jaro_distance(num, str(row[3]))
            #row=row.append(dis)
           row_with_score=jsonify({'data':row,'similarity_score':dis})
           
           list_of_similar_materials1['data']=row
           list_of_similar_materials1['similarity_score']=dis
           list_of_similar_materials.append(list_of_similar_materials1)
       return list_of_similar_materials      
           
    
                
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)