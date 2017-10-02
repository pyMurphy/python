import string

coefficient_list = [0,1,2,3,4,5,6,7,8,9]	# List of digits 0-9
var_list = list(string.ascii_lowercase)		# List of all lowercase characters
space_list = [' ','+','-','/','*','=']		# List of possible characters used in between variables

INVALID_EQUATION = 'Invalid Equation'		# Global string returned when the equation is invalid

def is_equation(equation, xpos):		# Returns whether an equation is valid or not
	if xpos != -1 and '=' in equation:		# If the equation has a variable and has an equals sign then it is a valid equation
		return True
	else:									# If not, it is invalid
		return False

def find_answer(equation):			# Finds the answer to the equation
	eqn = equation.split('=')				# Splits string into two parts before and after equals sign
	for var in var_list:					# Loops through ever character in the variable list
		if var in eqn[0]:					# If a variable is in the left hand side of the equation
			return int(eqn[1].lstrip())		# then it will return the right hand side of the equation as the answer
		elif var in eqn[1]:					# Similarly, if a variable is in the right hand side of the equation
			return int(eqn[0].lstrip())		# then it will return the left hand side of the equation as the answer

def check_negative(equation, xpos, value):		# Checks if the coefficient is negative or positive
	xlen = len(equation[:xpos])			# Finds amount of characters before the variable
	for pos in range(xlen,-1,-1):		# Loops from the character position and goes backwards
		if '-' in equation[pos]:		# If the character at that position is equal to '-' then we return the negative of the value
			return -value
		if '+' in equation[pos]:		# If the character at that position is equal to '+' then we return the value as normal as it is positive
			return value
	return value 				# If there are no characters before the number we assume it is already positive

def check_coefficient(equation, xpos):	# Returns the coefficient of the variable
	result=[]		
	chars_before = len(equation[:xpos])				# Gets the number of characters before the position of the variable in the string
	spaced = False
	while not spaced and xpos > 0:					# Loops until every character before is checked or there are no more digits in the coefficient
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
		return 1										# if there are no coefficients, we assume it is being multiplied by 1

def find_var(equation, var):	# Returns the true value of the coefficient and handles errors
	equation = equation.lower()			# Converts the equation to lowercase to check for
	try:
		xpos = equation.find(var)					# Finds the position of the variable passed into the function
		if is_equation(equation,xpos):				# Checks the equation is a valid equation
			c = check_coefficient(equation,xpos)	# Stores the coefficient of the variable in 'c'
			return check_negative(equation,xpos, c) # returns the negative or positive value of the coefficient
		else:
			return INVALID_EQUATION 			# Returns INVALID_EQUATION string if the equation is invalid
	except:
		return 'Error'				# Returns 'Error' string if something went wrong

def equation(e, var):		# Solves the equation for the variable inputted
	try:
		c = find_var(e, var)				# Returns the value of the coefficient
		answer = find_answer(e)				# Returns the value the equation equals
		eqn_answer = answer/c 				# Divides the answer by the coefficient to solve for the variable
		return var+' = '+str(eqn_answer)	# Returns "variable = answer"
	except:
		if find_var(e,var) == INVALID_EQUATION:		# Checks if find_var returns INVALID_EQUATION
			return INVALID_EQUATION					# Returns INVALID_EQUATION if it does
		else:
			return 'Error'				# If the error is not to do with it being an invalid equation, it returns 'Error'
