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
        aux = {}
        try:
            codeObejct = compile("input = " + str(i) + "\n" + code, 'sumstring', 'exec')
            
            loc = {}
            exec(codeObejct, globals(), loc)
            return_workaround = loc['output']
            to_print = loc['to_print']
            aux["prints"] = to_print
            
            aux["valueReturned"] =  return_workaround
        
        except SyntaxError as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            line_number = err.lineno
            aux["valueReturned"] = "%s at line %d of %s: %s" % (error_class, line_number, "source string", detail)
            break
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            aux["valueReturned"] = "%s at line %d of %s: %s" % (error_class, line_number, "source string", detail)
            break

        res.append(aux)

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

    var = execute_code("to_print = []\n" + code.replace("print", "to_print.append"), inputs, solutions)
    
    equal = True
    for i in range(len(var)):
        if var[i]["valueReturned"] != solutions[i]:
            equal = False
    return jsonify({'result': var, 'equal':equal})


if __name__ == '__main__':
    app.run(debug=True, port=8000)