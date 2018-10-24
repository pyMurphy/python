# SQL to Relational Algebra
# Disgusting code, please don't judge me based on this. Wrote it in an hour and plan to expand on it when I have time.

syntax = {
	'select': {
		'symbol':'π'
		#'func'	:projection
	},
	'from'	: {
		'symbol':':='
		#'func'	:table
	},
	'where'	: {
		'symbol':'σ'
		#'func'	:condition
	},
	'and'	: {
		'symbol':'U'
		#'func'	:union
	},
	'or'	: {
		'symbol':'n'
		#'func'	:intersection
	}
}

def projection(string):
	if 'select' in string.lower():
		ns = string[string.lower().find('select')+len('select'):].strip()
		if 'from' in ns.lower():
			ns = ns[:ns.lower().find('from')].strip()
		ns = ns.split(',')
		for i,v in enumerate(ns):
			ns[i] = ns[i].strip()
		return ns

def table(string):
	if 'from' in string.lower():
		ns = string[string.lower().find('from')+len('from'):].strip()
		if 'where' in ns.lower():
			ns = ns[:ns.lower().find('where')].strip()
		return ns

def condition(string):
	if 'where' in string.lower():
		ns = string[string.lower().find('where')+len('where'):].strip()
		return ns

def join_replace(string, operator):
	if operator.lower() in string.lower():
		string = string.replace(operator.upper(), syntax[operator.lower()]['symbol'])
	return string

def convert_syntax(msg):
	project = projection(msg)
	tab 	= table(msg)
	cond 	= condition(msg)
	cond 	= join_replace(cond,'and')
	cond 	= join_replace(cond,'or')
	print('ResultTable',syntax['from']['symbol'],syntax['select']['symbol']+'('+', '.join(project)+')(',syntax['where']['symbol']+cond+'({table})'.format(table=tab),')')

while True:
	convert_syntax(input('>'))
