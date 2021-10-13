'''
from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS
import sys
from io import StringIO
import contextlib
import traceback

app = Flask(__name__)
cors = CORS(app, resources={r"/tester": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


#Testing Route
@app.route('/', methods=['GET'])
def getDefault():
    return jsonify({'response': 'Hello to my users api!'})

    
#Testing Route
@app.route('/tester', methods=['POST'])
def tester():
    inputs = request.json['inputs']
    solutions = request.json['solutions']
    code = request.json['code']
    return jsonify({'response': 'Hello to my users api!'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)

'''

import traceback

def execute_code(inputs, solutions, code):
    array = []
    for i in inputs:
        try:
            codeObejct = compile("inp = " + str(i) + "\n" + code + "\nprint(output)", 'sumstring', 'exec')
            array.append(exec(codeObejct))
        except Exception as err:
            array.append(err)
    return array

print(execute_code([0,1,2,3], [0,2,4,6], "output = 2*inp"))