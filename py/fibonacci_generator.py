#!/usr/bin/env python
"""
coding=utf-8

Python 3.5.2

Generate all the Fibonacci numbers between two given numbers A and B

Warning(s): 
1. Code does not handle exceptions or large inputs robustly

"""

# Imports
import sys
import time
import math

def perfect_square(N):
	"""
	Helper function to check whether a number is a perfect square

	:return: True if number is a perfect square, False otherwise
	:rtype: bool
	"""
	if int(math.sqrt(N))*int(math.sqrt(N))==N:
		return True
	return False

def fibonacci(A, B):
	"""
	Fibonacci numbers generator

	Generates the list of Fibonacci numbers between A and B (both inclusive)

	:return: List of Fibonacci numbers
	:rtype: List[int]
	"""
	res = []
	n = A
	flag1 = flag2 = 0
	while n<=B:
		# If two numbers not yet found
		if flag1==0 or flag2==0:
			# A Fibonacci number n follows that 5*n*n+4 or 5*n*n-4 is a perfect square
			if perfect_square(5*n*n + 4) or perfect_square(5*n*n - 4):
				res.append(n)
				if flag1==0:
					flag1 = 1
					prev1 = n
					n += 1
				elif flag2==0:
					flag2 = 1
					prev2 = n
					n = prev1+prev2
			else:
				n += 1
		# Once two numbers are found, speed up by simply adding upto upper limit
		else:
			# No need to check for perfect squares
			res.append(n)
			prev1 = prev2
			prev2 = n
			n = prev1+prev2

	return res

def main():
	"""
	Main method

	Takes user input and prints the list of Fibonacci numbers in range

	:return: None
	:rtype: None
	"""

	# Take user input
	A = int(input("Enter lower limit (A): "))
	B = int(input("Enter upper limit (B): "))
	prompt = input("Print the list of Fibonacci numbers? (Y/N): ")
	if prompt=='Y' or prompt=='y':
		prompt = 1
	else:
		prompt = 0
	

	# Check for invalid input
	if A>B:
		print("Invalid input. Exiting...", file=sys.stderr)
		return
	if not A or A<0:
		A = 0
	if B<0:
		print("Found 0 Fibonacci numbers")
		return
	
	starttime = time.time()
	res = fibonacci(A, B)
	endtime = time.time()

	# Print answer
	print("Found %d Fibonacci numbers in %f seconds" %(len(res), endtime-starttime))
	
	if prompt:
		print(res)

if __name__=='__main__':
	main()
