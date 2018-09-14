import sys
import collections
import re

Parameter = collections.namedtuple('Parameter', ['coefficient', 'power'])

def parse_string(poly):
	poly = poly.replace('+', '|').replace('-', '|-').replace(' ', '')
	if poly.count('=') != 1:
		print("Error: Badly formatted equation")
		exit(3)
	left, dummy,right = poly.partition('=')
	left = left.split('|')
	right = right.split('|')
	arr = []
	for expr in left:
		if re.fullmatch('-?\d+\*?(X(\^\d+)?)?', expr) == None and \
			re.fullmatch('-?\d*\*?X(\^\d+)?', expr) == None:
			print(expr)
			print("Error: Badly formatted polynomial")
			exit(4)
		print(expr.replace('*','').replace('^', '').partition('X'))
		coeff, x, power = expr.replace('*','').replace('^', '').partition('X')
		if sum(c.isdigit() for c in coeff) == 0:
			if coeff == '-':
				coeff = '-1'
			else:
				coeff = '1'
		if not len(x):
			power = 0
		elif not len(power):
			power = 1
		print(int(coeff),'X^', int(power))
		arr.append(Parameter(int(coeff), int(power)))
	for expr in right:
		if re.fullmatch('-?\d+\*?(X(\^\d+)?)?', expr) == None and \
			re.fullmatch('-?\d*\*?X(\^\d+)?', expr) == None:
			print(expr)
			print("Error: Badly formatted polynomial")
			exit(4)
		print(expr.replace('*','').replace('^', '').partition('X'))
		coeff, x, power = expr.replace('*','').replace('^', '').partition('X')
		if sum(c.isdigit() for c in coeff) == 0:
			if coeff == '-':
				coeff = '-1'
			else:
				coeff = '1'
		if not len(x):
			power = 0
		elif not len(power):
			power = 1
		print(-int(coeff),'X^', int(power))
		arr.append(Parameter(-int(coeff), int(power)))
	return (arr)
		
		

def main():
	if len(sys.argv) != 2:
		print("Error: Invalid arguments")
		sys.exit(2)
	parse_string(sys.argv[1])

if __name__ == "__main__":
	main()

#TODO:
# normalize
# solve
