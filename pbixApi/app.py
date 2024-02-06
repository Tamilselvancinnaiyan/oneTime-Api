import io
import requests
import json
import csv


from flask import Flask, jsonify, request

app = Flask(__name__)

class ReportExtractor:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.result = []

    def extract(self):
        # code

        import json
from zipfile import ZipFile
import shutil
import pandas as pd

class ReportExtractor():

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.result = []

    def extract(self):
        pathFolder = f'{self.path}/temp_{self.name[:-5]}'
        #try: shutil.rmtree(pathFolder)
        #except:
         #   print(f'folder {pathFolder} not present')
        f = ZipFile(f'{self.path}/{self.name}', 'r')
        f.extractall(pathFolder)
        report_layout = json.loads(
            open(f'{pathFolder}/Report/Layout', 'r', encoding='utf-16 le').read()
        )
        #print(report_layout)
        f.close()
        fields = []
        for s in report_layout['sections']: 
            for vc in s['visualContainers']:       
                try:
                    query_dict = json.loads(vc['config'])
                    for command in query_dict['singleVisual']['prototypeQuery']['Select']:

                        if 'Measure' in command.keys():
                            #- MEASURES
                            name = command['Name'].split('.')[1]
                            table = command['Name'].split('.')[0]
                            fields.append([s['displayName'], query_dict['name'], table, name, 'Measure'])

                        elif 'Column' in command.keys():
                            # COLUMNS
                            name = command['Name'].split('.')[1]
                            table = command['Name'].split('.')[0]
                            fields.append([s['displayName'], query_dict['name'], table, name, 'Column'])

                        elif 'Aggregation' in command.keys():
                            # AGGREGATIONS
                            if ( ( '(' in command['Name'] ) & ( ')' in command['Name'] ) ): 
                                txt_extraction = command['Name'][command['Name'].find('(') + 1: command['Name'].find(')') ]
                            name  = txt_extraction.split('.')[1]
                            table = txt_extraction.split('.')[0]
                            fields.append([s['displayName'], query_dict['name'], table, name, 'Aggregation'])

                except: 
                    pass
        self.result =  fields
        

re = ReportExtractor(r"/Users/tamil/Desktop/Project/pbix/", "nesamani.pbix")
re.extract()

df = pd.DataFrame(re.result, columns=['Page', 'Visual ID', 'Table', 'Name', 'Type'])
# Aggregate the data
aggregated_data = df.groupby(['Page', 'Visual ID', 'Table']).apply(lambda x: x[['Name', 'Type']].to_dict(orient='records')).reset_index().rename(columns={0: 'AggregatedData'})

# Convert the aggregated data to JSON
json_data = aggregated_data.to_json(orient='index', indent=4)

def compare_csv(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

 

        for row1, row2 in zip(reader1, reader2):
            if row1 != row2:
                return False

 

        # Check if both files have the same number of rows
        if sum(1 for _ in reader1) != sum(1 for _ in reader2):
            return False

 

    return True

 

# Usage example
file1_path = '/Users/tamil/Desktop/Project/pbixApi/csv/annual-enterprise-survey-2021-financial-year-provisional-csv.csv'
#file2_path = 'annual-enterprise-survey-2021-financial-year-provisional-csv.csv'
file2_path = '/Users/tamil/Desktop/Project/pbixApi/csv/model.csv'

are_matching = compare_csv(file1_path, file2_path)




@app.route('/report', methods=['GET','POST'])

def check_matching():

    if are_matching:
        response = {'status': 'success'}
    else:
        response = {'status': 'failure'}
        
        d = {'data': json_data, 'matching': response}
    return jsonify(d)



if __name__ == '__main__':
    app.run()