from flask import Flask, jsonify, request
import sys
from io import StringIO
import contextlib
app = Flask(__name__)

def execute_code(code):
    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    with stdoutIO() as s:
        try:
            exec(code)
        except:
            print("Something wrong with the code")
    #print(code)
    return s.getvalue()

#Testing Route
@app.route('/', methods=['GET'])
def getDefault():
    return jsonify({'response': 'Hello to my users api!'})

#Testing Route
@app.route('/tester', methods=['POST'])
def tester():
    inputs = request.json['inputs']
    solutions = request.json['solutions']
    """
    Example

    {
	"inputs": [0,1,2,3],
	"solutions": [0,1,2,3],
	"code": "ls = inputs\n    output = []\n    for i in ls:\n        output.append(i)"
    }

    """
    code = request.json['code']

    code2 = code.splitlines()
    program_parsed = ""
    for i in code2:
        program_parsed += "    " + i + "\n"
    program = "def main(inputs):\n" + program_parsed + "    return outputs\nprint(main(inputs="+ str(inputs) +"))" 
    var = execute_code(program)
    return jsonify({'result': var[:-1], 'equal':var[:-1] == str(solutions)})


if __name__ == '__main__':
    app.run(debug=True, port=8000)