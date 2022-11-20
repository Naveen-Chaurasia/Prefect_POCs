from flask import Flask, jsonify, request,redirect
import requests
from prefect import flow, task
import json
import csv
import os
  
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'D:\pythone\JUPYTER NOTEBOOKS\Prefecte'
app.config['ALLOWED_EXTENSIONS'] = set(['csv']) 
  
# on the terminal type: curl http://127.0.0.1:5000/

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})
        
        
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
    return chemInfo.json()['Record']['Section']
    
    
           
    
    
@app.route('/lcia/<string:num>', methods = ['GET'])
def lcia(num):
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\Cut-off Cumulative LCIA v3.9.csv", 'r') as file:
       csvreader = csv.reader(file)
       for row in csvreader:
          if num == row[3]:
           
           return jsonify({'data': row})  

          elif num in row[3]:
           return jsonify({'data': row}) 


@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']

    # Check if the file is one of the allowed types/extensions
    if file :#and allowed_file(file.filename):
        
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return redirect(url_for('YOUR REDIRECT FUNCTION NAME',filename=filename))    
        return 'done'
               


@app.route('/addlcia/<string:num>/<string:uploadedfilename>', methods = ['GET'])
def addlcia(num,uploadedfilename):
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\Cut-off Cumulative LCIA v3.9.csv", 'r') as file:
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