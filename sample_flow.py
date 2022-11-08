import requests
from prefect import flow, task

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

@flow
def sample_flow(url):
    fact_json = call_api(url)
    fact_text = parse_fact(fact_json)
    return fact_text

sample_flow("https://beta3.api.climatiq.io/search?query=Building Materials&results_per_page=100")