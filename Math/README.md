# Python Equations Package

Usage:

Save equations.py in the same directory and then do
```python
from equations import equation
```

You need to pass `equation` and `variable` into the equation function
```python
eqn = input('Enter equation: ')
var = input('Enter variable: ')
print('Result: ' + equation(eqn,var))
```

### Version 0.1
  + Can solve simple equations without constants, for example `4x = 8` would return `x = 2.0`
  + Checks if the equation is invalid and will return `Invalid Equation`
  + Code includes internal commentary, explaining use of the package
