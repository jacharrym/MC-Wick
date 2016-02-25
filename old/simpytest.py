#!/usr/bin/python

from sympy import symbols, Function, Dummy, latex
from sympy.physics.secondquant import wicks, F, Fd, NO
from pprint import pprint

p,q,s,r,i,a = symbols("p,q,s,r,i,a")
result = wicks(Fd(a)*Fd(i)*Fd(p)*F(r))
#a_{a}^{\dagger}a_{i}a_{p}^{\dagger}a_{r}
#'a_{p}^{\\dagger}', 'a_{q}^{\\dagger}', 'a_{s}', 'a_{r}', 'a_{i}', 'a_{a}^{\\dagger}'
print result

result = ("KroneckerDelta(_i, r)*KroneckerDelta(a, r)*NO(CreateFermion(i)*CreateFermion(p)) - KroneckerDelta(_i, r)*KroneckerDelta(i, r)*NO(CreateFermion(a)*CreateFermion(p)) + KroneckerDelta(_i, r)*KroneckerDelta(p, r)*NO(CreateFermion(a)*CreateFermion(i)) + NO(CreateFermion(a)*CreateFermion(i)*CreateFermion(p)*AnnihilateFermion(r))")
result = result.replace("+","w+")
result = result.replace("-","w-")
result = result.split("w")

for element in result:
	#if not "NO" in element:
	print element

