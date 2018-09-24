import os,shutil,json,subprocess
from datetime import datetime
import requests
import dataset

def save_records(collection,records):
    for r in records:
        err = dataset.create(collection,r['UID'],r)
        if err != '':
                print("Error in saving record: "+err)

def get_wos_refs(new=True):
    #New=True will download everything from scratch and delete any existing records

    collection = 'wos_refs.ds'

    if new==True:
        if os.path.exists(collection)==True:
            shutil.rmtree(collection)

    if os.path.isdir(collection) == False:
        ok = dataset.init(collection)
        if ok == False:
            print("Dataset failed to init collection")
            exit()

    #Run query to get scope of records
    token = os.environ['WOSTOK']
    headers = {
        'X-ApiKey' : token,
        'Content-type': 'application/json'
    }

    base_url = 'https://api.clarivate.com/api/wos/?databaseId=WOK'

    collected = dataset.has_key(collection,"captured")

    if collected == True:
        date = dataset.read(collection,"captured")
        date = date[0]['captured']
        date = datetime.fromisoformat(date)
        current = datetime.today()
        diff = (current-date)
        base_url = base_url + '&loadTimeSpan=' +str(diff.days)+'D'

    url = base_url + '&count=1&firstRecord=1&usrQuery=OG=California%20Institute%20of%20Technology'

    incomplete = dataset.has_key(collection,"incomplete")

    if incomplete == True:
        query = dataset.read(collection,"incomplete")
        query_id = query[0]['incomplete']
        query = dataset.read(collection,"record_start")
        record_start = query[0]['record_start']
        query = dataset.read(collection,"record_count")
        record_count = query[0]['record_count']


    else:
        response = requests.get(url,headers=headers)
        response = response.json()
        record_count = response['QueryResult']['RecordsFound']
        print(record_count)
        query_id = response['QueryResult']['QueryID']
 
        dataset.create(collection,'incomplete',{"incomplete":query_id})
 
        record_start = 1

        dataset.create(collection,'record_start',{"record_start":record_start})
        dataset.create(collection,'record_count',{"record_count":record_start})

    query_url = 'https://api.clarivate.com/api/wos/query/'

    while record_count > 0:
        print(record_start)
        if record_count > 100:
            url = query_url + str(query_id) + '?count=100&firstRecord=' +\
                str(record_start)
            response = requests.get(url,headers=headers)
            response = response.json()
            print(response)
            save_records(collection,response['Records']['records']['REC'])
            record_start = record_start + 100
            record_count = record_count - 100
            dataset.update(collection,'record_start',{"record_start":record_start})
            dataset.update(collection,'record_count',{"record_count":record_count})
        else:
            url = query_url + str(query_id) + '?count=' +\
            str(record_count) + '&firstRecord='+ str(record_start)
            response = requests.get(url,headers=headers)
            response = response.json()
            save_records(collection,response['Records']['records']['REC'])
            record_count = 0

    date = datetime.today().isoformat()
    record = {"captured":date}
    if dataset.has_key(collection,"captured"):
        err = dataset.update(collection,'captured',record)
        if err !="":
            print(f"Unexpected error on update: {err}")
    else:
        err = dataset.create(collection,'captured',record)
        if err !="":
            print(f"Unexpected error on create: {err}")

    dataset.delete(collection,'incomplete')

if __name__ == "__main__":
    if os.path.isdir('data') == False:
        os.mkdir('data')
    os.chdir('data')
    get_wos_refs(False)

