import os, time, json
import urllib.parse
import requests
import csv

base_url = "https://api.crossref.org/works/"
contact = "?mailto=tmorrell@caltech.edu"
references = {}

with open("AIAA_DOIs.txt") as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) != 0:
            doi = row[0]
            if doi != "":
                print(doi)
                url = base_url + doi + contact
                response = requests.get(url)
                response = response.json()["message"]
                if "reference" in response:
                    references[doi] = response["reference"]
                else:
                    print("No references found for " + doi)

with open("AIAA_references_crossref.json", "w") as json_file:
    json.dump(references, json_file)
