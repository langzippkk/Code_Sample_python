import sys
import os

keyword = {'class','constructor','do','if','else','while','return','function','method','field',
'null','this','let','static','var','int','char','boolean','void','true','false'}

symbol = {'[',']','{','}','(',')','.',',',';','+','-','*','/','|','=','~'}

compare = {
		'<': '&lt;',
		'>': '&gt;',
		'\"': '&quot;',
		'&': '&amp;'
	}

class Parser:
	## parser class that parse the tokenized jack language

	def __init__(self,token):
		'''
		input: 
		    token: list of tuples in the format (word, word_type)
		class variables:
		 	  res: take in the parsed result
		    counter: record the current line that we are dealing
		    length: length of total token
		'''
		self.token = token
		self.res = ''
		self.counter = [-1]
		self.length = len(token)


	def result(self):
		## return the result of parser
		self.parser(self.token,self.res,self.counter,self.length)
		return self.res

	def write_tag(self,s):
		## helper function that output string in xml format
		return '<{}>\n'.format(s)

	def write_tag_close(self,s):
		## helper function that output string in xml format
		return '</{}>\n'.format(s)

	def has_next(self):
		## helper function that determine whether we reach the end
		if self.counter[0] < self.length-1:
			self.counter[0]+=1
			return True
		else:
			return False 

	def move_on(self):
		## helper function that write the next tuple into xml format.
		if self.has_next():
			return '<{}> {} </{}>\n'.format(self.token[self.counter[0]][0],\
				self.token[self.counter[0]][1],self.token[self.counter[0]][0])

	def move_2line(self):
		## helper function that write the next two tuples into xml format
		self.res += self.move_on()
		self.res += self.move_on()
		return

	def move_3line(self):
		## helper function that write the next three tuples into xml format
		self.res += self.move_on()
		self.res += self.move_on()
		self.res += self.move_on()
		return

	def parser(self,token,res,counter,length):
		'''
		main parser function
		overall format:
		class + classname + { + vardec + subroutine + } + class
		'''
		self.res += self.write_tag('class')
		self.move_3line()

		self.varDec()
		self.subroutine()

		self.res += self.move_on()
		self.res += self.write_tag_close('class')

	def subroutine(self):
		'''
	  	subrountine function that dealing with constructor/function/method
	  	overall format:
	  	(constructor/function/method) +
	  	(void/type)+ subroutineName +( + parameters +)+subroutineBody
	  	'''
		temp = token[self.counter[0]+1][1]
		if temp in  ('constructor','function','method'):
			self.res += self.write_tag('subroutineDec')
			self.move_2line()
			self.move_2line()
			#parameters
			self.parameters()	
			self.res += self.move_on()  ## )
			#subroutineBody
			self.res += self.write_tag('subroutineBody')
			self.res += self.move_on()  ## {
			# {' varDec* statements '}'
			if self.token[self.counter[0]+1][1] == 'var':			
				self.subVarDec()
			self.statements()
			self.res += self.move_on() 
			self.res += self.write_tag_close('subroutineBody')		
			self.res += self.write_tag_close('subroutineDec')
			self.subroutine()
		else:
			return


	def subVarDec(self):
		'''
		function that dealing with variables
		overall format:
		var+type+varName+(,+varName)+';'
		'''
		if self.token[self.counter[0]+1][1] == 'var':
			self.res += self.write_tag('varDec')
			self.move_3line()

			while self.token[self.counter[0]+1][1] == ',':
				self.move_2line()
			self.res += self.move_on()
			self.res += self.write_tag_close('varDec')
			self.subVarDec()
		else:
			return

	def statements(self):
		'''
		function that handles let,if,do,while,return statements
		overall format:
			1.If: if+(+expression+)+{+statements+}
			2.else: else+{+statements+}
			3.while: while+(+expression+)+{+statements+}
			4.do: do+ subroutineName +(+expressions)+.+subroutineName+(+expressions+)
			5.return: return+expression+;
			6.let: let+varName+ ([+expression+]) + = + expression+ ;
		'''
		self.res += self.write_tag('statements')
		while (self.token[self.counter[0]+1][1]) in ('let','if','do','while','return'):
			if 'if' in (self.token[self.counter[0]+1][1]):
				self.If()
			elif 'while' in (self.token[self.counter[0]+1][1]):
				self.While()
			elif 'do' in (self.token[self.counter[0]+1][1]):
				self.Do()
			elif 'return' in (self.token[self.counter[0]+1][1]):
				self.Return()
			elif 'let' in (self.token[self.counter[0]+1][1]):
				self.Let()
		self.res += self.write_tag_close('statements')

	def If(self):
		self.res+=self.write_tag('ifStatement')
		self.move_2line()
		self.Expressions()
		self.move_2line()
		self.statements()
		self.res+=self.move_on()
		if self.token[self.counter[0]+1][1] == 'else':
			self.Else()
		self.res+=self.write_tag_close('ifStatement')

	def Else(self):
		self.move_2line()
		self.statements()
		self.res += self.move_on()

	def While(self):
		self.res+=self.write_tag('whileStatement')
		self.move_2line()
		self.Expressions()
		self.move_2line()
		self.statements()
		self.res+=self.move_on()
		self.res+=self.write_tag_close('whileStatement')

	def Do(self):
		self.res += self.write_tag('doStatement')
		self.move_2line()
		if '.' in self.token[self.counter[0]+1][1]:
			self.move_2line()
		self.res+=self.move_on()
		self.Expression()
		self.move_2line()
		self.res += self.write_tag_close('doStatement')

	def Return(self):
		self.res+=self.write_tag('returnStatement')
		self.res+=self.move_on()
		if self.token[self.counter[0]+1][1] == ';':
			self.res+=self.move_on()
		else:
			self.Expressions()
			self.res += self.move_on()
		self.res+=self.write_tag_close('returnStatement')


	def Let(self):
		self.res += self.write_tag('letStatement')
		self.move_2line()
		if '[' in self.token[self.counter[0]+1][1]:
			self.res += self.move_on()
			self.Expressions()
			self.res += self.move_on()
		self.res += self.move_on()
		self.Expressions()
		self.res += self.move_on()
		self.res += self.write_tag_close('letStatement')



	def Expression(self):
		'''
		function that handles Multiple expressions
		overrall format:
		ExpressionList + expression + (expressionList)
	 	'''
		self.res+=self.write_tag('expressionList')
		if ')' in  self.token[self.counter[0]+1][1]:
			self.res+=self.write_tag_close('expressionList')
			return
		else:
			self.Expressions()
			while ',' in self.token[self.counter[0]+1][1]:
				self.res += self.move_on()
				self.Expressions()
			self.res+=self.write_tag_close('expressionList')

	def Expressions(self):
		'''
		function that handles single expression
		overrall format:
  		expression+(+(+expression)
  		'''
		self.res += self.write_tag('expression')
		self.expressionsHelper()
		while self.token[self.counter[0]+1][1] in ('+', '-', '*', '/','&amp;','&lt;','&gt;','=','|'):
			self.res += self.move_on()
			self.expressionsHelper()
		self.res += self.write_tag_close('expression')

	def expressionsHelper(self):
		'''
		helper function that handles different terms in an expression
		overrall format:
			1.'(' : （+expression+）
			2.'.': 	identifier+ . + subroutine + ( + expressionList + )
			3.'-' and '~': - or ~ another term
			4.'[':	identifier+[expressions]  
			5.'double (': 	identifier + （+expression+）
		'''
		self.res += self.write_tag('term')
		if '(' in self.token[self.counter[0]+1][1]:
			self.res+= self.move_on()  	
			self.Expressions()
			self.res += self.move_on()

		elif '.' in self.token[self.counter[0]+2][1]:
			self.move_2line()
			self.move_2line()
			self.Expression()
			self.res += self.move_on()


		elif '-' in self.token[self.counter[0]+1][1] or '~' in self.token[self.counter[0]+1][1]:
			self.res+= self.move_on()  ## - or ~
			self.expressionsHelper()

		elif '[' in self.token[self.counter[0]+2][1]:
			self.move_2line()
			self.Expressions() 
			self.res+=self.move_on()

		elif '(' in self.token[self.counter[0]+2][1]:
			self.move_2line()
			self.Expression()
			self.res += self.move_on()

		elif self.token[self.counter[0]+1][1] not in ['.','(','-','[','~']:
			self.res += self.move_on()	

		self.res += self.write_tag_close('term')


	def parameters(self):
		'''
		function that handles multiple parameters
		overrall format:
		type+varName +(, + type+ varName)
		'''
		self.res += self.write_tag('parameterList')
		if self.token[self.counter[0]+1][1] != ')':
			self.move_2line()
			while token[self.counter[0]+1][1] == ',':
				self.move_3line()
			self.res += self.write_tag_close('parameterList')
			return
		else:
			self.res += self.write_tag_close('parameterList')
			return


	def varDec(self):
		'''
		function that handles static or field variable
		overall format:
		(static/field + type + varName +(,+varName)+;
		'''
		temp = self.token[self.counter[0]+1][1]
		if temp in ('static','field'):
			self.res+=self.write_tag('classVarDec')
			self.move_3line()
			while token[self.counter[0]+1][1] == ',':
				self.move_2line() 
			self.res += self.move_on()  
			self.res += self.write_tag_close('classVarDec')        
			self.varDec()
		else:
			return


