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

fermions = True
bosons = False
printZeroValues = False
occupiedIndexes = ("i","j","k","l","m","n","o","p","q","r","s","t","u")
virtualIndexes = ("a","b","c","d","e","f","g","h")

#Generate the terms

## subOperators
class subOperators(object):
	def __init__(self,sign,string,scalar):
		self.sign = sign
		self.string = string
		self.scalar = scalar



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

def searchSuperOperator ( superOperator ) :
	if "\hat" in superOperator: 
		return True
	else :
		return False

## Return the subindex of the operator
def index ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")
	return auxindex[initial+1:final]

## Return the subindex of the operator
def checkDoubleIndex ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")

	index1 = auxindex[initial+1]
	index2 = auxindex[final-1]

	if index1.isupper() and index2.isupper() :
		return True
	elif  index1.islower() and index2.islower() :
		return True
	else :
		return False

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

def upper(String):
	String = String.upper()
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

V0 = subOperators (+1,["a_{p}^{\dagger}", "a_{Q}^{\dagger}","\hat{H}","a_{r}","a_{S}" ], "" )
# wX \hat{A} yZ
# = [X^\dagger w^\dagger , \hat{A} y Z ]_+
# = X^\dagger w^\dagger \hat{A} y Z + \hat{A} y Z  X^\dagger w^\dagger
# = X^\dagger w^\dagger y Z A (1) - X^\dagger w^\dagger A y Z (2)  + 
# y Z A  X^\dagger w^\dagger (3) - A y Z  X^\dagger w^\dagger (4)

V1 = subOperators (+1,[V0.string[1], V0.string[0], V0.string[3], V0.string[4], V0.string[2]], "" )
if "{H}" in V1.string[4] :
	V1.scalar = "E"
	del V1.string[4]
V2 = subOperators (-1,[V0.string[1], V0.string[0], V0.string[2], V0.string[3], V0.string[4]], "" )
if "{H}" in V2.string[2] :
	V2.scalar = "E" + "-\epsilon_{" + index(V2.string[3]) + "}" + "-\epsilon_{" + index(V2.string[4])
	del V2.string[2]
V3 = subOperators (+1,[V0.string[3], V0.string[4], V0.string[2], V0.string[1], V0.string[0]], "" )
if "{H}" in V3.string[2] :
	V3.scalar = "E" + "+\epsilon_{" + index(V3.string[0]) + "}" + "+\epsilon_{" + index(V3.string[1])
	del V3.string[2]
V4 = subOperators (-1,[V0.string[2], V0.string[3], V0.string[4], V0.string[1], V0.string[0]], "" )
if "{H}" in V4.string[0] :
	V4.scalar = "E"
	del V4.string[0]

allV = [V1,V2,V3,V4]
#V1.string.append("a_{t}")
#V1.string.append("a_{u}")
allV = [V1]
	

## Please do not set both variables True or false at the same time...
if ( fermions == True and bosons == True ) or ( fermions == False and bosons == False ) :
	sys.exit("Please use fermions or bosons...")

## =====================
# Method 2
## =====================
print "="*10
print "== Method 2"
print "="*10

#Variables

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
				value = operatorchain (0,["+0"])
			else :
				value = operatorchain (auxSign,[auxCommutator.string])

			auxvalue = copy.copy(value)

			auxvalue.sign =  outputValue.sign*auxvalue.sign
			sign =  sign*outputValue.sign

#			adjointAuxValue = operatorchain (auxvalue.sign,  symbolOfSign(auxvalue.sign) + value.chain + outputValue.chain + longformat(outputV))
			##auxvalue.chain =  outputValue.chain + auxvalue.chain

			if outputValue.chain is not "" :
				auxvalue.chain.append(outputValue.chain[0])
			
			## Check if the chain was already added in the matrix
#			if not auxvalue.chain in matrixOfCombinations[ntype] and not adjointAuxValue.chain in matrixOfCombinations[ntype] or "+0" in adjointAuxValue.chain :

			if not "+0" in auxvalue.chain :
				for element in outputV :
					auxvalue.chain.append( longformat(element) )
				matrixOfCombinations[ntype].append( auxvalue) 
#			elif "+0" in auxvalue.chain and printZeroValues == True :
#				matrixOfCombinations[ntype].append( "+0" )

			auxvalue2 = copy.copy(auxvalue)
			auxvalue2.sign = sign

			## Recursion
			if ncombination > 0 :
				matrixOfCombinations, ncombination, ntype, auxOutputV, auxvalue2 = generateCombinations ( matrixOfCombinations, ncombination, ntype, auxOutputV, auxvalue2)

			ncombination = ncombination + 1
			ntype = ntype - 1

	return matrixOfCombinations, ncombination, ntype, outputV, outputValue


## Generate all the combinations

for Vi in allV :

	print "="*10
	print "== Initial"
	print "="*10
	print "\t",longformat(Vi.string)

	print "== Fermi vacuum"
	Vi.string = transformToFermiSpace ( Vi.string )
	print "\t",longformat(Vi.string)

	## Zero 
	sign = 1
	NV, sign = normalOrder (Vi.string,sign)

	matrixOfCombinations = list()
	totalCombinations = len(Vi.string)/2

	# "Allocating" a list of lists
	for i in range(0, totalCombinations+1):
		matrixOfCombinations.append( list() )

	matrixOfCombinations[0].append ( operatorchain ( sign,longformat(NV) ) )

	auxint = 0
	matrixOfCombinations, auxint, auxint, outputVector, outputValue = generateCombinations ( \
		matrixOfCombinations, totalCombinations, 0, Vi.string, operatorchain (1,""))

	## Checking the zero terms
	auxMatrixOfCombinations = copy.deepcopy(matrixOfCombinations)
	for i in range(0, totalCombinations+1):
		# Select only the non-zero terms after operates over the HF wavefunction in the fermi vacuum
		if len (matrixOfCombinations[i]) > 0 :
			print typeOfCombination[i]
## 		Here we need to check the doubles indexes (iJ) 
			for j in range(0,len(matrixOfCombinations[i])):
				print "\t",matrixOfCombinations[i][j].sign, matrixOfCombinations[i][j].chain
				# It will remove all terms with an anhiliation operator to the left
				if dagger(matrixOfCombinations[i][j].chain[-1]) == 0 and \
				"\delta_{" not in (matrixOfCombinations[i][j].chain[-1]) : 
					auxMatrixOfCombinations[i][j] = None
				# It will remove all the dirac deltas between diferent species
				for k in range(0,len(matrixOfCombinations[i][j].chain)):
					if "\delta_{" in matrixOfCombinations[i][j].chain[k] and \
					not ( checkDoubleIndex( matrixOfCombinations[i][j].chain[k]) ) :
						auxMatrixOfCombinations[i][j] = None
						break

	# Clean all zero terms for each type of combinations
	for i in range(len(auxMatrixOfCombinations)-1,-1, -1):
		auxMatrixOfCombinations[i] = filter (None,  auxMatrixOfCombinations[i] )
	# Clean all zero combinations 	
	auxMatrixOfCombinations = filter (None,  auxMatrixOfCombinations )

	for i in range(0,len(auxMatrixOfCombinations)):
		for j in range(0, len(auxMatrixOfCombinations[i])):
			print auxMatrixOfCombinations[i][j].chain

#	print auxMatrixOfCombinations[1][0].chain

	del matrixOfCombinations 

## =====================
## END PROGRAM
## ====================
