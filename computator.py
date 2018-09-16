#!/usr/bin/env python3
import sys
from regex import sub
import re
from functools import reduce

def	expr_to_parameter(expr, multiplier = 1):
	#BONUS: input validation
	if re.fullmatch(r'-?\d+(.\d+)?\*?(X(\^-?\d+(.\d+)?)?)?', expr) == None and \
		re.fullmatch(r'-?\d*(.\d+)?\*?X(\^-?\d+(.\d+)?)?', expr) == None:
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
	return (float(coeff) * multiplier, float(power))

def parse_string(poly):
	poly = poly
	if poly.count('=') != 1:
		print("Error: Badly formatted equation")
		exit(3)
	poly = poly.replace(' ', '')
	left, dummy,right = sub(r'[^\^]\K-', '+-', poly).partition('=')
	left = left.split('+')
	right = right.split('+')
	arr = []
	for expr in left:
		arr.append(expr_to_parameter(expr, 1))
	for expr in right:
		arr.append(expr_to_parameter(expr, -1))
	return (arr)

#TODO: rewrite as a lambda? How does that even work? What even is a lambda?
def euclid_gcd_iter(a, b):
	while b:
		a, b = b, a % b
	return (a)

def normalize_poly(arr):
	d = {}
	negative = 0
	for poly in arr:
		if poly[1] in d:
			d[poly[1]] += poly[0]
		else:
			d[poly[1]] = poly[0]
		if poly[1] < 0: negative += 1
	#remove nullified items
	for i, j in list(d.items()):
		if not j:
			del d[i]
	#BONUS: reduce elements
	gcd = 0
	if not 0 in d.keys() and len(d):
		#NOTE: the reduce function is to "reduce" an iterable to a single value with a function
			#NOT to mathemematically reduce the power
			#it is NOT a mathematical function. euclid_gcd_iter() is a mathematical function
		gcd = reduce(euclid_gcd_iter, d.keys())
		print("GCD:",gcd)
		d2 = {}
		for i in d.keys():
			d2[i // gcd] = d[i]
		d = d2
	#BONUS: increase order until no negatives
	smallest = min(d, default=0)
	if smallest != 0:
		d2 = {}
		for i in d.keys():
			d2[i - smallest] = d[i]
		d = d2
	return d

def print_poly(polies):
	print("Reduced form:", end=' ')
	if not len(polies):
		print(0, end=' ')
	for i in sorted(polies):
		if polies[i] < 0:
			print('- ', end='')
		elif polies[i] > 0 and i != min(polies, key=int):
			print('+ ', end='')
		if polies[i] == 1:
			if i == 0:
				print('1', end=' ')
			elif i != 1:
				print('X^{0:g} '.format(i), end=' ')
			else:
				print('X ', end='')
		elif polies[i]:
			print('{0:g} '.format(abs(polies[i])), end='')
			if i:
				print('* X', end='')
				if i != 1:
					print('^{0:g}'.format(i), end=' ')
				else:
					print(' ', end='')
	print('= 0')

def sqrt(i):
	#TODO: this
	return (i^0.5)

def solve_quad(polies):
	#BUGCHECK: no entry for power 1
	if not 1.0 in polies:
		polies[1] = 0
	discrim = polies[1] * polies[1] - 4 * polies[2] * polies[0]
	if not discrim:
		print("Discriminant is zero, the solution is:")
		print('{0:g}'.format(-polies[1] / 2 * polies[2]))
	elif discrim > 0:
		print("Discriminant is strictly positive, the two solutions are:")
		print('{0:g}'.format((-polies[1] + sqrt(discrim)) / 2 * polies[2]))
		print('{0:g}'.format((-polies[1] - sqrt(discrim)) / 2 * polies[2]))
	elif discrim < 0:
		print("Discriminant is strictly negative, the two solutions are:")
		pass

def solve_cube(polies):
	pass

def solve_poly(polies):
	degree = max(polies, default=0)
	print('Polynomial degree: {0:g}'.format(degree))
	for i in polies:
		if not i.is_integer():
			print("The polynomial has decimal powers, I can't solve.")
			return
	if degree == 0:
		if not 0 in polies:
			print("This polynomial has infinite solutions.")
		else:
			print("This polynomial has no solutions.")
	elif degree == 1:
		print("The solution is:")
		print(-polies[0]/polies[1])
	elif degree == 2:
		solve_quad(polies)
	elif degree == 3:
		solve_cube(polies)
	else:
		print("The polynomial degree is stricly greater than 2, I can't solve.")


def main():
	if len(sys.argv) != 2:
		print("Error: Invalid arguments")
		sys.exit(2)
	polynomials = parse_string(sys.argv[1])
	polynomials = normalize_poly(polynomials)
	print_poly(polynomials)
	solve_poly(polynomials)

if __name__ == "__main__":
	main()

#TODO:
# solve
