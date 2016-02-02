#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import signal
from itertools import *
import itertools 
import copy
import sys

## =====================
## Python program to solve the Wick's theorem for a chain of operators in latex format. 
## =====================

## =====================
## User options
## =====================

## V0 = Initial chain of operators
V0 = ["a_{p}^{\dagger}", "a_{q}^{\dagger}","a_{r}","a_{s}" ]  
V0 = ["a_{Q}^{\dagger}", "a_{p}^{\dagger}","a_{r}","a_{S}","a_{t}","a_{u}" ]  
V0 = ["a_{Q}^{\dagger}", "a_{p}^{\dagger}","a_{r}","a_{S}"]  

fermions = True
bosons = False
printZeroValues = False
occupiedIndexes = ("i","j","k","l","m","n","o","p","q","r","s")
virtualIndexes = ("a","b","c","d","e","f","g","h")

#Generate the terms

## =====================
## General Funtions 
## =====================

## Creation operator = 1
## Annhiliation operator = 0
def dagger ( operator ) :
	if "^{\dagger}" in operator: 
		return 1
	else :
		return 0
## Return the subindex of the operator
def index ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")
	return auxindex[initial+1:final]

## Evaluate if the vector is sorted in reverse form
def evaluateOrder ( vector ):
	
	sortedVector = sorted(vector, reverse=True)

	isSorted = True
	for i in range(0, len(vector)) :
		if vector[i] != sortedVector[i] :
			isSorted = False

	return isSorted

## Return the chain of operators in its normal order
def normalOrder ( vector, auxSign ) :
	
	## Build an initial auxiliary vector of 1 and 0
	auxVector = list()
	outputVector = list(vector) #Copy the initial vector
	for i in outputVector :
		auxVector.append(dagger(i))

	## Search which elements are disordered
	while not evaluateOrder(auxVector):
		for j in range(0,len(auxVector)) :
			if auxVector[j] == 0:
				for k in range(j,len(auxVector)):
					if auxVector[k] == 1:
						break
	
				indexToSwap = (j,k)
				break
		## Swap
		outputVector[indexToSwap[0]], outputVector[indexToSwap[1]] = outputVector[indexToSwap[1]], outputVector[indexToSwap[0]] 			

		## Build the new auxiliary vector
		auxVector = list()
		for i in outputVector :
			auxVector.append(dagger(i))

		if fermions == True :
			auxSign = auxSign * -1
		if bosons == True :
			auxSign = auxSign * 1

	return outputVector, auxSign

## Commutator object
class commutator(object):
	def __init__(self,sign,string):
		self.sign = sign
		self.string = string

## Evaluate the contraction pair
def evaluateContraction ( operator1, operator2 ) :
		index1 = index(operator1)
		index2 = index(operator2)

		dagger1 = dagger(operator1)
		dagger2 = dagger(operator2)

		if dagger1 == dagger2 :
			## \contraction{a_i}{a_j} = \contraction{a_i^{\dagger}}{a_j^{\dagger}} = 0
			outputCommutator = commutator (0,"")
		else : 	
			## \contraction{a_i}{a_j^{\dagger}} = \delta_{ij}
			if dagger1 == 0 and dagger2 == 1 :
				outputCommutator = commutator (1,"\delta_{"+index1+index2+"}")
			## \contraction{a_i^{\dagger}}{a_j} = 0
			elif dagger1 == 1 and dagger2 == 0 :
				outputCommutator = commutator (0,"")
		return outputCommutator

## Remove an operator from the vector
def removeOperator ( vector, index ) :
	del vector[index]

## Return the sign "+" or "-" just for printing
def symbolOfSign (sign) :
	if sign == 1:
		return "+"
	elif sign == -1:
		return "-" 
	elif sign == 0:
		return ""

## Convert a list to a string
def longformat ( vector ) :
	string = ""
	for i in vector :
		string = string + i
	string = string[0:]
	return string

def lower(String):
	String = String.lower()
	return String

def transformToFermiSpace ( vector ) :
	auxVector = list()
	for i in range(0,len(vector)) :
		auxIndex = index(vector[i])		
		if lower(auxIndex) in occupiedIndexes :
			if dagger(vector[i]) == 1 :
				auxVector.append ("b_"+"{"+auxIndex+"}")
			elif dagger(vector[i]) == 0 :
				auxVector.append ("b_"+"{"+auxIndex+"}^{\dagger}")
		elif lower(auxIndex) in virtualIndexes :
			if dagger(vector[i]) == 1 :
				auxVector.append ("b_"+"{"+auxIndex+"}^{\dagger}")
			elif dagger(vector[i]) == 0 :
				auxVector.append ("b_"+"{"+auxIndex+"}")

	return auxVector