def remove_comment(file):
	'''
	input:single line with comments
	output:single line without comments
	'''
	with open(file,'r') as document:
		res = ""
		skip = False
		for line in document:
			#line = line.replace(' ','')
			line = line.replace('\t','')
			## if find // comment, delete comment
			if line.find('//') >=0:
				line = line[:line.find('//')]
				line+= '\n'
			if line.find('/*') >=0:
				if line.find('*/')>0:
					## start end in the same line
					line = line[0:line.find('/*')] + line[line.find('*/')+2:]
				else:
					## only start
					line = line[:line.find('/*')]
					## if there are still code, we should add a new line
					res += line
					if len(line)>0:
						res+='\n'
					skip = True
			## only end
			if line.find('/*') <0 and line.find('*/')>0:
				line = line[line.find('*/')+2:]
				skip = False
			if not line.strip():
				continue
			if skip:
				continue
			res+=line
	return res


def line_tokenizer(line):
	'''
	input: line without comments
	output: tokenized jack language

	if find special symbol, append the words previous to the symbol and 
	the symbol seperately
	otherwise, split them by space
	if find "print words", deal with this line individually
	'''
	line = line.lstrip()
	res = []
	temp_pointer = 0
	skip = False
	for index,char in enumerate(line):
		if char in symbol and not skip:
			res.append(line[temp_pointer:index])
			res.append(char)
			temp_pointer = index+1
		if char == ' ' and not skip:
			res.append(line[temp_pointer:index])
			temp_pointer = index+1
		if char =='"' and skip:
			skip = False
			res.append(line[temp_pointer+1:index+1])
			#print(line[temp_pointer:index])
			temp_pointer = index+1
			continue
		if char == '"' and not skip:
			skip = True

	return res


