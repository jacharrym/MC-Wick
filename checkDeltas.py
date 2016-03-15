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

def lower(String):
	String = String.lower()
	return String


## Return the subindex of the operator
def index ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")
	return auxindex[initial+1:final]

def indexDelta ( delta ) :

	auxindex = delta.split("_")[1]
	twoindex = auxindex.split(",")
	#initial = auxindex.find("{")
	#final = auxindex.find("}")

	index1 = twoindex[0].replace("{","")
	index2 = twoindex[1].replace("}","")
	order1 = order[lower(index1[0][0])]	
	order2 = order[lower(index2[0][0])]	

	output = list()
	if order1 > order2:
		output = (index2,index1)
	else :
		output = (index1,index2)
	return output


def checkDeltas (vector, listA, listB ) :

	auxVector = list()

	indexListA = list()
	indexListB = list()

	for o in listA :
		auxindex = index(o)
		indexListA.append(auxindex)	
	for o in listB :
		auxindex = index(o)
		indexListB.append(auxindex)	

	for i in range(0,len(vector)) :
		line1 = vector[i]
		sign1 = line1.sign
		scalar = line1.scalar
		auxline1 = line1.chain # Split the deltas

		newLine = list()

		for element in auxline1 :

			if "delta" in element:	
				auxindex = indexDelta(element)
				# i < j < k < l... we can not create/annihilate a particle in the same orbital
				# if it was previously excited, or viceversa
				if auxindex[0][0] in indexListA and auxindex[1][0] in indexListA:		
					newLine.append (0)
				if auxindex[0][0] in indexListB and auxindex[1][0] in indexListB:		
					newLine.append (0)
				else :
				# then just keep the deltas
					newLine.append (element)
			# then just keep the operators
			else :
				newLine.append (element)

		if not 0 in newLine:
			auxVector.append (operatorchain (sign1, newLine, scalar) )

	return 	auxVector	

