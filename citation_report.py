import os,csv,argparse
from datetime import datetime
import requests
import dataset

parser = argparse.ArgumentParser(description=\
        "Get WOS citation counts for a list of DOIs")
parser.add_argument('csv', help='file with DOIs separated by ,')
args = parser.parse_args()

dois = []

with open(args.csv,newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        dois += row

out = open('output.csv','w',newline='')
writer = csv.writer(out)

#Run query to get scope of records
token = os.environ['WOSTOK']
headers = {
    'X-ApiKey' : token,
    'Content-type': 'application/json'
}

base_url = 'https://api.clarivate.com/api/wos/?databaseId=WOK'

for doi in dois:
    url = base_url + '&count=1&firstRecord=1&usrQuery=DO='+doi
    response = requests.get(url,headers=headers)
    response = response.json()
    if response['QueryResult']['RecordsFound'] == 0:
        print(doi+' not found in Web of Science')
    else:
        citations = response['Data']['Records']['records']['REC']['dynamic_data']['citation_related']['tc_list']['silo_tc']['local_count']
        writer.writerow([doi,citations])

