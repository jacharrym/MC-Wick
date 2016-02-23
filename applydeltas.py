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

def indexDelta ( delta ) :
	auxindex = delta.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")

	index1 = auxindex[1]
	index2 = auxindex[2]
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
def setIndex ( integral, sign, exchange ) :

	dummyIndex = ("p","q","r","s")	

	shift = 0
	i = 0
	for index in dummyIndex:
		if index in integral:
			print integral
			integral = integral.replace(dummyIndex[i],dummyIndex[i-shift])
			print integral
		else :
			shift = shift + 1
		i = i + 1

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
		print integral
	return integral, sign, exchange	

def applyDeltas (vector) :

	#listName = sys.argv[1]
	#listFile = open (listName, "r")
	#listLines = listFile.readlines()

	#outputName = listName + ".out"
	#outputFile = open (outputName, "w")

	includeExchange = False
	auxVector = list()

	#setIndex("pq","rs")

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
					addDelta.append ("\delta_{"+indexDelta(j)+"}")
			else: 
				addDelta.append (j)
				#addDelta = addDelta + j
		print sign1, auxIntegral,addDelta

		auxIntegral, sign1, exchange = setIndex(auxIntegral,sign1,includeExchange)
		print sign1, auxIntegral

		auxVector.append (operatorchain (sign1, addDelta, auxIntegral) )

	return 	auxVector	