## =====================
## Wick's theorem
## =====================

print "="*10
print "== Initial"
print "="*10
print "\t",longformat(V0)

print "== Fermi vacuum"
V0 = transformToFermiSpace ( V0 )
print "\t",longformat(V0)


## Please do not set both variables True or false at the same time...
if ( fermions == True and bosons == True ) or ( fermions == False and bosons == False ) :
	sys.exit("Please use fermions or bosons...")

## =====================
## Method 1
## =====================

print "="*10
print "== Method 1, available only for singles and doubles contractions until N=5 "
print "="*10

## Zero 
sign = 1
NV, sign = normalOrder (V0,sign)
print "Zero"
print "\t" +symbolOfSign(sign)+longformat(NV)

## Singles
print "Singles"
for m in range (0,len(V0)):
	for n in range (m+1,len(V0)):
		auxV = list()
		auxV = list(V0)
		auxSign = 1
		auxCommutator = evaluateContraction ( V0[m], V0[n] )

		removeOperator(auxV,m)
		removeOperator(auxV,n-1)

		auxV , auxSign = normalOrder(auxV,auxSign)
		auxSign = auxSign * auxCommutator.sign

		# Rule C of Wick's theorem for fermions:
		#   rearrange the operators (introducing minus signs whenever the order of two fermionic operators is swapped) to ensure the contracted terms are adjacent in the string.
		if fermions == True :
			if (m - n)%2 == 1 : # Odd number -> odd distance between operators -> even number of permutations -> same sign
				auxSign = auxSign
			elif (m - n)%2 == 0 : # even number -> even distance between operators -> odd number of permutations -> opposite sign
				auxSign = -auxSign

		if auxSign == 0:
			value = "\t+0"
		else :
			value = "\t"+ symbolOfSign(auxSign)+auxCommutator.string+longformat(auxV)

		print value
# Doubles
print "Doubles"
for m in range (0,len(V0)):
	for n in range (m+1,len(V0)):

		auxV1 = list()
		auxV1 = list(V0)
		auxSign1 = 1
		auxCommutator1 = evaluateContraction ( V0[m], V0[n] )

		removeOperator(auxV1,m)
		removeOperator(auxV1,n-1)

#		auxV1 , auxSign1 = normalOrder(auxV1,auxSign1)
		auxSign1 = auxSign1 * auxCommutator1.sign

		# Rule C of Wick's theorem for fermions:
		#   rearrange the operators (introducing minus signs whenever the order of two fermionic operators is swapped) to ensure the contracted terms are adjacent in the string.
		if fermions == True :
			if (n - m)%2 == 1 : # Odd number -> odd distance between operators -> even number of permutations -> same sign
				auxSign1 = auxSign1
			elif (n - m)%2 == 0 : # even number -> even distance between operators -> odd number of permutations -> opposite sign
				auxSign1 = -auxSign1

		for o in range (m+1,len(V0)):
			for p in range (o+1,len(V0)):
				if n != o and n != p:

					auxV2 = list()
					auxV2 = list(V0)
					auxSign2 = 1
					auxCommutator2 = evaluateContraction ( V0[o], V0[p] )

					removeOperator(auxV2,o)
					removeOperator(auxV2,p-1)

					auxV3 = list()
					auxV3 = list(V0)

					removeOperator(auxV3,m)
					removeOperator(auxV3,n-1)

					if n < o :
						removeOperator(auxV3,o-2)
					else :
						removeOperator(auxV3,o-1)
					if n < p :
						removeOperator(auxV3,p-3)
					else :
						removeOperator(auxV3,p-2)

#					auxV2 , auxSign2 = normalOrder(auxV2,auxSign2)
					auxSign2 = auxSign2 * auxCommutator2.sign

					# Rule C of Wick's theorem for fermions:
					#   rearrange the operators (introducing minus signs whenever the order of two fermionic operators is swapped) to ensure the contracted terms are adjacent in the string.
					if fermions == True :
						if (p - o)%2 == 1 : # Odd number -> odd distance between operators -> even number of permutations -> same sign
							auxSign2 = auxSign2
						elif (p - o)%2 == 0 : # even number -> even distance between operators -> odd number of permutations -> opposite sign
							auxSign2 = -auxSign2
					
					finalSign = auxSign1 * auxSign2



					if finalSign == 0:
						value = "\t+0"
					else :
						value = "\t"+ symbolOfSign(finalSign)+auxCommutator1.string+auxCommutator2.string + longformat(auxV3)

					print value


## =====================
# Method 2
## =====================
print "="*10
print "== Method 2"
print "="*10

#Variables
matrixOfCombinations = list()
totalCombinations = len(V0)/2

