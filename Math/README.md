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

Here would be the output of the program:

```
Enter equation: 8x + 4 = 20
Enter variable: x
Result: x = 2.0
```

### Version 0.1
  + Can solve simple equations without constants, for example `4x = 8` would return `x = 2.0`
  + Checks if the equation is invalid and will return `Invalid Equation`
  + Code includes internal commentary, explaining use of the package

### Version 0.2
  + Can solve simple equations with constants, for example `8x + 4 = 20` would return `x = 2.0`
