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
	if len(vector) > 0 :
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
	else :
		print 0	
	print "_"*20


#V0 = subOperators (+1,['a_{i}^{\dagger}', 'a_{a}','a_{pi}^{\dagger}', 'a_{qi}','a_{b}^{\dagger}', 'a_{j}'],"")
#V0 = subOperators (+1,['a_{i}^{\dagger}', 'a_{a}','a_{pi}^{\dagger}','a_{ri}^{\dagger}', 'a_{qi}', 'a_{si}','a_{b}^{\dagger}', 'a_{j}'],"")


# build each term

V1sign = 1
#factorA = (1.0)
factorA = (1.0/2.0)
#integralA = ["p","|","q"]
integralA = ["p","q","|","r","s"]
V1scalar = [integralA]

# SS
#V1string = ['a_{i}^{\dagger}', 'a_{a}','a_{p}^{\dagger}','a_{q}', 'a_{b}^{\dagger}', 'a_{j}']
#V1string = ['a_{i}^{\dagger}', 'a_{a}','a_{p}^{\dagger}','a_{q}^{\dagger}', 'a_{s}', 'a_{r}','a_{b}^{\dagger}', 'a_{j}']

# 0 D
#V1string = ['a_{p}^{\dagger}','a_{q}', 'a_{b}^{\dagger}', 'a_{j}','a_{a}^{\dagger}', 'a_{i}']
V1string = ['a_{p}^{\dagger}','a_{q}^{\dagger}', 'a_{s}', 'a_{r}','a_{b}^{\dagger}', 'a_{j}','a_{a}^{\dagger}', 'a_{i}']

V1sign = float(V1sign*factorA)

V1 = subOperators (V1sign,V1string, V1scalar )

#allV = [V1,V2]
allV = [V1]

newV = list()

A = ["\hat{V}"]
	
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

#latexPrinting ( expandedTerms, "Step 1" ) 

if "\hat{H}" in A : 
	#print "call to check deltas!"
	expandedTerms = checkDeltas.checkDeltas (expandedTerms,	wX, yZ)

if "\hat{V}" in A[0] : 
	#print "call to apply deltas!"
	expandedTerms = applydeltas.applyDeltas (expandedTerms)


#latexPrinting ( expandedTerms, "Step 2" ) 

# Sum all terms in the propagator matrix element
expandedTerms = sumTerms.sumTerms(expandedTerms)

#latexPrinting ( expandedTerms, "Step 3" ) 

if "\hat{V}" in A[0] or "\hat{H}" in A: 
	expandedTerms = removeExcitations.removeExcitations(expandedTerms)

#latexPrinting ( expandedTerms, "Step 4" ) 

if "\hat{V}" in A[0] : 
	#print "call to apply deltas!"
	expandedTerms = applydeltas.applyDeltas (expandedTerms)


#latexPrinting ( expandedTerms, "Step 4-5" ) 
# Sum all terms in the propagator matrix element
expandedTerms = sumTerms.sumTerms(expandedTerms)

latexPrinting ( expandedTerms, "Step 5" ) 


#if "\hat{V}" in A[0] : 
#	#print "call to apply deltas!"
#	expandedTerms = checkDeltas.checkDeltas (expandedTerms,	wX, yZ)


#basicPrinting ( expandedTerms, "5" ) 
latexPrinting ( expandedTerms, "Step 6" ) 



## =====================
## END PROGRAM
## ====================
