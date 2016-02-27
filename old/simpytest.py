#!/usr/bin/python

from sympy import symbols, Function, Dummy, latex
from sympy.physics.secondquant import wicks, F, Fd, NO
from pprint import pprint

p,q,s,r,i,j,a = symbols("p,q,s,r,i,j,a")

result = wicks(F(i)*Fd(j)*Fd(p)*Fd(q)*F(s)*F(r)  )
#1 b_{i}b_{j}^{\dagger}b_{p}^{\dagger}b_{q}^{\dagger}b_{s}b_{r}

mystring = str(result)

printresult = True
if printresult:
	mystring = mystring.replace("+","w+")
	mystring = mystring.replace("-","w-")
	mystring = mystring.split("w")

	m = 0
	for element in mystring:
		m  = m +1
		if not "AnnihilateFermion(i)" in element:
			print element

