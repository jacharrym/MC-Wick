#!/usr/bin/python

from sympy import symbols, Function, Dummy, latex
from sympy.physics.secondquant import wicks, F, Fd, NO
from pprint import pprint

p,q,s,r,i,j,k,l,a,b,c,d = symbols("p,q,s,r,i,j,k,l,a,b,c,d")

#result = wicks(Fd(j)*Fd(p)*Fd(q)*F(s)*F(r))
#a_{j}', 'a_{p}^{\dagger}', 'a_{q}^{\dagger}', 'a_{s}', 'a_{r}

#result = wicks(Fd(p)*Fd(q)*F(s)*F(r)*Fd(j))
#a_{p}^{\dagger}', 'a_{q}^{\dagger}', 'a_{s}', 'a_{r}', 'a_{j}'

#result = wicks(Fd(p)*F(r)*Fd(j))
#a_{p}^{\dagger}', 'a_{q}^{\dagger}', 'a_{s}', 'a_{r}', 'a_{j}'

#'a_{i}^{\\dagger}', 'a_{k}', 'a_{p}^{\\dagger}', 'a_{q}

#result = wicks(Fd(i)*F(k)*Fd(p)*F(q))
#'a_{J}^{\\dagger}', 'a_{A}', 'a_{P}^{\\dagger}', 'a_{Q}'
result = wicks(Fd(j)*F(a)*Fd(p)*F(q))
#a_{p}^{\dagger}', 'a_{q}^{\dagger}', 'a_{s}', 'a_{r}', 'a_{j}'


#a_{i}^{\\dagger}', 'a_{p}^{\\dagger}', 'a_{r}', 'a_{j}
# ['a_{i}^{\\dagger}', 'a_{p}^{\\dagger}', 'a_{q}^{\\dagger}', 'a_{s}', 'a_{r}', 'a_{j}']
# ['a_{i}^{\\dagger}', 'a_{j}', 'a_{p}^{\\dagger}', 'a_{r}']
#'a_{i}^{\\dagger}', 'a_{j}', 'a_{p}^{\\dagger}', 'a_{q}^{\\dagger}', 'a_{s}', 'a_{r}']
#a_{i}^{\dagger}a_{p}^{\dagger}a_{q}^{\dagger}a_{s}a_{r}a_{j}
#a_{i}^{\dagger}a_{j}a_{p}^{\dagger}a_{q}^{\dagger}a_{s}a_{r}
print result
mystring = str(result)

print "="
printresult = True
if printresult:
	mystring = mystring.replace("+","w+")
	mystring = mystring.replace("-","w-")
	mystring = mystring.split("w")

	m = 0
	for element in mystring:
		m  = m +1
		#if not "AnnihilateFermion(j)" in element:
#		if not "CreateFermion(i)" in element:
	
		print element

