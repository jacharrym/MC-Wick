#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import signal
import copy
import sys
import wick
from wick import operatorchain
from wick import subOperators 


global occupiedIndexes 
global dummyIndexes 
global virtualIndexes 
global occupiedIndexesB 
global virtualIndexesB 

occupiedIndexes = ("i","j","k","l","m","n","o","pi","qi","ri","si")
dummyIndexes = ("p","q","r","s")
virtualIndexes = ("a","b","c","d","e","f","g","h","pa","qa","ra","sa")
occupiedIndexesB = ("I","J","K","L","M","N","O","P","Q","R","S")
virtualIndexesB = ("A","B","C","D","E","F","G","H")

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
		return 1
	elif sign == "-":
		return -1

def symbolOfSign (sign) :
	if sign == 1:
		return "+"
	elif sign == -1:
		return "-"

def transformToVacuumSpace ( operator ) :
	auxOperator = ""
	auxIndex = index(operator)		
	if lower(auxIndex) in occupiedIndexes :
		if dagger(operator) == 1 :
			auxOperator = "b_"+"{"+auxIndex+"}"
		elif dagger(operator) == 0 :
			auxOperator = "b_"+"{"+auxIndex+"}^{\dagger}"
	elif lower(auxIndex) in virtualIndexes :
		if dagger(operator) == 1 :
			auxOperator = "b_"+"{"+auxIndex+"}^{\dagger}"
		elif dagger(operator) == 0 :
			auxOperator = "b_"+"{"+auxIndex+"}"
	elif lower(auxIndex) in dummyIndexes :
		if dagger(operator) == 1 :
			auxOperator = "b_"+"{"+auxIndex+"}^{\dagger}"
		elif dagger(operator) == 0 :
			auxOperator = "b_"+"{"+auxIndex+"}"

	return auxOperator


def removeExcitations (vector) :

	includeExchange = False
	auxVector = list()
	finalVector = list()

	#print "remove ex"
	

	for i in range(0,len(vector)) :
		auxVector.append( list() )
		#vector[i].chain = ['b_{i}^{\dagger}','b_{p}^{\dagger}', 'b_{q}']

	for i in range(0,len(vector)) :
		line1 = vector[i]
		sign1 = line1.sign

		string1 = line1.chain
		integral1 = line1.scalar
		# other
		auxVector[i].append([0])
		#pqrs
		auxVector[i].append([0])
		auxVector[i].append([0])
		auxVector[i].append([0])
		auxVector[i].append([0])

		for j in string1 :	
			auxindex = index(j) 
			kk = 0 

			if auxindex in dummyIndexes :
				kk = dummyIndexes.index(auxindex) 
				if dagger( j) == 1:
					auxVector[i][kk+1] = ["a_{"+auxindex+"i}^{\dagger}","a_{"+auxindex+"a}^{\dagger}"]
				if dagger( j) == 0:
					auxVector[i][kk+1] = ["a_{"+auxindex+"i}","a_{"+auxindex+"a}"] 
			else :
				if not "delta" in j :
					j =  transformToVacuumSpace ( j ) 
				if auxVector[i][0] == [0] :	
					auxVector[i][0] = [j]
				else :
					auxVector[i][0] = auxVector[i][0] + [j]

		outputVector = list()
		for pp in auxVector[i][1]:	
			for qq in auxVector[i][2]:	
				for rr in auxVector[i][3]:	
					for ss in auxVector[i][4]:	
						newTerm = list()

						oldDeltas = list()

						auxoutputVector = list()
						for ii in auxVector[i][0]:	
							if not ii == 0 and not "delta" in ii :
								newTerm.append(ii)
							if not ii == 0 and "delta" in ii :
								oldDeltas.append(ii)
						if not pp == 0 :
							newTerm.append(pp)
						if not qq == 0 :
							newTerm.append(qq)
						if not rr == 0 :
							newTerm.append(rr)
						if not ss == 0 :
							newTerm.append(ss)

						if len(newTerm) > 0 :	
							V0 = subOperators (+1,newTerm,"")
							auxoutputVector = wick.wick (V0)
							
						# Here we add the previous kronecker deltas 
						if len(oldDeltas) > 0 and len(newTerm) == 0:
							auxoutputVector.append ( [operatorchain (+1,oldDeltas,"") ] )

						if len(auxoutputVector) > 0 :	
							outputVector.append( auxoutputVector )

		for element in outputVector:
			for nCombinations in element:
				for iterm in nCombinations :

					numberOfParticles = 0 
					thereIsOperators = False

					for operator in iterm.chain :
						if not "delta" in operator :
							thereIsOperators = True
							indexOfOperator = index(operator)
							if dagger(operator) == 1:

								if indexOfOperator in occupiedIndexes :
									numberOfParticles = numberOfParticles - 1
								if indexOfOperator in virtualIndexes :
									numberOfParticles = numberOfParticles + 1
							# We are in the fermi vaccum, there isn't annhilitation operators left
							if dagger(operator) == 0:

								print "It should never enter here"

					# Here we add the previous kronecker deltas
					if len(oldDeltas) > 0 and len(newTerm) > 0:
						iterm.chain = oldDeltas + iterm.chain

					# This is an excitation
					if numberOfParticles == 0 and thereIsOperators :
						sign1 = 0
					sign1 = sign1 * iterm.sign

					if not sign1 == 0 :
						finalVector.append (operatorchain (sign1, iterm.chain, integral1) )


		if len(string1) == 0 :	
			finalVector.append (operatorchain (sign1, "", integral1) )
	return 	finalVector	

