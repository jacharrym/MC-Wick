#!/usr/bin/python

from sympy import symbols, Function, Dummy, latex
from sympy.physics.secondquant import wicks, F, Fd, NO
from pprint import pprint

p,q,s,r,i,a = symbols("p,q,s,r,i,a")
result = wicks(F(p)*F(q)*Fd(s)*Fd(r)*Fd(i)*Fd(a))
#'a_{p}^{\\dagger}', 'a_{q}^{\\dagger}', 'a_{s}', 'a_{r}', 'a_{i}', 'a_{a}^{\\dagger}'
print result

result=("KroneckerDelta(_a, s)*KroneckerDelta(_a, r)*KroneckerDelta(p, s)*KroneckerDelta(q, r)*NO(CreateFermion(a)*CreateFermion(i)) - KroneckerDelta(_a, s)*KroneckerDelta(_a, i)*KroneckerDelta(i, q)*KroneckerDelta(p, s)*NO(CreateFermion(a)*CreateFermion(r)) + KroneckerDelta(_a, s)*KroneckerDelta(_a, a)*KroneckerDelta(a, q)*KroneckerDelta(p, s)*NO(CreateFermion(i)*CreateFermion(r)) - KroneckerDelta(_a, s)*KroneckerDelta(p, s)*NO(CreateFermion(a)*CreateFermion(i)*CreateFermion(r)*AnnihilateFermion(q)) - KroneckerDelta(_a, r)*KroneckerDelta(_a, s)*KroneckerDelta(p, r)*KroneckerDelta(q, s)*NO(CreateFermion(a)*CreateFermion(i)) + KroneckerDelta(_a, r)*KroneckerDelta(_a, i)*KroneckerDelta(i, q)*KroneckerDelta(p, r)*NO(CreateFermion(a)*CreateFermion(s)) - KroneckerDelta(_a, r)*KroneckerDelta(_a, a)*KroneckerDelta(a, q)*KroneckerDelta(p, r)*NO(CreateFermion(i)*CreateFermion(s)) + KroneckerDelta(_a, r)*KroneckerDelta(p, r)*NO(CreateFermion(a)*CreateFermion(i)*CreateFermion(s)*AnnihilateFermion(q)) + KroneckerDelta(_a, i)*KroneckerDelta(_a, s)*KroneckerDelta(i, p)*KroneckerDelta(q, s)*NO(CreateFermion(a)*CreateFermion(r)) - KroneckerDelta(_a, i)*KroneckerDelta(_a, r)*KroneckerDelta(i, p)*KroneckerDelta(q, r)*NO(CreateFermion(a)*CreateFermion(s)) + KroneckerDelta(_a, i)*KroneckerDelta(_a, a)*KroneckerDelta(a, q)*KroneckerDelta(i, p)*NO(CreateFermion(r)*CreateFermion(s)) - KroneckerDelta(_a, i)*KroneckerDelta(i, p)*NO(CreateFermion(a)*CreateFermion(r)*CreateFermion(s)*AnnihilateFermion(q)) - KroneckerDelta(_a, a)*KroneckerDelta(_a, s)*KroneckerDelta(a, p)*KroneckerDelta(q, s)*NO(CreateFermion(i)*CreateFermion(r)) + KroneckerDelta(_a, a)*KroneckerDelta(_a, r)*KroneckerDelta(a, p)*KroneckerDelta(q, r)*NO(CreateFermion(i)*CreateFermion(s)) - KroneckerDelta(_a, a)*KroneckerDelta(_a, i)*KroneckerDelta(a, p)*KroneckerDelta(i, q)*NO(CreateFermion(r)*CreateFermion(s)) + KroneckerDelta(_a, a)*KroneckerDelta(a, p)*NO(CreateFermion(i)*CreateFermion(r)*CreateFermion(s)*AnnihilateFermion(q)) + KroneckerDelta(_a, s)*KroneckerDelta(q, s)*NO(CreateFermion(a)*CreateFermion(i)*CreateFermion(r)*AnnihilateFermion(p)) - KroneckerDelta(_a, r)*KroneckerDelta(q, r)*NO(CreateFermion(a)*CreateFermion(i)*CreateFermion(s)*AnnihilateFermion(p)) + KroneckerDelta(_a, i)*KroneckerDelta(i, q)*NO(CreateFermion(a)*CreateFermion(r)*CreateFermion(s)*AnnihilateFermion(p)) - KroneckerDelta(_a, a)*KroneckerDelta(a, q)*NO(CreateFermion(i)*CreateFermion(r)*CreateFermion(s)*AnnihilateFermion(p)) + NO(CreateFermion(a)*CreateFermion(i)*CreateFermion(r)*CreateFermion(s)*AnnihilateFermion(p)*AnnihilateFermion(q))")
result = result.replace("+","w+")
result = result.replace("-","w-")
result = result.split("w")

for element in result:
	#if not "NO" in element:
	print element

