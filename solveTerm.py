#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import wick
import sumTerms
import removeSinglesExcitations
from wick import operatorchain
import applydeltas

global occupiedIndexesAlpha
global virtualIndexesAlpha
global occupiedIndexesBeta
global virtualIndexesBeta

occupiedIndexesAlpha = ("i","j","k","l","m","n","o","p","q","r","s")
virtualIndexesAlpha  = ("a","b","c","d","e","f","g","h")
occupiedIndexesBeta  = ("I","J","K","L","M","N","O","P","Q","R","S")
virtualIndexesBeta  = ("A","B","C","D","E","F","G","H")

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
	elif scalar[0] == "+" :
		sign = +1
		auxscalar = scalar[1:]
	else :
		sign = +1
		auxscalar = scalar

	return sign, auxscalar

def commutator ( A, B ) :
	AB = subOperators (+1.0, A + B, "")
	BA = subOperators (-1.0, B + A, "")
	ABBA = [AB,BA]
	return ABBA

def anticommutator ( A, B ) :
	AB = subOperators (+1.0, A + B, "") ## list(A) + list(B)
	BA = subOperators (+1.0, B + A, "")
	ABBA = [AB,BA]
	return ABBA

def superOperator ( H, v ) :
	## \hat{H} v = [v,H]_- = vH - Hv
	vH = subOperators (+1.0, v + H, "")
	Hv = subOperators (-1.0, H + v, "")
	vHHv = [vH,Hv]
	return vHHv

def calculateEpsilon ( vector ) :

	output = list()
	for operator in vector :

		indexi = index(operator)
		if indexi.isupper() : # beta species
			if indexi in occupiedIndexesBeta  : #
				epsilon = "-\epsilon_{"
			if indexi in virtualIndexesBeta  : #
				epsilon = "+\epsilon_{"
		if indexi.islower() : # alpha species
			if indexi in occupiedIndexesAlpha : #
				epsilon = "-\epsilon_{"
			if indexi in virtualIndexesAlpha : #
				epsilon = "+\epsilon_{"

		epsilon = epsilon + indexi
		epsilon = epsilon +"}"
		output.append(epsilon)

	return output

