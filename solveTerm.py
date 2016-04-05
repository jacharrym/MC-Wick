#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import wick
import sumTerms
import removeSinglesExcitations
import removeExcitations
from wick import operatorchain
import applydeltas
import checkDeltas

global occupiedIndexesAlpha
global virtualIndexesAlpha
global occupiedIndexesBeta
global virtualIndexesBeta

occupiedIndexesAlpha = ("i","j","k","l","m","n","o","pi","qi")
virtualIndexesAlpha  = ("a","b","c","d","e","f","g","h","pa","qa")
occupiedIndexesBeta  = ("I","J","K","L","M","N","O")
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
	#vH = subOperators (+1.0, v + H, "")
	#Hv = subOperators (-1.0, H + v, "")
	#vHHv = [vH,Hv]
	## \hat{H} v = [H,v]_- = Hv - vH
	#Hv = subOperators (+1.0, H + v, "")
	#vH = subOperators (-1.0, v + H, "")
	## \hat{H} v = [v,H]_- = -Hv + vH
	Hv = subOperators (-1.0, H + v, "")
	vH = subOperators (+1.0, v + H, "")
	HvvH = [Hv,vH]

	return HvvH

def adjoint ( chain ) :
        outChain = list()

	for i in chain :
		if "dagger" in i :
			ii = "a_{"+index(i)+"}"
		else :
			ii = "a_{"+index(i)+"}^{\dagger}"
		outChain.append(ii)
	outChain.reverse()
	return outChain


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

def basicPrinting ( vector, n ) :

	print "Result for term" + n
	for i in vector : 
		print i.sign, i.scalar, i.chain
	print "_"*20

def latexPrinting ( vector, n ) :

	print "Result for term" + n
	for i in vector : 
		if i.sign > 0 :
			print "+" + str(i.sign), 
		else :
			print i.sign,
		if "||" in i.scalar or "|" in i.scalar:
			print "\\langle", 
			for k in i.scalar :
				if len(k) == 1 :	
					print k,
				if len(k) == 2 and k.isalpha() :	
					print k[0]+"_{"+k[1]+"}",
				if len(k) == 2 and not k.isalpha() :	
					print k,

			print "\\rangle", 
		else : 
			print i.scalar,

		if len(i.chain) > 0 :
			print "(",
			for j in i.chain :
				print j,
			print ")"
		else :
			print ""
	print "_"*20




