import os, time, json
import urllib.parse
import requests
import csv

# Set up WOS access
token = os.environ["WOSTOK"]
headers = {"X-ApiKey": token, "Content-type": "application/json"}

base_url = "https://api.clarivate.com/api/wos/?databaseId=WOK"
references_url = "https://api.clarivate.com/api/wos/references/?databaseId=WOK"
references = {}

with open("AIAA_DOIs.txt") as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) != 0:
            doi = row[0]
            if doi != "":
                print(doi)
                url = base_url + "&count=1&firstRecord=1&usrQuery=DO=" + doi
                response = requests.get(url, headers=headers)
                response = response.json()
                time.sleep(0.5)
                if "QueryResult" in response:
                    if response["QueryResult"]["RecordsFound"] == 0:
                        print(doi + " not found in Web of Science")
                    else:
                        uid = response["Data"]["Records"]["records"]["REC"][0]["UID"]
                        euid = urllib.parse.quote(uid)
                        url = (
                            references_url + "&count=100&firstRecord=1&uniqueId=" + euid
                        )
                        response = requests.get(url, headers=headers)
                        response = response.json()
                        time.sleep(0.5)
                        lenv = len(response["Data"])
                        references[doi] = response["Data"]
                        recnum = 100
                        while lenv == 100:
                            url = (
                                references_url
                                + "&count=100&firstRecord="
                                + str(recnum)
                                + "&uniqueId="
                                + euid
                            )
                            response = requests.get(url, headers=headers)
                            response = response.json()
                            time.sleep(0.5)
                            lenv = len(response["Data"])
                            references[doi] = references[doi] + response["Data"]
                            recnum = recnum + 100
                        print(len(references[doi]))

                else:
                    print(response)

with open("AIAA-DOIs_references.json", "w") as json_file:
    json.dump(references, json_file)
