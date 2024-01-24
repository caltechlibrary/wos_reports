import os, time, json
import urllib.parse
import requests
import csv

base_url = "https://api.crossref.org/works/"
contact = "?mailto=tmorrell@caltech.edu"
references = {}
count = {}

with open("SSPPdois.txt") as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) != 0:
            doi = row[0]
            ref_count = 0
            if doi != "":
                print(doi)
                url = base_url + doi + contact
                response = requests.get(url)
                if response.status_code == 200:
                    response = response.json()["message"]
                    if "reference" in response:
                        references[doi] = response["reference"]
                        for ref in response["reference"]:
                            if 'DOI' in ref:
                                ref_doi = ref['DOI']
                                if ref_doi.startswith('10.2514'):
                                    ref_count += 1
                        count[doi] = ref_count
                    else:
                        print("No references found for " + doi)
                else:
                    print("Error: " + str(response.status_code))

with open("SSPP_references_crossref.json", "w") as json_file:
    json.dump(references, json_file)

with open("SSPP_references_crossref_count.csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    for key, value in count.items():
        writer.writerow([key, value])
