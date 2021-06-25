import os, time, json
import urllib.parse
import requests
import csv


#Set up WOS access
token = os.environ['WOSTOK']
headers = {
    'X-ApiKey' : token,
    'Content-type': 'application/json'
}

references_url = 'https://api.clarivate.com/api/wos/references/?databaseId=WOK'
references = {}

with open('wos_ids.csv') as wos_ids:
    ids = csv.reader(wos_ids)
    for idv in ids:
        idv = idv[0]
        euid = urllib.parse.quote(idv)
        url = references_url + '&count=100&firstRecord=1&uniqueId='+euid
        response = requests.get(url,headers=headers)
        response = response.json()
        time.sleep(0.5)
        lenv = len(response['Data'])
        references[idv] = response['Data']
        recnum = 100
        while lenv == 100:
            url = references_url+'&count=100&firstRecord='+str(recnum)+'&uniqueId='+euid
            response = requests.get(url,headers=headers)
            response = response.json()
            time.sleep(0.5)
            lenv = len(response['Data'])
            references[idv] = references[idv] + response['Data']
            recnum = recnum + 100
        print(len(references[idv]))

with open('add_chen_references.json','w') as json_file:
    json.dump(references, json_file)


