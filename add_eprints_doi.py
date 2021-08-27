import csv

doi_mapping = {}

with open('doi_update.csv') as infile:
    reader = csv.reader(infile)
    for row in reader:
        doi_mapping[row[0]] = row[1]

with open('beckman.tsv') as infile:
    with open('beckman_doi.csv','w') as outfile: 
        reader = csv.DictReader(infile,delimiter='\t')
        writer = csv.writer(outfile)
        for row in reader:
            doi = ''
            eprintid = row['EPrintID']
            if row['DOI'] == '':
                if eprintid in doi_mapping:
                    doi = doi_mapping[eprintid]
                else:
                    print(eprintid)
            else:
                doi = row['DOI']

            if doi != '':
                writer.writerow([doi,eprintid])
