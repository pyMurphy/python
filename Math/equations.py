# Python Equation Package
#
# USER 		-	pyMurphy
# DATE		- 	01/10/2017
# VERSION	-	V0.2.1
#
# This is a package for solving simple linear equations.
# It is mainly a project for me to improve my programming skills
# so it may not be the most efficient.
#
# Feel free to use this code to learn from, I have commented what
# I'm doing on each line so that it's easy to understand. Sorry if
# some of the variable names aren't clear, but hopefully the
# internal commentary makes up for it.

import string

coefficient_list = [0,1,2,3,4,5,6,7,8,9]	# List of digits 0-9
var_list = list(string.ascii_lowercase)		# List of all lowercase characters
space_list = [' ','+','-','/','*','=']		# List of possible characters used between variables

INVALID_EQUATION = 'Invalid Equation'		# Global string returned when the equation is invalid

def is_equation(equation, xpos):			# Returns whether an equation is valid or not
	if xpos != -1 and '=' in equation:		# If the equation has a variable and has an equals sign then it is a valid equation
		return True
	else:									# If not, it is invalid
		return False

def find_answer(equation):					# Finds the answer to the equation
	eqn = equation.split('=')				# Splits string into two parts before and after equals sign
	for var in var_list:					# Loops through ever character in the variable list
		if var in eqn[0]:					# If a variable is in the left hand side of the equation
			return int(eqn[1].lstrip())		# then it will return the right hand side of the equation as the answer
		elif var in eqn[1]:					# Similarly, if a variable is in the right hand side of the equation
			return int(eqn[0].lstrip())		# then it will return the left hand side of the equation as the answer

def find_constants(equation, xpos):								# Finds constant in the equation
	c = check_coefficient(equation,xpos)						# Finds the coefficient for the variable
	clen = len(str(c))											# Gets the length of the coefficient
	cpos = equation.find(str(c))
	var_term = None
	if xpos == cpos+clen:	
		var_term = equation[cpos:xpos+1]
	elif c==1:
		var_term = equation[xpos]
	if xpos == cpos+clen or c==1:								# Checks if the variable is next to the coefficient (making sure)
		eqn = equation.split('=')								# Splits the equation into 2 around the equals sign
		for var in var_list:									# Goes through every possible variable
			if var in eqn[0]:									# If there is a variable in the first part of the equation then return that
				eqn = eqn[0].lstrip()
			elif var in eqn[1]:									# If there is a variable in the second part of the equation then return that
				eqn = eqn[1].lstrip()
		eqn = (eqn.replace(var_term,'')).replace(' ','')		# Remove the x term and whitespace
		eqn_value = eqn 										# New variable to store the value
		if '+' in eqn:
			eqn_value = eqn.replace('+','')						# Removes + sign for the value
		elif '-' in eqn:
			eqn_value = eqn.replace('-','')						# Removes - sign for the value
		return check_negative(eqn, eqn.find(eqn_value),int(eqn_value))  	# Returns the true value of the constant

def check_negative(equation, xpos, value):	# Checks if the coefficient is negative or positive
	xlen = len(equation[:xpos])				# Finds amount of characters before the variable
	if xpos==0:
		return value
	for pos in range(xlen,-1,-1):			# Loops from the character position and goes backwards
		if not pos>xpos:
			if '-' in equation[pos]:		# If the character at that position is equal to '-' then we return the negative of the value
				return -value
			if '+' in equation[pos]:		# If the character at that position is equal to '+' then we return the value as normal as it is positive
				return value
	return value 							# If there are no characters before the number we assume it is already positive

def check_coefficient(equation, xpos):					# Returns the coefficient of the variable
	result=[]		
	chars_before = len(equation[:xpos])					# Gets the number of characters before the position of the variable in the string
	spaced = False
	while not spaced and xpos > 0:						# Loops until every character before is checked or there are no more digits in the coefficient
		for coefficient in coefficient_list:		
			if str(coefficient) in equation[xpos-1]:	# Checks if the digit 0-9 is equal to the character
				result.append(coefficient)				# adds digit to the results array
			else:
				for space in space_list:				# Checks for characters that aren't digits to break out the loop
					if space in equation[xpos-1]:
						spaced = True					# breaks the loop as all the digits are now in the results table
		xpos -= 1										# Takes 1 from xpos so that it goes back another character
	try:
		coefficient_list_str = map(str,(list(reversed(result))))	# Reverses the results array and turns it into an array of strings
		coefficient_str = ''.join(coefficient_list_str)				# Joins items in the results array into a single string
		return int(coefficient_str)									# Turns string into integer and returns the coefficient of the variable
	except:
		return 1													# if there are no coefficients, we assume it is being multiplied by 1

def find_var(equation, xpos):						# Returns the true value of the coefficient and handles errors
	try:
		if is_equation(equation,xpos):				# Checks the equation is a valid equation
			c = check_coefficient(equation,xpos)	# Stores the coefficient of the variable in 'c'
			return check_negative(equation,xpos, c) # returns the negative or positive value of the coefficient
		else:
			return INVALID_EQUATION 				# Returns INVALID_EQUATION string if the equation is invalid
	except:
		return 'Error'								# Returns 'Error' string if something went wrong

def equation(e, var):							# Solves the equation for the variable inputted
	try:
		e = e.lower()
		vpos = e.find(var)
		c = find_var(e, vpos)					# Returns the value of the coefficient
		answer = find_answer(e)					# Returns the value the equation equals
		constant = find_constants(e, vpos)		# Finds the constant in equation
		answer -= constant 						# Will add/take constant from other answer
		eqn_answer = answer/c 					# Divides the answer by the coefficient to solve for the variable
		return var+' = '+str(eqn_answer)		# Returns "variable = answer"
	except:
		if find_var(e,var) == INVALID_EQUATION:	# Checks if find_var returns INVALID_EQUATION
			return INVALID_EQUATION				# Returns INVALID_EQUATION if it does
		else:
			return 'Error'						# If the error is not to do with it being an invalid equation, it returns 'Error'
