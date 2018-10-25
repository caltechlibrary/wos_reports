# wos_reports

Generate reports from Web of Science

## citation_report

Take a csv file with DOIs, return a csv file with DOIs and citation counts

Requires: 

Python 3 (Recommended via [Anaconda](https://www.anaconda.com/download)) with reqests library.

#### Usage
Type `python citation_report.csv doi.csv`; you'll get an output.csv file.  You
need to get a WOS developer token from developer.clarivate.com and save it to
an environment variable by typing `export WOSTOK=***token goes here***`