# "Allocating" a list of lists
for i in range(0, totalCombinations+1):
	matrixOfCombinations.append(list())

## 
typeOfCombination = {
0:"Zero",
1:"Singles",
2:"Doubles",
3:"Triples, not tested!",
4:"Quadruples, not tested!",
}

## Chain of operator object
class operatorchain(object):
	def __init__(self,sign,chain):
		self.sign = sign
		self.chain = chain

## Generate all the posible combinations of the Wick's theorem with a recursive method: singles, doubles, triplets...
def generateCombinations ( matrixOfCombinations, ncombination, ntype, vector, outputValue ):

	for m in range (0,len(vector)):
		for n in range (m+1,len(vector)):

			ncombination = ncombination - 1
			ntype = ntype + 1

			outputV = list(vector) 
			sign = 1
			auxSign = 1

			auxCommutator = evaluateContraction ( vector[m], vector[n] )

			removeOperator(outputV,m)
			removeOperator(outputV,n-1)
			
			auxOutputV = list(outputV) ## Not ordered
			sign = sign * auxCommutator.sign

			# Rule C of Wick's theorem for fermions:
			#   rearrange the operators (introducing minus signs whenever the order of two fermionic operators is swapped) to ensure the contracted terms are adjacent in the string.
			if fermions == True :
				if (n - m)%2 == 1 : # Odd number -> odd distance between operators -> even number of permutations -> same sign
					sign = sign
				elif (n - m)%2 == 0 : # even number -> even distance between operators -> odd number of permutations -> opposite sign
					sign = -sign

			auxSign = sign
			outputV, auxSign = normalOrder(outputV,auxSign) ## Ordered, only it is used for the ncombination-1

			if auxSign == 0:
				value = operatorchain (0,"+0")
			else :
				value = operatorchain (auxSign,auxCommutator.string)

			auxvalue = copy.copy(value)
			#print "sign 3", auxvalue.sign
			auxvalue.sign =  outputValue.sign*auxvalue.sign
			#print "sign 4", auxvalue.sign
			sign =  sign*outputValue.sign


			adjointAuxValue = operatorchain (auxvalue.sign,  symbolOfSign(auxvalue.sign) + value.chain + outputValue.chain + longformat(outputV))
			auxvalue.chain =  outputValue.chain + auxvalue.chain
			
			## Check if the chain was already added in the matrix
			if not auxvalue.chain in matrixOfCombinations[ntype] and not adjointAuxValue.chain in matrixOfCombinations[ntype] or "+0" in adjointAuxValue.chain :

				if not "+0" in auxvalue.chain :
					print "ntype", ntype, "sign 5", auxvalue.sign
					matrixOfCombinations[ntype].append( symbolOfSign(auxvalue.sign) + auxvalue.chain + longformat(outputV)) 
				elif "+0" in auxvalue.chain and printZeroValues == True :
					matrixOfCombinations[ntype].append( "+0" )
 
			auxvalue.sign = sign
			
			## Recursion
			if ncombination > 0 :
				matrixOfCombinations, ncombination, ntype, auxOutputV, auxvalue = generateCombinations ( matrixOfCombinations, ncombination, ntype, auxOutputV, auxvalue)

			ncombination = ncombination + 1
			ntype = ntype - 1

	return matrixOfCombinations, ncombination, ntype, outputV, outputValue



## Zero 
sign = 1
NV, sign = normalOrder (V0,sign)
matrixOfCombinations[0].append ( symbolOfSign(sign)+longformat(NV) )

## Generate all the combinations

auxint = 0
matrixOfCombinations, auxint, auxint, outputVector, outputValue = generateCombinations (matrixOfCombinations, totalCombinations, 0, V0, operatorchain (1,""))

## Printing the values
for i in range(0, totalCombinations+1):
	print typeOfCombination[i]
	for j in range(0,len(matrixOfCombinations[i])):
		print "\t",matrixOfCombinations[i][j]

## =====================
## END PROGRAM
## ====================



#print "All"
#
#### itertootls
#
#chain = "ABCDEF"
#singles = []
#singles += combinations(chain,2)
#print singles
##
#allelements = ["CDE","BDE","BCE","BCD","ADE","ACE","ACD","ABE","ABD","ABC"]
#
#mydoubles = list()
#for i in range(0,len(allelements)) :
#	chain = allelements[i]
#	doubles = []
#	doubles += combinations(chain,2)
#	for j in range(0,len(doubles)):
#		auxdoubles1 = singles[i]+doubles[j]
#		auxdoubles2 = doubles[j]+singles[i]
#		if not auxdoubles1 in mydoubles and not auxdoubles2 in mydoubles :
#			mydoubles.append(auxdoubles1)
#print mydoubles

