#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import signal
import copy
import sys
from wick import operatorchain

global order
order = {
"a":1,
"b":2,
"c":3,
"d":4,
"e":5,
"f":6,
"g":7,
"h":8,
"i":9,
"j":10,
"k":11,
"l":12,
"m":13,
"n":14,
"o":15,
"p":16,
"q":17,
"r":18,
"s":19,
}


## General Funtions 
## =====================

def lower(String):
	String = String.lower()
	return String

## Return the subindex of the operator
def index ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")
	return auxindex[initial+1:final]

## Creation operator = 1
## Annhiliation operator = 0
def dagger ( operator ) :
	if "^{\dagger}" in operator: 
		return 1
	else :
		return 0

def indexDelta ( delta ) :
	auxindex = delta.split("_")[1]
	twoindex = auxindex.split(",")
	#initial = auxindex.find("{")
	#final = auxindex.find("}")

	index1 = twoindex[0][1]
	index2 = twoindex[1][0]
	order1 = order[lower(index1)]	
	order2 = order[lower(index2)]	

	if order1 > order2:
		output = index2+index1
	else :
		output = index1+index2
	return output

## Return the sign "1" for "+" and "-1" for "-"
def valueOfSign (sign) :
	if sign == "+":
		return 1
	elif sign == "-":
		return -1

def symbolOfSign (sign) :
	if sign == 1:
		return "+"
	elif sign == -1:
		return "-"
def setIndex ( integral, vector, sign, exchange ) :

	dummyIndex = ("p","q","r","s")	

	auxindexvector = list()
	auxvector = list()
	for operator in vector:
		auxindexvector.append( index(operator) )
		auxvector.append( dagger(operator) )

	shift = 0
	i = 0

	for indexi in dummyIndex:
		if indexi in integral:
			integral = integral.replace(dummyIndex[i],dummyIndex[i-shift])
			auxindexvector = [operator.replace(dummyIndex[i], dummyIndex[i-shift]) for operator in auxindexvector]

		else :
			shift = shift + 1
		i = i + 1

	for m in range(0,len(auxvector)) :
		if auxvector[m] == 1 :
			vector[m] = "b_{"+auxindexvector[m]+"}^{\dagger}"
		if auxvector[m] == 0 :
			vector[m] = "b_{"+auxindexvector[m]+"}"

	if exchange :
		i = integral[0]
		j = integral[1]
		k = integral[2]
		l = integral[3]

		ii = order[lower(i)]	
		jj = order[lower(j)]
		kk = order[lower(k)]
		ll = order[lower(l)]

		if ii > jj:
			ij = j + i
			sign = -1*sign
		else :
			ij = i + j
		if kk > ll :
			kl = l + k
			sign = -1*sign
		else :
			kl = k + l

		integral = ij + "||" + kl
	return integral, vector, sign, exchange	

def applyDeltas (vector) :

	#listName = sys.argv[1]
	#listFile = open (listName, "r")
	#listLines = listFile.readlines()

	#outputName = listName + ".out"
	#outputFile = open (outputName, "w")

	includeExchange = False
	auxVector = list()

	#setIndex("pq","rs")

	print "apply"

	for i in range(0,len(vector)) :
		line1 = vector[i]
		sign1 = line1.sign
		if "||" in line1.scalar :
			integral = line1.scalar[:2] + line1.scalar[4:]
			includeExchange = True
		else :
			integral = line1.scalar[:2] + line1.scalar[3:]
		auxLine1 = line1.chain # Split the deltas
	#	print auxLine1
		auxIntegral = integral

		addDelta = list()
		for j in auxLine1 :	
			if "delta" in j :
				if ( indexDelta(j)[1] in auxIntegral or indexDelta(j)[0] in auxIntegral ) : 
					auxIntegral = auxIntegral.replace( indexDelta(j)[1], indexDelta(j)[0] )
				else :
					addDelta.append ("\delta_{"+indexDelta(j)[0]+","+indexDelta(j)[1]+"}")
			else: 
				addDelta.append (j)
				#addDelta = addDelta + j
		print addDelta

		auxIntegral, addDelta, sign1, exchange = setIndex(auxIntegral, addDelta, sign1,includeExchange)
		#print sign1, auxIntegral

		auxVector.append (operatorchain (sign1, addDelta, auxIntegral) )

	return 	auxVector	

