#!/usr/bin/python

from sympy import symbols, Function, Dummy, latex
from sympy.physics.secondquant import wicks, F, Fd, NO
from pprint import pprint

p,q,s,r,i,j,a = symbols("p,q,s,r,i,j,a")

result = wicks(Fd(i)*Fd(p)*Fd(q)*F(s)*F(r)*F(j))
#a_{i}^{\dagger}a_{p}^{\dagger}a_{q}^{\dagger}a_{s}a_{r}a_{j}
#a_{i}^{\dagger}a_{j}a_{p}^{\dagger}a_{q}^{\dagger}a_{s}a_{r}

mystring = str(result)

printresult = True
if printresult:
	mystring = mystring.replace("+","w+")
	mystring = mystring.replace("-","w-")
	mystring = mystring.split("w")

	m = 0
	for element in mystring:
		m  = m +1
		if not "AnnihilateFermion(j)" in element:
			print element

