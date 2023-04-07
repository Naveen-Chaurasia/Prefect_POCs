from flask import Flask, jsonify, request,redirect
import requests

import json
import csv
import os
import jellyfish  
  
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'D:\pythone\JUPYTER NOTEBOOKS\Prefecte'
app.config['ALLOWED_EXTENSIONS'] = set(['csv']) 
  
# on the terminal type: curl http://127.0.0.1:5000/

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})
        
        
#@app.route('/similar_materials', methods = ['GET', 'POST'])
#def similar_materials():
    
#https://towardsdatascience.com/calculate-similarity-the-most-relevant-metrics-in-a-nutshell-9a43564f533e


    
 
@app.route('/add_header', methods = ['GET'])
def addHeader():
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\Cut-off Cumulative LCIA v3.9.csv", 'r') as file:
       filename = "unit_process.csv"
       csvreader = csv.reader(file)
       for row in csvreader:
        header=row
        break
       with open(filename, 'w') as csvfile: 
         csvwriter = csv.writer(csvfile)  
         csvwriter.writerow(header)
         return header

 
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
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\sample_eco_lcia.csv", 'r') as file:
       csvreader = csv.reader(file)
       for row in csvreader:
          print("________________________________________________________")
          print(row)
          if num == row[3]:
           
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
           
######################################################################################   
@app.route('/upload', methods=['POST'])
def upload_read_add_generate_lcia():
    # Get the name of the uploaded file
    file = request.files['file']
     
    # Check if the file is one of the allowed types/extensions
    if file :#and allowed_file(file.filename):
        
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return redirect(url_for('YOUR REDIRECT FUNCTION NAME',filename=filename))    
        return readcsvfile(filename)
    
    
@app.route('/readcsvfile/<string:readfilename>', methods = ['GET'])  
def readcsvfile(readfilename):
    loc='D:\Ardhi\Ecoinvent\cut-off-system-model'+'\\'+readfilename
    with open(loc, 'r') as file:
       csvreader = csv.reader(file)
       for row in csvreader: 
         url='http://127.0.0.1:5000/addlcia/'+row[0]+'/'+readfilename
         response=requests.get(url)
         print (response)
         
    return 'done' 
    
    
    
@app.route('/addlcia/<string:num>/<string:uploadedfilename>', methods = ['GET'])
def addlcia(num,uploadedfilename):
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\sample_eco_lcia.csv", 'r') as file:
       csvreader = csv.reader(file)
       filename = "unit_process__"+uploadedfilename
       with open(filename, 'a') as csvfile:
           csvwriter = csv.writer(csvfile)  
      
           for row in csvreader:
              if num == row[3]: 
               csvwriter.writerow(row) 
               return jsonify({'data': row})  

              elif num in row[3]:
               csvwriter.writerow(row)
               return jsonify({'data': row})                
  
      
#method not working  problem in reding csv file without saving it
# Route that will process the file upload
@app.route('/uploadandreadcsv', methods=['POST'])
def uploadandreadcsv():
    
    file = request.files['file']
    with open(file, 'r') as file1:
    # Check if the file is one of the allowed types/extensions
        if file1 :#and allowed_file(file.filename):
                
                filename = file.filename

                csvreader = csv.reader(file1)
                for row in csvreader: 
                     url='http://127.0.0.1:5000/addlcia/'+row[0]+'/'+filename
                     response=requests.get(url)
                     print (response)
                     
                return 'done'       
            
                
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)