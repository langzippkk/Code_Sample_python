This is a project that tokenize and parse the jack programming language according to its syntax and generate xml file:

	sample input: main.jack
	sample output:main.xml

Compile and run:

	Dependencies: Python3.5 or higher, Python Module(just sys and os)

	output: a .xml file in the same directory as the input .jack file
	
	test case: this code successfully passed all the tests given


How to run:
	
	1. the compiler only translate single .jack file and the VM translator will handle multiple files problem.
	Run this code by: python location/of/compiler.py location/of/input.jack
	In my case, for example, it would be: $ python compiler.py ./Square/Square.jack


	2. The output will be named input.xml and in the same directory with input file(might overwrite previous input.xml file if you have one
	with the same directory of input.jack !!)
	

compiler.py

	This python code has two parts:
	1. Simple tokenizer that tokenize each char and convert it to a tuple: ('type',char)

	2. A parser class that parse these token according to the logic of jack languages.


	The parser uses a counter to represent the current tuple(from part1) that need to be parsed.
	Subrountine,varDec,statements(including if,while,do,return,let),expression,term are handled 
	with their corresponding syntax, which is also written below each function definition as comment in detail.