def word_tokenizer(word):
	'''
	input:single tokenized word
	output: tuple with word and its type

	add their tag to different type of word

	'''
	if word in keyword:
		return ('keyword',word)
	elif word in symbol:
		return ('symbol',word)
	elif '"' in word:
		return (('stringConstant',word.replace('"','')))
	elif word.isdigit():
		return (('integerConstant',word))
	elif word in compare:
		return (('symbol',compare[word]))
	else:
		return (('identifier',word))


def tokenizer(input):
	'''
	input: code without comments
	output: list of tuples
	driver function that use word and sentence tokenizer in this function
	'''
	directory = os.path.dirname(input)
	res = ""
	temp_res = []
	res +='<tokens>'
	res += '\n'
	parsed = (remove_comment(input))
	for line in parsed.split('\n'):
		translate = line_tokenizer(line)
		for word in translate:
			if word =='':
				continue
			words = word_tokenizer(word)
			temp_res.append(words)
			xml = '<' +words[0]+ '> ' +\
			words[1] + ' </' + words[0] + '>\n'
			res +=xml
	## keep it want to look at tokenizer result
	# res+= '</tokens>'
	# file = input.replace('.jack','.xmlt')
	# output =open(os.path.join(file),'w')
	# output.write(res)
	return temp_res


if __name__ == "__main__":
	## parse input file
	file = sys.argv[-1]
	token = tokenizer(file)
	parser = Parser(token)
	result = parser.result()
	directory = os.path.dirname(file)
	file = file.replace('.jack','.xml')
	output =open(os.path.join(file),'w')
	output.write(result)