#!/usr/bin/env python3
import sys
import re
from functools import reduce

def	expr_to_parameter(expr, multiplier = 1):
	#BONUS: input validation
	if re.fullmatch('-?\d+\*?(X(\^\d+)?)?', expr) == None and \
		re.fullmatch('-?\d*\*?X(\^\d+)?', expr) == None:
		print("Error: Badly formatted polynomial:", expr)
		exit(4)
	coeff, x, power = expr.replace('*','').replace('^', '').partition('X')
	#BONUS: natural coefficients
	if sum(c.isdigit() for c in coeff) == 0:
		if coeff == '-':
			coeff = '-1'
		else:
			coeff = '1'
	#BONUS: natural powers
	if not len(x):
		power = 0
	elif not len(power):
		power = 1
	return (float(coeff) * multiplier, int(power))

def parse_string(poly):
	poly = poly
	if poly.count('=') != 1:
		print("Error: Badly formatted equation")
		exit(3)
	left, dummy,right = poly.replace('-', '+-').replace(' ', '').partition('=')
	left = left.split('+')
	right = right.split('+')
	arr = []
	for expr in left:
		arr.append(expr_to_parameter(expr, 1))
	for expr in right:
		arr.append(expr_to_parameter(expr, -1))
	return (arr)

def euclid_gcd_recurse(a, b):
	if not a:
		return b
	else:
		return euclid_gcd_recurse(b, a % b)

def normalize_poly(arr):
	d = {}
	negative = 0
	for poly in arr:
		if poly[1] in d:
			d[poly[1]] += poly[0]
		else:
			d[poly[1]] = poly[0]
		if poly[1] < 0: negative += 1
	#BONUS: reduce elements
	gcd = 0
	if not 0 in d.keys():
		gcd = reduce(euclid_gcd_recurse, d.keys())
	if gcd:
		for item in d.keys():
			item /= gcd
	#print(d)
	return d

def print_poly(polies):
	print("Reduced form: ", end='')
	for i in range(0, max(polies, key=int) + 1):
		print(polies[i],'*X^',i, sep='', end=' ')
	print()

def main():
	if len(sys.argv) != 2:
		print("Error: Invalid arguments")
		sys.exit(2)
	polynomials = parse_string(sys.argv[1])
	polynomials = normalize_poly(polynomials)
	print(polynomials)
	print_poly(polynomials)

if __name__ == "__main__":
	main()

#TODO:
# normalize
# solve