def solveTerm (nmax,V0):
	#nmax = 2
	#pQrS
	#V0 = subOperators (+1,["a_{a}^{\dagger}", "a_{B}^{\dagger}","\hat{H}","a_{k}","a_{C}" ], "" )
	print V0.string

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
	#V12 = anticommutator (Xw,AyZ)
	V12 = commutator (Xw,AyZ)
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

	# build each term
	V1 = subOperators (V1sign,V1string, "" )
	V2 = subOperators (V2sign,V2string, "" )
	V3 = subOperators (V3sign,V3string, "" )
	V4 = subOperators (V4sign,V4string, "" )

	# Apply reference Hamiltonian operator
	if V0.string[nmax] == "\hat{H}": 
		if "{H}" in V1.string[nmax*2] :
			V1.scalar = ["E"]
			del V1.string[nmax*2]
		if "{H}" in V2.string[nmax] :
			V2.scalar = ["E"]
			V2.scalar = V2.scalar + calculateEpsilon(V2.string[nmax+1:])
			del V2.string[nmax]
		if "{H}" in V3.string[nmax] :
			V3.scalar = ["E"]
			V3.scalar = V3.scalar + calculateEpsilon(V3.string[:nmax])
			del V3.string[nmax]
		if "{H}" in V4.string[0] :
			V4.scalar = ["E"]
			del V4.string[0]

	# Express perturbation operator
	if V0.string[nmax] == "\hat{V}": 

		integralA = "pq||rs"
		integralB = "po||ro"
		auxV11 = ["a_{p}^{\dagger}", "a_{q}^{\dagger}","a_{s}","a_{r}"]
		auxV12 = ["a_{p}^{\dagger}", "a_{r}"]

		if "{V}" in V1.string[nmax*2] :
			V12 = copy.deepcopy(V1)

			V1.sign = float(V1.sign*(1.0/4.0))
			#V1.sign = float(V1.sign*(1.0))
			V1.scalar = [integralA]
			V1.string = V1.string [:] + auxV11
			del V1.string[nmax*2] #{V}

			V12.sign = float(V12.sign*(-1.0))
			V12.scalar = [integralB]
			V12.string = V12.string [:] + auxV12
			del V12.string[nmax*2] #{V}

		if "{V}" in V2.string[nmax] :
			V22 = copy.deepcopy(V2)

			V2.sign = float(V2.sign*(1.0/4.0))
			#V2.sign = float(V2.sign*(1.0))
			V2.scalar = [integralA]
			V2.string = V2.string[:nmax] + auxV11 + \
					V2.string[nmax+1:] #avoid V

			V22.sign = float(V22.sign*(-1.0))
			V22.scalar = [integralB]
			V22.string = V22.string [:nmax] + auxV12 + \
					V22.string[nmax+1:] #avoid V

		if "{V}" in V3.string[nmax] :
			V32 = copy.deepcopy(V3)

			V3.sign = float(V3.sign*(1.0/4.0))
			#V3.sign = float(V3.sign*(1.0))
			V3.scalar = [integralA]
			V3.string = V3.string[:nmax] + auxV11 + \
					V3.string[nmax+1:] #avoid V
			V32.sign = float(V32.sign*(-1.0))
			V32.scalar = [integralB]
			V32.string = V32.string [:nmax] + auxV12 + \
					V32.string[nmax+1:] #avoid V

		if "{V}" in V4.string[0] :
			V42 = copy.deepcopy(V4)

			V4.sign = float(V4.sign*(1.0/4.0))
			#V4.sign = float(V4.sign*(1.0))
			V4.scalar = [integralA]

			del V4.string[0] #{V}
			V4.string = auxV11 + V4.string[:]

			V42.sign = float(V42.sign*(-1.0))
			V42.scalar = [integralB]
			del V42.string[0] #{V}
			V42.string = auxV12 + V42.string[:]



	#reunite all four terms
	if V0.string[nmax] == "\hat{H}": 
		allV = [V1,V2,V3,V4]

		print "v1",V1.sign, V1.scalar, V1.string
		print "v2",V2.sign, V2.scalar, V2.string
		print "v3",V3.sign, V3.scalar, V3.string
		print "v4",V4.sign, V4.scalar, V4.string

	if V0.string[nmax] == "\hat{V}": 
		allV = [V1,V12,V2,V22,V3,V32,V4,V42]
		#allV = [V1,V2,V3,V4]

		#allV = [V1]
		#allV = [V1,V12]
		print "v1",V1.sign, V1.scalar, V1.string
		print "v21",V12.sign, V12.scalar, V12.string
		print "v2",V2.sign, V2.scalar, V2.string
		print "v22",V22.sign, V22.scalar, V22.string
		print "v3",V3.sign, V3.scalar, V3.string
		print "v32",V32.sign, V32.scalar, V32.string
		print "v4",V4.sign, V4.scalar, V4.string
		print "v42",V42.sign, V42.scalar, V42.string

	newV = list()
		
	i = 0
	for Vi in allV :
		i = i + 1
		print i
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
				# remove hamiltoniand matrix elements between ground state and single excitations determinants.

				if V0.string[nmax] == "\hat{H}": 
					removeiterm = removeSinglesExcitations.removeSinglesExcitations(iterm)
				else :
					removeiterm = False
				if not removeiterm :
				# Here we expand for each "scalar"
				# Sum all terms in the propagator matrix element
					for iscalar in iterm.scalar:
						auxSign = 0
						auxSign, auxscalar = getSignFromScalar(auxSign,iscalar)
						auxSign = auxSign * iterm.sign
						newTerm = operatorchain ( auxSign, iterm.chain, auxscalar)
						expandedTerms.append (newTerm)	


	# Sum all terms in the propagator matrix element
	#print "summing"
	expandedTerms = sumTerms.sumTerms(expandedTerms)

	print "Result for term1"
	for i in expandedTerms :
		print i.sign, i.scalar, i.chain


	if V0.string[nmax] == "\hat{V}": 
		#print "call to apply deltas!"
		expandedTerms = applydeltas.applyDeltas (expandedTerms)

	print "Result for term2"
	for i in expandedTerms :
		print i.sign, i.scalar, i.chain

	# Sum all terms in the propagator matrix element
	expandedTerms = sumTerms.sumTerms(expandedTerms)

	print "Result for term3"
	for i in expandedTerms :
		print i.sign, i.scalar, i.chain
	print "="


	return expandedTerms


## =====================
## END PROGRAM
## ====================
