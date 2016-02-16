#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import signal
import copy
import sys
import wick
import sumTerms
from wick import operatorchain

## subOperators
class subOperators(object):
	def __init__(self,sign,string,scalar):
		self.sign = sign
		self.string = string
		self.scalar = scalar

## Return the subindex of the operator
def index ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")
	return auxindex[initial+1:final]

## Get sign from scalar
def getSignFromScalar ( sign, scalar ) :

	if scalar[0] == "-" :
		sign = -1	
		auxscalar = scalar[1:]
	else :
		sign = +1
		auxscalar = scalar

	return sign, auxscalar

def commutator ( A, B ) :
	AB = subOperators (+1, A + B, "")
	BA = subOperators (-1, B + A, "")
	ABBA = [AB,BA]
	return ABBA

def anticommutator ( A, B ) :
	AB = subOperators (+1, A + B, "") ## list(A) + list(B)
	BA = subOperators (+1, B + A, "")
	ABBA = [AB,BA]
	return ABBA

def superOperator ( H, v ) :
	## \hat{H} v = [v,H]_- = vH - Hv
	vH = subOperators (+1, v + H, "")
	Hv = subOperators (-1, H + v, "")
	vHHv = [vH,Hv]
	return vHHv

def calculateEpsilon ( vector ) :

	output = list()
	for operator in vector :
		epsilon = "-\epsilon_{"
		epsilon = epsilon + index(operator)
		epsilon = epsilon +"}"
		output.append(epsilon)

	return output

nmax = 2
#pQrS
V0 = subOperators (+1,["a_{p}^{\dagger}", "a_{Q}^{\dagger}","\hat{H}","a_{r}","a_{S}" ], "" )

# wX \hat{A} yZ element
# = [X^\dagger w^\dagger , \hat{A} y Z ]_+
# = X^\dagger w^\dagger \hat{A} y Z + \hat{A} y Z  X^\dagger w^\dagger
# = X^\dagger w^\dagger y Z A (1) - X^\dagger w^\dagger A y Z (2)  + 
# y Z A  X^\dagger w^\dagger (3) - A y Z  X^\dagger w^\dagger (4)

# Set the initial element
wX = V0.string[0:nmax]
Xw = wX
Xw.reverse()
A = [V0.string[nmax]] #list of one element
yZ = V0.string[nmax+1:]
AyZ = A + yZ

# expand the anticommutator and superoperator
V12 = anticommutator (Xw,AyZ)
V34 = superOperator (A,yZ)

# get all chains of operators
V1string = V12[0].string[0:nmax] + V34[0].string
V2string = V12[0].string[0:nmax] + V34[1].string

V3string = V34[0].string + V12[1].string[nmax+1:]
V4string = V34[1].string + V12[1].string[nmax+1:] 

# get all signs
V1sign = V12[0].sign * V34[0].sign
V2sign = V12[0].sign * V34[1].sign
V3sign = V12[1].sign * V34[0].sign
V4sign = V12[1].sign * V34[1].sign

# get the "scalar" factor
V1 = subOperators (V1sign,V1string, "" )
if "{H}" in V1.string[nmax*2] :
	V1.scalar = ["E"]
	del V1.string[nmax*2]
V2 = subOperators (V2sign,V2string, "" )
if "{H}" in V2.string[nmax] :
	V2.scalar = ["E"]
	V2.scalar = V2.scalar + calculateEpsilon(V2.string[nmax+1:])
	del V2.string[nmax]
V3 = subOperators (V3sign,V3string, "" )
if "{H}" in V3.string[nmax] :
	V3.scalar = ["E"]
	V3.scalar = V3.scalar + calculateEpsilon(V3.string[:nmax])
	del V3.string[nmax]
V4 = subOperators (V4sign,V4string, "" )
if "{H}" in V4.string[0] :
	V4.scalar = ["E"]
	del V4.string[0]

#reunite all four terms
allV = [V1,V2,V3,V4]
newV = list()
	
for Vi in allV :

	# Perform Wick's theorem
 	auxVi = wick.wick(Vi)

	# save only the non zero terms	
	if len(auxVi) > 0 :
		newV.append(auxVi)

expandedTerms = list()

for Vi in newV :
	#number of combinations (single, doubles) resulting from wick's theorem	
	for ncombinations in Vi:
		# number of terms (deltas)
		for iterm in ncombinations:
			# Here we expand for each "scalar"
			for iscalar in iterm.scalar:
				auxSign = 0
				auxSign, auxscalar = getSignFromScalar(auxSign,iscalar)
				auxSign = auxSign * iterm.sign
				newTerm = operatorchain ( auxSign, iterm.chain, auxscalar)
				expandedTerms.append (newTerm)	

# Sum all terms in the propagator matrix element
expandedTerms = sumTerms.sumTerms(expandedTerms)

for i in expandedTerms :
	print i.sign, i.scalar, i.chain


## =====================
## END PROGRAM
## ====================
