import requests
from prefect import flow, task
import json
import csv



@flow
def sample_flow(url):
     
    print("----------------------")
    
    with open("D:\Ardhi\Ecoinvent\cut-off-system-model\Cut-off Cumulative LCIA v3.9.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row in csvreader:
        print(row)
    
    

sample_flow("https://beta3.api.climatiq.io/search?query=resin&results_per_page=100")


