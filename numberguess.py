# Python Number Guesser
# 
# DATE	-	03/10/2017
# USER 	-	pyMurphy
#
# Quick test to see if I can make a number guessing
# game with minimal code. Managed to get it down to
# 9 lines.

from random import randint
num=randint(0,100)
def check(i,g):
	return 'Lower' if i < g else 'Higher'
def guess():
	g=input('Number: ')
	print('Correct' if int(g)==num else check(num,int(g)))
	guess()
guess()