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

	Generates the check digit of a numeric sequence using Luhn Algorithm

	:return: Generated check digit
	:rtype: int
	"""
	digital = {0: 0, 2: 2, 4: 4, 6: 6, 8: 8, 10: 1, 12: 3, 14: 5, 16: 7, 18: 9}
	s = 0
	for i in range(len(N)):
		if i&1:
			s += digital[int(N[i])*2]
		else:
			s += int(N[i])
	s *= 9
	check = s%10
	return check

def luhn_checker_10(N):
	"""
	Luhn mod 10 check digit checker

	Checks the check digit of a numeric sequence using Luhn Algorithm

	:return: True if N is valid, False if invalid
	:rtype: bool
	"""
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
