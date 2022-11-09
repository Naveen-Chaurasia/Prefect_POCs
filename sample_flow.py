import requests
from prefect import flow, task
import json
import csv

@task
def call_api(url):
    access_token = '1YTWX5GJMQME16GGFK5G6N5MB96M'
    response = requests.get(url,headers={'Content-Type':'application/json','Authorization': 'Bearer {}'.format(access_token)})    
    print(response.status_code)
    return response.json()

@task
def parse_fact(response):
    fact = response["results"]
    print(fact)
    return fact
    
@task
def add_header_of_csv(results): 
    fields = ['id', 'name', 'category', 'sector','constituent_gases'] 
    filename = "climateiq.csv"
    # writing to csv file 
    with open(filename, 'w') as csvfile:  
     csvwriter = csv.writer(csvfile)  
     csvwriter.writerow(fields) 
    return results
    
    
@task
def split_result(results):
    #datadict = json.load(results)
    #datatict is a list of dict.
    datadict=results
    print("*******************")
    print(type(datadict))
    #ids=[]
    filename = "climateiq.csv"
    for item in datadict:
    
     row=[item['id'],item['name'],item['category'],item['sector'],item['constituent_gases']]
     print(row)
     print("*******************")
     with open(filename, 'a') as csvfile:  
      csvwriter = csv.writer(csvfile)  
      csvwriter.writerow(row) 
     #print("*******************")
     #print(item)
     #print("*******************")
     #ids.append(item['id'])
    return results
    

@flow
def sample_flow(url):
    fact_json = call_api(url)
    fact_text = parse_fact(fact_json)
    results=add_header_of_csv(fact_text)
    fact_id=split_result(results)
    print("----------------------")
    print(fact_id)
    return fact_id

sample_flow("https://beta3.api.climatiq.io/search?query=Building Materials&results_per_page=100")