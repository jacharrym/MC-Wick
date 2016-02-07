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

## General Funtions 
## =====================

def index ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")
	return auxindex[initial+1:final]

def buildDeltaKroneker ( operator1, operator2 ) :
	index1 = index(operator1)
	index2 = index(operator2)
	out = "\delta_{"+index1+index2+"}"
	return out

## Creation operator = 1
## Annhiliation operator = 0
def dagger ( operator ) :
	if "^{\dagger}" in operator: 
		return 1
	else :
		return 0

listName = sys.argv[1]
listFile = open (listName, "r")
listLines = listFile.readlines()

outputName = listName + ".out"
outputFile = open (outputName, "w")

for line in listLines :
	line = line.replace("\delta_",",\delta_")
	line = line.replace("}a_","},a_")
	line = line.replace("+a_","+,a_")
	line = line.replace("-a_","-,a_")
	line = line.replace("\n","")

	auxline = line.split(",")
	sign = auxline[0]
	outputFile.write( sign )
	del auxline[0]
	
	j = len(auxline) - 1
	for i in range(0,len(auxline)):
		isOperator = True
		if "\delta" in auxline[i] :
			outputFile.write( auxline[i] )
			isOperator = False
			j = j + 1
		if "a_" in auxline[i] and isOperator == True :
			if dagger(auxline[i]) == 1 and dagger(auxline[j]) == 0 :
				delta =	buildDeltaKroneker (auxline[i] , auxline[j] )
				outputFile.write (delta	)
		j = j - 1
#			outputFile.write( auxline[i] )
		

	outputFile.write( "\n" )


## Return the subindex of the operator

### Evaluate if the vector is sorted in reverse form
#def evaluateOrder ( vector ):
#	
#	sortedVector = sorted(vector, reverse=True)
#
#	isSorted = True
#	for i in range(0, len(vector)) :
#		if vector[i] != sortedVector[i] :
#			isSorted = False
#
#	return isSorted
#
### Return the chain of operators in its normal order
#def normalOrder ( vector, auxSign ) :
#	
#	## Build an initial auxiliary vector of 1 and 0
#	auxVector = list()
#	outputVector = list(vector)
#	for i in outputVector :
#		auxVector.append(dagger(i))
#
#	## Search which elements are disordered
#	while not evaluateOrder(auxVector):
#		for j in range(0,len(auxVector)) :
#			if auxVector[j] == 0:
#				for k in range(j,len(auxVector)):
#					if auxVector[k] == 1:
#						break
#	
#				indexToSwap = (j,k)
#				break
#		## Swap
#		outputVector[indexToSwap[0]], outputVector[indexToSwap[1]] = outputVector[indexToSwap[1]], outputVector[indexToSwap[0]] 			
#
#		## Build the new auxiliary vector
#		auxVector = list()
#		for i in outputVector :
#			auxVector.append(dagger(i))
#
#		if fermions == True :
#			auxSign = auxSign * -1
#		if bosons == True :
#			auxSign = auxSign * 1
#
#	return outputVector, auxSign


listFile.close()
outputFile.close()
