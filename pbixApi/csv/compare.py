import csv
from flask import Flask, jsonify

app = Flask(__name__)

 

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

 

if are_matching:
    print("The data in both CSV files matches.")
else:
    print("The data in the CSV files does not match.")



@app.route('/api', methods=['GET'])
def check_matching():

    if are_matching:
        response = {'status': 'success'}
    else:
        response = {'status': 'failure'}

    return jsonify(response)

if __name__ == '__main__':
    app.run()
