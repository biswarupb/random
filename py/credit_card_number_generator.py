#!/usr/bin/env python
"""
coding=utf-8

Python 3.5.2

Credit card numbers generator
Useful demo of what this code aims to do: https://developer.paypal.com/developer/creditCardGenerator/

Warning(s): 
1. The card numbers generated are random and are to be used only for testing purposes in legally allowed settings
2. Code does not handle exceptions or large inputs robustly

"""

# Imports
import sys
import random

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

def main():
	"""
	Main method

	Takes user input and generates a set of credit card numbers

	:return: None
	:rtype: None
	"""

	# Take user input
	N = int(input("How many credit card numbers are to be generated?: "))

	# Visa, Mastercard, Amex, Discover, Maestro, JCB, Diners International, Diners US & Canada, RuPay, MIR

	# Prefixes for the card networks
	# Retrived from https://en.wikipedia.org/wiki/Payment_card_number
	networks = {}
	networks['Visa'] = ['4']
	networks['Mastercard'] = ['51', '52', '53', '54', '55']
	for i in range(222100, 272100):
		networks['Mastercard'].append(str(i))
	networks['American Express'] = ['34', '37']
	networks['Discover'] = ['6011', '64', '65']
	networks['Maestro'] = ['50', '56', '57', '58', '639', '67']
	networks['JCB'] = []
	for i in range(3528, 3590):
		networks['JCB'].append(str(i))
	networks['Diners Club International'] = ['36', '300', '301', '302', '303', '304', '305', '3095', '38', '39']
	networks['Diners Club US & Canada'] = ['54', '55'] # 55 is co-branded with Mastercard
	networks['RuPay'] = ['60', '6521', '6522']
	networks['MIR'] = ['2200', '2201', '2202', '2203', '2204']

	netkeys = list(networks.keys())

	# A list of numbers from 0 to 9 (inclusive) for later use
	buff = [str(i) for i in range(10)]

	# Randomly choose card networks and number distribution among these networks
	for i in range(N):
		# Choose a random network
		chosen = random.choice(netkeys)
		# Choose randomly an allowed prefix depending on network
		ccnumber = random.choice(networks[chosen])

		# Generate a random list of numbers except the check digit and the prefix
		netlength = 16
		if chosen=='American Express':
			netlength = 15 # Amex has 15 length CC numbers
		rem = netlength-len(ccnumber)-1
		while rem:
			ccnumber += random.choice(buff)
			rem -= 1

		# Generate check digit using the Luhn Algorithm
		ccnumber += str(luhn_check_generator_10(ccnumber))

		# Print card number and respective card network
		if chosen=='American Express':
			print(ccnumber+'  ('+chosen+')') # Extra space because of 15 digits
		else:
			print(ccnumber+' ('+chosen+')')


if __name__=='__main__':
	main()
