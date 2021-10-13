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
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            print(detail + " in line " + str(line_number))
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
    print(var[:-1] == str(solutions))
    return jsonify({'result': var[:-1], 'equal':var[:-1] == str(solutions)})


if __name__ == '__main__':
    app.run(debug=True, port=8000)




'''
code = "inputs = [0,1,2,3]\nls = inputs\noutput = []\nfor i in ls:\n    output.append(i)\nprint(output)"
codeObejct = compile(code, 'sumstring', 'exec')

exec(codeObejct)


Por cada input:

	---------CODE ---------
	var input = "aaddd"

	print("___ITERATION<"+input+">")

	func X(x){
		var output;
		CODIGO output <-- XXX
		print(PEPITO)
		
		return output
	}

	print("___SOLUTION<"+X(input)+">")
	--------------------   

	try
		compiled_code = compile(CODE)
	execpt
		syntax error
			....

	return_exec = exec(compiled_code)

	if(return_exec == output)
		ok
	else
		NOK
		


calcular si x es un palindromo

___ITERATION<asdasd>
PEPITO
___SOLUTION<true>

___ITERATION<asdasd>
PEPITO
___SOLUTION<false>



{
	result:"correct"
	console:
	"
	--- Test 1(input = "asdasd") ---
		PEPITO
	--------------------------------
	--- Test 2(input = "asdfdd") ---
		PEPITO
	--------------------------------
	--- Test 1(input = "asdasd") ---
		PEPITO
	--------------------------------
	---- Test 2 ---
		PEPITO
	---------------
	...

	" 


}


'''