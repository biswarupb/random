#!/usr/bin/env python
"""
coding=utf-8

Python 3.5.2

Generate all the prime numbers between two given numbers A and B

Warning(s): 
1. Code does not handle exceptions or large inputs robustly

"""

# Imports
import sys
import time
import math

def naive(A, B):
	"""
	Naive method

	Generates the list of primes between A and B (both inclusive)
	Time Complexity: O((B-A) sqrt(B))
	Space Complexity: O(B-A)

	:return: List of prime numbers
	:rtype: List[int]
	"""
	if B<=2:
		return [2]

	primes = []

	for p in range(A, B+1):
		ctr = 0
		if p==2:
			primes.append(2)
		elif p&1:
			# Check only the odd numbers
			for i in range(3, int(p**0.5)+1, 2):
				if p%i == 0:
					ctr = 1
					break
			if ctr==0 and p!=1 and p!=0:
				primes.append(p)

	return primes

def eratosthenes(A, B):
	"""
	Sieve of Eratosthenes

	Generates the list of primes between A and B (both inclusive)
	Algorithm: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
	Time Complexity: O(B log log B)
	Space Complexity: O(B)

	:return: List of prime numbers
	:rtype: List[int]
	"""
	# Mark all numbers as prime
	N = B
	primes = [True] * (N+1)
	primes[0] = primes[1] = False

	for p in range(N+1):
		if primes[p]:
			# Mark multiples of p by counting to N from 2p in increments of p, and mark them as False
			# 2p, 3p, 4p, ...
			for f in range(p*p, N+1, p):
				primes[f] = False

	# The True indices mark the prime numbers
	return [p for p in range(A, len(primes)) if primes[p]==True]

def segmented_eratosthenes(A, B):
	"""
	Segmented Sieve of Eratosthenes

	Generates the list of primes between A and B (both inclusive)
	Time Complexity: O(B log log B)
	Space Complexity: O(B)

	Adapted from: https://github.com/andrewstewart/segsieve/blob/master/primes.py

	:return: List of prime numbers
	:rtype: List[int]
	"""

	_prime1000 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
	if B<1000:
		return [p for p in _prime1000 if p>=A and p<=B]

	segfactor = 0.2
	delta = int(math.ceil(math.sqrt(B-A)*abs(segfactor)))

	sep = (B-A)//delta + 1
	primes = segmented_eratosthenes(2, int(math.sqrt(B))+1)
	primes2 = segmented_eratosthenes(2, int(math.sqrt(sep)+1))
	q = len(primes2)
	while q>0 and primes2[0]<A:
		primes2.pop(0)
		q -= 1
	a = A
	while a<B:
		if a+sep>B:
			sep = B-a
		b = [True] * sep
		if a<2:
			if a==1:
				b[0] = False
			if a==0:
				b[:1] = [False, False]
		stop2 = int(math.ceil(math.sqrt(a + sep)))
		for c in primes:
			if c>stop2:
				break
			q = a%c
			if q!=0:
				d = a-q+c
			else:
				d = a
			while d<a+sep:
				b[d-a] = False
				d += c
		for c in range(sep):
			if b[c]:
				primes2.append(a+c)
		a += sep

	return primes2

def atkin(A, B):
	"""
	Sieve of Atkin

	Generates the list of primes between A and B (both inclusive)
	Algorithm: https://en.wikipedia.org/wiki/Sieve_of_Atkin
	Time Complexity: O(B / (log log B))
	Space Complexity: O(B)

	:return: List of prime numbers
	:rtype: List[int]
	"""
	N = B
	primes = []
	if B<3:
		return [2]
	
	primes = [False] * (N+1)
	primes[2] = primes[3] = True

	x = 1
	while x*x<N: 
		y = 1
		while y*y<N: 
			# a) p = (4*x*x)+(y*y) has odd number of solutions and p % 12 = 1 or p % 12 = 5 
			p = (4*x*x)+(y*y) 
			if p<=N and (p%12 == 1 or p%12 == 5): 
				primes[p] ^= True
			
			# b) p = (3*x*x)+(y*y) has odd number of solutions and p % 12 = 7 
			p = (3*x*x)+(y*y)
			if p<=N and p%12 == 7: 
				primes[p] ^= True

			# c) p = (3*x*x)-(y*y) has odd number of solutions, x > y and p % 12 = 11 
			p = (3*x*x)-(y*y)
			if x>y and p<=N and p%12 == 11: 
				primes[p] ^= True
			y += 1
		x += 1

	# Mark all multiples of squares
	r = 5
	while r*r<N: 
		if primes[r]: 
			for f in range(r*r, B+1, r*r): 
				primes[f] = False
		r += 1

	# The True indices mark the prime numbers
	return [p for p in range(A, len(primes)) if primes[p]==True]

