from os import error
from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS
import sys
from io import StringIO
import contextlib
import traceback

class InterpreterError(Exception): pass

app = Flask(__name__)
cors = CORS(app, resources={r"/tester": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def execute_code(code, inputs, solutions):
    res = []
    for i in inputs:
        try:
            codeObejct = compile("input = " + str(i) + "\n" + code, 'sumstring', 'exec')
            
            loc = {}
            exec(codeObejct, globals(), loc)
            return_workaround = loc['output']

            print(loc)
            
            res.append(return_workaround)
        
        except SyntaxError as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            line_number = err.lineno
            res.append("%s at line %d of %s: %s" % (error_class, line_number, "source string", detail))
            break
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            res.append("%s at line %d of %s: %s" % (error_class, line_number, "source string", detail))
            break

    return res

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

    """
    Example

    {
	"inputs": [0,1,2,3],
	"solutions": [0,2,4,6],
	"code": "output = input*2"
    }
    """

    var = execute_code(code, inputs, solutions)
    
    print(var == str(solutions))
    return jsonify({'result': var, 'equal':var == solutions})


if __name__ == '__main__':
    app.run(debug=True, port=8000)