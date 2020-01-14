from math import *
from sympy import *

def calc_dim(size,degree_in):
	degree = abs(degree_in)
	length = size[0]
	width = size[1]

	a=width
	b=length

	x = Symbol('x')
	y = Symbol('y')

	'''
	print('cot:',cot(degree))
	print('sin:',sin(degree))
	print('cos:',cos(degree))
	print('tan:',tan(degree))
	'''
	output = solve([2*(x+y)+a*tan(degree)-b/cos(degree)-b,y*sin(degree)+a/cos(degree)-b/(sin(degree)*cos(degree))+y/sin(degree)+b*cot(degree)-y*cos(degree)*cot(degree)-a],[x, y])
	#print(output)

	slnx = int(output[x])
	slny = int(output[y])
	#if degree_in >=0:
	#print(slnx,length-slnx-slny)
	return [slnx,length-slnx-slny]
	#elif degree_in < 0:
		#return [length-slnx-slny,slnx]
	
