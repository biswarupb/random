#!/usr/bin/env python
"""
coding=utf-8

Python 3.5.2

Code to calculate the day of any given date in the Gregorian calendar using an algorithm
Algorithm: https://www.timeanddate.com/date/doomsday-weekday.html

Warnings: 
1. Performs reliably for the New Calendar introduced after 1752 (however *seems to work* upto dates in the 1600s)
2. Code does not handle exceptions robustly

"""

# Imports
import sys

def get_day(d, m, y, leap):
	"""
	Calculator method

	Uses the algorithm to find the day

	:return: Day corresponding to the DD-MM-YYYY date
	:rtype: str
	"""

	# Initializing the mappings
	dd = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
	
	# 1800-1899: Friday, 1900-1999: Wednesday, 2000-2099: Tuesday, 2100-2199: Sunday (cyclic)
	cc = {0: 5, 1: 3, 2: 2, 3: 0}

	# Follow steps of algorithm
	num1 = int((y%100)/12)
	num2 = int((y%100)%12)
	num3 = int(num2/4)
	num4 = cc[(int(y/100)-18)%4]
	num5 = (num1+num2+num3+num4)%7

	# Doomsday for Year Y
	doomsday = dd[num5]

	# Set up the doomsday dictionaries
	# List from https://www.timeanddate.com/date/doomsday-rule.html
	ddays_common = {1: 3, 2: 28, 3: 7, 4: 4, 5: 9, 6: 6, 7: 4, 7: 11, 8: 8, 9: 5, 10: 10, 11: 7, 12: 12}
	ddays_leap = {1: 4, 2: 29, 3: 7, 4: 4, 5: 9, 6: 6, 7: 4, 7: 11, 8: 8, 9: 5, 10: 10, 11: 7, 12: 12}

	dday = ddays_common[m]
	if leap:
		dday = ddays_leap[m]

	# Calculate the day
	diff = abs(dday-d)%7
	if d<dday:
		ans = (num5-diff)%7
	else:
		ans = (num5+diff)%7

	return dd[ans]

def main():
	"""
	Main method

	Takes user input and prints result

	:return: None
	:rtype: None
	"""

	# Take user input
	d = int(input("Enter DD (1-31): "))
	m = int(input("Enter MM (1-12): "))
	y = int(input("Enter YYYY: "))
	month_to_num = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
	
	# Check for invalid input
	if y<0 or m<0 or m>12 or d<0 or d>31:
		print("Invalid input. Exiting...", file=sys.stderr)
		return

	leap = False
	if y%100==0:
		if y%400==0:
			leap = True
	elif y%4==0:
		leap = True
	if leap:
		month_to_num[2] += 1
	if d>month_to_num[m]:
		print("Invalid input. Exiting...", file=sys.stderr)
		return
	
	# Print answer
	print("Day:", get_day(d, m, y, leap))

if __name__=='__main__':
	main()
