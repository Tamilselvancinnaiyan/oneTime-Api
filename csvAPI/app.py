import csv
import requests

from flask import Flask, jsonify
app = Flask(__name__)


def compare_csv(file1_url, file2_url):
    response1 = requests.get(file1_url)
    response2 = requests.get(file2_url)

 

    lines1 = response1.text.strip().split('\n')
    lines2 = response2.text.strip().split('\n')

 

    if len(lines1) != len(lines2):
        return False

 

    for line1, line2 in zip(lines1, lines2):
        row1 = line1.strip().split(',')
        row2 = line2.strip().split(',')

 

        if row1 != row2:
            return False

 

    return True

 

# Usage example

file1_url = 'https://dev-bulkdownloads.s3.amazonaws.com/student/course/filesannual-enterprise-survey-2021-financial-year-provisional-csv.csv'
file2_url = 'https://dev-bulkdownloads.s3.amazonaws.com/student/course/filesannual-enterprise-survey-2021-financial-year-provisional-csv+(1).csv'


are_matching = compare_csv(file1_url, file2_url)


@app.route('/execute-script', methods=['GET'])
def get_are_matching():
    try:
         
        response = {'status': 'success', 'message': 'Script executed successfully'}
        return jsonify(response)
    except Exception as e:
        # Handle the exception and return an error response
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run()
