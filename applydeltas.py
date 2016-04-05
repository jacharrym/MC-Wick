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


## Return the sign "1" for "+" and "-1" for "-"
def valueOfSign (sign) :
	if sign == "+":
		return 1.0
	elif sign == "-":
		return -1.0

def symbolOfSign (sign) :
	if sign == 1.0:
		return "+"
	elif sign == -1.0:
		return "-"
def setIndex ( integral, vector, sign, exchange ) :

	dummyIndexA = ("p","q","r","s")	
	dummyIndexB = ("P","Q","R","S")	

	auxindexvector = list()
	auxvector = list()
	for operator in vector:
		if "delta" in operator :
			auxindexvector.append( index(operator) )
			auxvector.append( "delta" )
		else :
			auxindexvector.append( index(operator) )
			auxvector.append( dagger(operator) )

	shift = 0
	i = 0

	for indexi in dummyIndexA:
		#print indexi, integral
		matching = [s for s in integral if indexi in s]
		if matching :
			#print integral
	
			for u in range(0,len(integral)) :
				integral[u] = integral[u].replace(dummyIndexA[i],dummyIndexA[i-shift])
			#print integral
			auxindexvector = [operator.replace(dummyIndexA[i], dummyIndexA[i-shift]) for operator in auxindexvector]

		else :
			shift = shift + 1
		i = i + 1

	shift = 0
	i = 0

	for indexi in dummyIndexB:
		#print indexi, integral
		matching = [s for s in integral if indexi in s]
		if matching :
			#print integral
	
			for u in range(0,len(integral)) :
				integral[u] = integral[u].replace(dummyIndexB[i],dummyIndexB[i-shift])
			#print integral
			auxindexvector = [operator.replace(dummyIndexB[i], dummyIndexB[i-shift]) for operator in auxindexvector]

		else :
			shift = shift + 1
		i = i + 1


	for m in range(0,len(auxvector)) :
		if auxvector[m] == 1 :
			vector[m] = "b_{"+auxindexvector[m]+"}^{\dagger}"
		if auxvector[m] == 0 :
			vector[m] = "b_{"+auxindexvector[m]+"}"

		if auxvector[m] == "delta" :
			vector[m] = "\delta_{"+auxindexvector[m]+"}"
	if exchange :
		i = integral[0]
		j = integral[1]
		k = integral[2]
		l = integral[3]

		ii = order[lower(i)[0]]	
		jj = order[lower(j)[0]]
		kk = order[lower(k)[0]]
		ll = order[lower(l)[0]]

		# this is valid only if the basis functions are real.
		if ii > jj:
			ij = [j,i]
			sign = -1*sign
		else :
			ij = [i,j]

		#   < ij || kl > =     < ij | kl > - < ij | lk >
		# - < ij || kl > = - ( < ij | kl > - < ij | lk > )
		# - < ij || kl > =   - < ij | kl > + < ij | lk > 
		# - < ij || kl > =     < ij | lk > - < ij | kl >  
		# - < ij || kl > =     < ij || lk > 
		#   < ij || kl > =   - < ij || lk > 

		if kk > ll :
			kl = [l,k]
			sign = -1*sign
		else :
			kl = [k,l]

		integral = ij + ["||"] + kl

	else :
		i = integral[0]
		j = integral[1]
		k = integral[2]
		l = integral[3]

		ii = order[lower(i)[0]]	
		jj = order[lower(j)[0]]
		kk = order[lower(k)[0]]
		ll = order[lower(l)[0]]

		ij = [i,j]
		kl = [k,l]

		integral = ij + ["|"] + kl

	return integral, vector, sign, exchange	

def applyDeltas (vector) :

	includeExchange = False
	auxVector = list()

	dummyIndexesA = ("p","q","r","s")
	dummyIndexesB = ("P","Q","R","S")
	dummyIndexes = dummyIndexesA + dummyIndexesB

	for i in range(0,len(vector)) :
		line1 = copy.deepcopy(vector[i])
		sign1 = line1.sign


		if "||" in line1.scalar :
			integral = line1.scalar
			#integral = integral.split(",")
			del integral[integral.index("||")]
			includeExchange = True
		elif "|" in line1.scalar : ##?

			integral = line1.scalar
			#integral = integral.split(",")
			del integral[integral.index("|")]
			includeExchange = False
		else : 
			integral = line1.scalar

		auxLine1 = line1.chain # Split the deltas
		auxIntegral = integral

		addDelta = list()
		#print i,line1.scalar,auxIntegral,integral
		for j in auxLine1 :	
			if "delta" in j :
				#print "delta", j, indexDelta(j)
				auxindex = indexDelta(j)

				# Just the dummy indexes
				if ( auxindex[0][0] in auxIntegral and auxindex[1][0] in auxIntegral ) : 

					for u in range(0,len(auxIntegral)) :		

						# delta_{pi,qi} => qi -> pi
						if auxindex[1][0] in dummyIndexes and  auxindex[1][0] == auxIntegral[u]:
							auxIntegral[u] = auxIntegral[u].replace( auxindex[1][0], auxindex[0] ) 

						# delta_{pi,qi} => p -> pi, restric the dummy index
						if auxindex[0][0] in dummyIndexes and not auxindex[0] == auxIntegral[u]:

							auxIntegral[u] = auxIntegral[u].replace( auxindex[0][0], auxindex[0] ) 

						# delta_{p,pi} => p -> pi
						if auxindex[0][0] ==  auxindex[1][0] :

							auxIntegral[u] = auxIntegral[u].replace( auxindex[0], auxindex[1] ) 
						#if auxindex[0][0] in dummyIndexes and len(auxindex[0]) > 1:
						#	print "12",auxIntegral[u]
						#	auxIntegral[u] = auxIntegral[u].replace( indexDelta(j)[0][0], indexDelta(j)[0] ) 


				# Any delta_{x,p}
				elif ( indexDelta(j)[1][0] in auxIntegral ) : 
					for u in range(0,len(auxIntegral)) :		

						#print auxIntegral[u]
						if not indexDelta(j)[1][0] == indexDelta(j)[0][0]:

							auxIntegral[u] = auxIntegral[u].replace( indexDelta(j)[1][0], indexDelta(j)[0] ) 
							#print "i",auxIntegral[u]

						# delta_{x,p} => p -> x
						else :
							auxIntegral[u] = auxIntegral[u].replace( indexDelta(j)[1][0], indexDelta(j)[0] ) 
							#print "e",auxIntegral[u]

						#print auxIntegral[u]
				# Any delta_{x,y} 
				else :
					if not indexDelta(j)[0][0] == indexDelta(j)[1][0]:
						addDelta.append ("\delta_{"+indexDelta(j)[0]+","+indexDelta(j)[1]+"}")
						#sign1 = 0
				#print auxIntegral
			else: 
				addDelta.append (j)
				#addDelta = addDelta + j
		auxIntegral, addDelta, sign1, exchange = setIndex(auxIntegral, addDelta, sign1,includeExchange)

		if not sign1 == 0 :
			auxVector.append (operatorchain (sign1, addDelta, auxIntegral) )

	return 	auxVector	