def sundaram(A, B):
	"""
	Sieve of Sundaram

	Generates the list of primes between A and B (both inclusive)
	Algorithm: https://en.wikipedia.org/wiki/Sieve_of_Sundaram
	Time Complexity: O(B log B)
	Space Complexity: O(B)

	:return: List of prime numbers
	:rtype: List[int]
	"""

	# Get new limit
	N = int((B-2)/2)
	# Mark all as False
	not_primes = [False] * (N+1)

	for i in range(1, N+1):
		j = i
		while i+j+2*i*j <= N:
			not_primes[i+j+2*i*j] = True
			j += 1

	if A<=2:
		return [2]+[2*p+1 for p in range(1, N+1) if not_primes[p]==False and (2*p+1)>=A and (2*p+1)<=B]
	return [2*p+1 for p in range(1, N+1) if not_primes[p]==False and (2*p+1)>=A and (2*p+1)<=B]

def main():
	"""
	Main method

	Takes user input and prints the list of primes

	:return: None
	:rtype: None
	"""

	# Take user input
	A = int(input("Enter lower limit (A): "))
	B = int(input("Enter upper limit (B): "))
	print ("""
	1. Naive Method
	2. Sieve of Eratosthenes
	3. Segmented Eratosthenes
	4. Sieve of Atkin
	5. Sieve of Sundaram
	6. All
	""")
	method = int(input("Choose method (1-6): "))
	prompt = input("Print the list of primes? (Y/N): ")
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
	if B<=1:
		print("Found 0 primes")
		return
	
	starttime = time.time()
	if method==1:
		res = naive(A, B)
	elif method==2:
		res = eratosthenes(A, B)
	elif method==3:
		res = segmented_eratosthenes(A, B)
	elif method==4:
		res = atkin(A, B)
	elif method==5:
		res = sundaram(A, B)
	endtime = time.time()

	# Print answer
	if method==1:
		print("Using Naive Method -> Found %d primes in %f seconds" %(len(res), endtime-starttime))
	elif method==2:
		print("Using Sieve of Eratosthenes -> Found %d primes in %f seconds" %(len(res), endtime-starttime))
	elif method==3:
		print("Using Segmented Sieve of Eratosthenes -> Found %d primes in %f seconds" %(len(res), endtime-starttime))
	elif method==4:
		print("Using Sieve of Atkin -> Found %d primes in %f seconds" %(len(res), endtime-starttime))
	elif method==5:
		print("Using Sieve of Sundaram -> Found %d primes in %f seconds" %(len(res), endtime-starttime))
	else:
		print("Sl\tMethod\t\t# Primes\tTime (s)")
		
		starttime = time.time()
		res = naive(A, B)
		endtime = time.time()
		print("1\tNaive\t\t%d\t\t%f" %(len(res), endtime-starttime))
		
		starttime = time.time()
		res = eratosthenes(A, B)
		endtime = time.time()
		print("2\tEratosthenes\t%d\t\t%f" %(len(res), endtime-starttime))
		
		starttime = time.time()
		res = segmented_eratosthenes(A, B)
		endtime = time.time()
		print("3\tSeg-Eratos\t%d\t\t%f" %(len(res), endtime-starttime))
		
		starttime = time.time()
		res = atkin(A, B)
		endtime = time.time()
		print("4\tAtkin\t\t%d\t\t%f" %(len(res), endtime-starttime))
		
		starttime = time.time()
		res = sundaram(A, B)
		endtime = time.time()
		print("5\tSundaram\t%d\t\t%f" %(len(res), endtime-starttime))
	
	if prompt:
		print(res)

if __name__=='__main__':
	main()