def solveTerm (nmax,V0):
	#pQrS

	# wX \hat{A} yZ element
	# = [X^\dagger w^\dagger , \hat{A} y Z ]_+
	# = X^\dagger w^\dagger \hat{A} y Z + \hat{A} y Z  X^\dagger w^\dagger
	# = X^\dagger w^\dagger y Z A (1) - X^\dagger w^\dagger A y Z (2)  + 
	# y Z A  X^\dagger w^\dagger (3) - A y Z  X^\dagger w^\dagger (4)

	# x \hat{A} y element
	# = [x^\dagger , \hat{A} y ]_+
	# = x^\dagger \hat{A} y + \hat{A} y x^\dagger 
	# = x^\dagger A (1) y - X^\dagger y A (2)  + 
	# A y x^\dagger (3) - y A x^\dagger (4)

	# Set the initial element
	wX = V0.string[0]

	#Xw = wX
	#Xw.reverse()
	
	Xw = adjoint (wX)
	
	A = [V0.string[1][0]]
	yZ = V0.string[1][1:]
	AyZ = A + yZ
	nXw = len(Xw)
	nAyZ = len(AyZ)

	print Xw,A,yZ
	#print nXw,nAyZ

	# expand the anticommutator and superoperator
	#V12 = commutator (Xw,AyZ)
	V12 = anticommutator (Xw,AyZ)
	V34 = superOperator (A,yZ)

	# get all chains of operators
	#V1string = V12[0].string[0:nXw] + V34[0].string#
	#V2string = V12[0].string[0:nXw] + V34[1].string#

	#V3string = V34[0].string + V12[1].string[nAyZ:]
	#V4string = V34[1].string + V12[1].string[nAyZ:] 

	V2string = V12[0].string[0:nXw] + V34[0].string#
	V1string = V12[0].string[0:nXw] + V34[1].string#

	V4string = V34[0].string + V12[1].string[nAyZ:]
	V3string = V34[1].string + V12[1].string[nAyZ:] 

	#print V1string
	#print V2string
	#print V3string
	#print V4string

	# get all signs
	#V1sign = V12[0].sign * V34[0].sign
	#V2sign = V12[0].sign * V34[1].sign
	#V3sign = V12[1].sign * V34[0].sign
	#V4sign = V12[1].sign * V34[1].sign

	V2sign = V12[0].sign * V34[0].sign
	V1sign = V12[0].sign * V34[1].sign
	V4sign = V12[1].sign * V34[0].sign
	V3sign = V12[1].sign * V34[1].sign


	# build each term
	V1 = subOperators (V1sign,V1string, "" )
	V2 = subOperators (V2sign,V2string, "" )
	V3 = subOperators (V3sign,V3string, "" )
	V4 = subOperators (V4sign,V4string, "" )


	#reunite all four terms
	if "\hat{H}" in A : 
		allV = [V1,V2,V3,V4]



	# Apply reference Hamiltonian operator
	if "\hat{H}" in A : 
		for i in range(0,len(allV)) :
			
			operatorPosition = allV[i].string.index("\hat{H}")
			if operatorPosition == 0 or operatorPosition == (len(allV[i].string)-1) :
				allV[i].scalar = ["E"]
				del allV[i].string[operatorPosition]
			elif operatorPosition == nXw and i == 1 :
				allV[i].scalar = ["E"]
				allV[i].scalar = allV[i].scalar + calculateEpsilon(allV[i].string[nXw+1:])
				del allV[i].string[nXw]
			elif operatorPosition == (nAyZ-1) and i == 2:
				allV[i].scalar = ["E"]
				allV[i].scalar = allV[i].scalar + calculateEpsilon(allV[i].string[:nAyZ-1])
				del allV[i].string[nAyZ-1]

			print "H"+str(i+1),allV[i].sign, allV[i].scalar, allV[i].string

	if "\hat{V}" in A : 
		allV = [V1,V2,V3,V4] #we begin from these four

	# Express perturbation operator
	if "\hat{V}" in A : 

		# intra
		#integralA = ["p","q","|","r","s"]
		#integralB = ["p","q","|","r","q"]

		# a-b
		#integralA = ["p","P","|","q","Q"]
		#integralB = ["p","Pi","|","q","Pi"]

		# b-a
		integralA = ["P","p","|","Q","q"]
		integralB = ["P","pi","|","Q","pi"]

		
		# intra
		#auxV11 = ["a_{p}^{\dagger}", "a_{q}^{\dagger}","a_{r}","a_{s}"]
		#auxV12 = ["a_{p}^{\dagger}", "a_{q}"]
		
		# inter
		#auxV11 = ["a_{p}^{\dagger}", "a_{P}^{\dagger}","a_{q}","a_{Q}"]
		auxV11 = ["a_{P}^{\dagger}", "a_{p}^{\dagger}","a_{Q}","a_{q}"]
		# a-b
		#auxV12 = ["a_{p}^{\dagger}", "a_{q}"]
		# b-a
		auxV12 = ["a_{P}^{\dagger}", "a_{Q}"]

		factorA = (1.0/2.0)
		factorB = (-1.0)

		for i in range(0,len(allV)) :

			operatorPosition = allV[i].string.index("\hat{V}")

			if operatorPosition == (len(allV[i].string)-1) :
				V12 = copy.deepcopy(allV[i])

				allV[i].sign = float(allV[i].sign*factorA)
				#V1.sign = float(V1.sign*(1.0))
				allV[i].scalar = [integralA]
				allV[i].string = allV[i].string [:] + auxV11
				del allV[i].string[operatorPosition]

				V12.sign = float(V12.sign*factorB)
				V12.scalar = [integralB]
				V12.string = V12.string [:] + auxV12
				del V12.string[operatorPosition] #{V}

			elif operatorPosition == nXw and i == 1:

				V22 = copy.deepcopy(allV[i])

				allV[i].sign = float(allV[i].sign*factorA)
				#V2.sign = float(V2.sign*(1.0))
				allV[i].scalar = [integralA]
				allV[i].string = allV[i].string[:nXw] + auxV11 + \
						V2.string[nXw+1:] #avoid V

				V22.sign = float(V22.sign*factorB)
				V22.scalar = [integralB]
				V22.string = V22.string[:nXw] + auxV12 + \
						V22.string[nXw+1:] #avoid V


			elif operatorPosition == (nAyZ-1) and i == 2:

				V32 = copy.deepcopy(allV[i])
				allV[i].sign = float(allV[i].sign*factorA)
				#V3.sign = float(V3.sign*(1.0))
				allV[i].scalar = [integralA]
				allV[i].string = allV[i].string[:nAyZ-1] + auxV11 + \
						allV[i].string[nAyZ:] #avoid V

				V32.sign = float(V32.sign*factorB)
				V32.scalar = [integralB]
				V32.string = V32.string [:nAyZ-1] + auxV12 + \
						V32.string[nAyZ:] #avoid V


			elif operatorPosition == 0 :

				V42 = copy.deepcopy(allV[i])

				allV[i].sign = float(allV[i].sign*factorA)
				#V4.sign = float(V4.sign*(1.0))
				allV[i].scalar = [integralA]

				del allV[i].string[0] #{V}
				allV[i].string = auxV11 + allV[i].string[:]

				V42.sign = float(V42.sign*factorB)
				V42.scalar = [integralB]
				del V42.string[0] #{V}
				V42.string = auxV12 + V42.string[:]


			#print "v"+str(i+1),allV[i].sign, allV[i].scalar, allV[i].string

	if "\hat{V}" in A : 
		allV = [V1,V12,V2,V22,V3,V32,V4,V42]
		#allV = [V1,V2,V3,V4]
		#allV = [V12,V22,V32,V42]
		for i in range(0,len(allV)) :
			print i+1,allV[i].sign,allV[i].string
	newV = list()
		
	i = 0
	for Vi in allV :
		i = i + 1
		#print "Vi", i
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

				if "\hat{H}" in A : 
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
	expandedTerms = sumTerms.sumTerms(expandedTerms)

	latexPrinting ( expandedTerms, "Step 1" ) 
	#basicPrinting ( expandedTerms, "1" ) 

	if "\hat{H}" in A : 
		#print "call to check deltas!"
		expandedTerms = checkDeltas.checkDeltas (expandedTerms,	wX, yZ)

	if "\hat{V}" in A : 
		#print "call to apply deltas!"
		expandedTerms = applydeltas.applyDeltas (expandedTerms)


	latexPrinting ( expandedTerms, "Step 2" ) 

	# Sum all terms in the propagator matrix element
	expandedTerms = sumTerms.sumTerms(expandedTerms)

	latexPrinting ( expandedTerms, "Step 3" ) 

	if "\hat{V}" in A or "\hat{H}" in A: 
		expandedTerms = removeExcitations.removeExcitations(expandedTerms)

	latexPrinting ( expandedTerms, "Step 4" ) 

	if "\hat{V}" in A : 
		#print "call to apply deltas!"
		expandedTerms = applydeltas.applyDeltas (expandedTerms)


	# Sum all terms in the propagator matrix element
	expandedTerms = sumTerms.sumTerms(expandedTerms)

	latexPrinting ( expandedTerms, "Step 5" ) 


	if "\hat{V}" in A : 
		#print "call to apply deltas!"
		expandedTerms = checkDeltas.checkDeltas (expandedTerms,	wX, yZ)


	#basicPrinting ( expandedTerms, "5" ) 
	latexPrinting ( expandedTerms, "Step 6" ) 

	return expandedTerms


## =====================
## END PROGRAM
## ====================
