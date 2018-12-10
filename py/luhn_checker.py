#!/usr/bin/env python
"""
coding=utf-8

Python 3.5.2

Check if a identification card number is valid using Luhn Check Algorithm (mod 10)
Original patent by Hans Peter Luhn (https://patents.google.com/patent/US2950048)

Warning(s): 
1. Code does not handle exceptions or large inputs robustly

"""

# Imports
import sys

def luhn_check_generator_10(N):
	"""
	Luhn mod 10 check digit generator

	Generates the check digit of a numeric sequence using the Luhn Algorithm

	:return: Generated check digit
	:rtype: int
	"""
	# Digital sum of numbers
	digital = {0: 0, 2: 2, 4: 4, 6: 6, 8: 8, 10: 1, 12: 3, 14: 5, 16: 7, 18: 9}

	# Storing the sum
	s = 0
	for i in range(len(N)):
		if i&1:
			# Double the odd index numbers, 0-index notation
			s += digital[int(N[i])*2]
		else:
			# Keep the even index numbers as is, 0-index notation
			s += int(N[i])
	
	s *= 9
	# Mod 10
	check = s%10
	
	return check

def luhn_checker_10(N):
	"""
	Luhn mod 10 check digit checker

	Checks the check digit of a numeric sequence using the Luhn Algorithm

	:return: True if N is valid, False if invalid
	:rtype: bool
	"""

	# In this program, the last digit is taken to be the check digit
	if luhn_check_generator_10(N[:-1])==int(N[-1]):
		return True
	return False

def main():
	"""
	Main method

	Takes user input and checks or generates check digit

	:return: None
	:rtype: None
	"""

	# Take user input
	N = input("Enter number without spaces: ")
	while not N:
		print('No input detected. Please retry.', file=sys.stderr)
		N = input("Enter number to be checked without spaces: ")

	prompt = input("Generate (0) a check digit or check (1) the check digit?: ")
	if prompt=='0':
		check = luhn_check_generator_10(N)
		print('Check digit is %d' %(check))
		print('Complete number with check digit: '+N+str(check))
	else:
		if luhn_checker_10(N):
			print('Number is valid')
		else:
			print('Number is invalid')

if __name__=='__main__':
	main()
