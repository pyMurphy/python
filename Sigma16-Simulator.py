class Machine:
	def __init__(self, code):
		self.registers = [0 for i in range(16)]		# Define 16 registers
		self.code = self.comments(code)				# Clean up tabs and comments and initialise code
		self.instructions = {
			'add':self.add,
			'div':self.div,
			'sub':self.sub,
			'mul':self.mul,
			'store':self.store,
			'load':self.load,
			'lea':self.lea
		}
		self.variables={}
		self.initialise()	# Initialise variables
	def add(self,loc,reg1,reg2):
		self.registers[int(loc)]=int(self.registers[int(reg1)])+int(self.registers[int(reg2)])		# Store reg1+reg2 in "loc" register
	def div(self,loc,reg1,reg2):
		self.registers[int(loc)]=int(int(self.registers[int(reg1)])/int(self.registers[int(reg2)]))	# Store reg1/reg2 in "loc" register
	def sub(self,loc,reg1,reg2):
		self.registers[int(loc)]=int(self.registers[int(reg1)])-int(self.registers[int(reg2)])		# Store reg1-reg2 in "loc" register
	def mul(self,loc,reg1,reg2):
		self.registers[int(loc)]=int(self.registers[int(reg1)])*int(self.registers[int(reg2)])		# Store reg1*reg2 in "loc" register
	def store(self,loc,var):
		self.variables[var]=self.registers[int(loc)]		# Store value in "loc" register in variable "var"
	def load(self,loc,var):
		self.registers[int(loc)]=self.variables[var]		# Load variable "var" into "loc" register
	def lea(self,loc,const):
		self.registers[int(loc)]=int(const)					# Load constant "const" into "loc" register
	def comments(self,code):
		clean=[]
		lines=code.split('\n')
		for line in lines:
			clean.append(line.split(';')[0].strip())		# Remove comments
		return '\n'.join(clean).replace('\t',' ').strip()	# Remove tabs
	def initialise(self):
		lines=self.code.split('\n')
		data=[]
		for line in lines:
			if 'data' in line.lower():
				data.append(line)
		for d in data:
			self.variables[d[:d.lower().find('data')].strip()]=int(d.lower().split('data')[1])		# Set variables from DATA in file
		self.code='\n'.join([item for item in lines if item not in data]).strip()					# Remove DATA from the bottom of file
	def compile(self):
		lines=self.code.split('\n')
		for i,line in enumerate(lines):
			splt=line.split()
			if len(splt)>=1:					# Check if line contains valid text
				cmd=splt[0].lower()
				if cmd in self.instructions:	# Check if line contains valid instruction
					args=line.split()[1]
					args=args.replace('[R0]','')			# Remove [R0] from arguments e.g x[R0] = x
					args=args.replace('R','').split(',')	# Remove R from arguments e.g R1 = 1
					self.instructions[cmd](*args)			# Call instruction with arguments
					print('{:04x}:'.format(i),' '.join(list(map('{:02x}'.format,self.registers))))
			self.registers[0]=0
		with open('sigma.out','w') as f:
			var=sorted(self.variables.keys())	# Sort the variables alphabetically
			w=[]
			for v in var:
				w.append('{key},{val}'.format(key=v,val=self.variables[v]))
			f.write('\n'.join(w))	# Write var,val to file

def main():
	with open('sigma.in') as f:
		code=f.read()
	sigma16 = Machine(code)
	sigma16.compile()

if __name__=='__main__':
	main()
