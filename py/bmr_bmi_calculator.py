#!/usr/bin/env python
"""
coding=utf-8

Python 3.5.2

BMR and BMI calculator based on your height, weight, age and sex

Warning(s): 
1. Code does not handle exceptions or large inputs robustly

"""

# Imports
import sys

def bmr(W, H, A, S):
	"""
	Basal Metabolic Rate calculator

	Calculates the BMR based on the Harris-Benedict Formula
	Algorithm: http://www.healthfitonline.com/resources/harris_benedict.php

	:return: The BMR in kcal/day
	:rtype: float
	"""
	if S=='XX' or S=='xx':
		# Female
		res = 655 + (4.35*W) + (4.7*H) - (4.7*A)
	else:
		# Male
		res = 66 + (6.23*W) + (12.7*H) - (6.8*A)
	return res

def bmi(W, H):
	"""
	Body Mass Index Calculator

	Calculates the BMI
	Algorithm: https://www.cdc.gov/healthyweight/assessing/bmi/childrens_bmi/childrens_bmi_formula.html

	:return: The BMI in kg/m^2
	:rtype: float
	"""
	res = 703.0*W/(H*H)
	return res

def main():
	"""
	Main method

	Takes user input and prints the Basal Metabolic Rate and Body Mass Index

	:return: None
	:rtype: None
	"""

	# Take user input
	W = float(input("Enter weight in pounds: "))
	H = float(input("Enter height in inches: "))
	A = float(input("Enter age in years: "))
	S = input("Enter XX if female, XY if male: ")

	# Calculate health data
	BMR = bmr(W, H, A, S)
	BMI = bmi(W, H)
	# https://www.cancer.org/cancer/cancer-causes/diet-physical-activity/body-weight-and-cancer-risk/adult-bmi.html
	if BMI<18.5:
		body_type = 'Underweight'
	elif BMI<25:
		body_type = 'Normal'
	elif BMI<30:
		body_type = 'Overweight'
	else:
		body_type = 'Obese'

	# Print health data
	print("-----------------BMR-----------------")
	print("BMR (kcal/day): %d" %(BMR))
	print("Required daily calorie intake with very little activity: %d" %(BMR*1.2))
	print("Required daily calorie intake with light activity: %d" %(BMR*1.375))
	print("Required daily calorie intake with moderate activity: %d" %(BMR*1.55))
	print("Required daily calorie intake with high activity: %d" %(BMR*1.725))
	print("Required daily calorie intake with very high activity: %d" %(BMR*1.9))
	print("-----------------BMI-----------------")
	print("BMI (kg/m^2): %.2f (%s)" %(BMI, body_type))

if __name__=='__main__':
	main()
