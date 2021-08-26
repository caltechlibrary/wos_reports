import os, time, json
import requests
import csv


#Go from a list of WOS references to a list of publishers

def add_count(prefix,dictionary,count=1):
    if prefix in dictionary:
        dictionary[prefix] = dictionary[prefix] + count
    else:
        dictionary[prefix] = count

article_prefixes = {}
reference_prefixes = {}

with open('resnick_references.json') as references:
    refs = json.loads(references.read())
    for ref in refs.keys():
        if ref.startswith('10.'):
            prefix = ref.split('/')[0]
            if 'cell' in ref and prefix == '10.1016':
                prefix = 'cell'
            add_count(prefix,article_prefixes)
        for citation in refs[ref]:
            if 'DOI' in citation:
                prefix = citation['DOI'].split('/')[0]
                if prefix.startswith('DOI'):
                    prefix = prefix.split(' ')[1]
                if 'cell' in ref and prefix == '10.1016':
                    prefix = 'cell'
                add_count(prefix,reference_prefixes)

article_prefixes = sorted(article_prefixes.items(), key=lambda x:x[1], reverse=True)
reference_prefixes = sorted(reference_prefixes.items(), key=lambda x:x[1], reverse=True)

url = 'https://api.crossref.org/prefixes/'
contact = '&mailto=tmorrell@caltech.edu'

article_publishers = {}
reference_publishers = {}

for prefix in article_prefixes:
    if prefix[0] == 'cell':
        add_count('Cell Press',article_publishers, prefix[1])
    else:
        response = requests.get(url+prefix[0]+contact)
        time.sleep(0.1)
        publisher = response.json()['message']['name']
        add_count(publisher,article_publishers, prefix[1])

for prefix in reference_prefixes:
    if prefix[0] == 'cell':
        add_count('Cell Press',reference_publishers, prefix[1])
    else:
        response = requests.get(url+prefix[0]+contact)
        time.sleep(0.1)
        if response.status_code == 200:
            publisher = response.json()['message']['name']
            add_count(publisher, reference_publishers, prefix[1])
        else:
            print(prefix[0])
            print(response.text)

article_publishers = sorted(article_publishers.items(), key=lambda x:x[1], reverse=True)
reference_publishers = sorted(reference_publishers.items(), key=lambda x:x[1], reverse=True)

with open('resnick_article_publishers.csv','w') as outfile:
    writer = csv.writer(outfile)
    for publisher in article_publishers:
        writer.writerow(publisher)

with open('resnick_reference_publishers.csv','w') as outfile:
    writer = csv.writer(outfile)
    for publisher in reference_publishers:
        writer.writerow(publisher)

