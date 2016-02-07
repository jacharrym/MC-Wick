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

	index1 = auxindex[1]
	index2 = auxindex[2]

	order1 = order[index1]	
	order2 = order[index2]	

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

listName = sys.argv[1]
listFile = open (listName, "r")
listLines = listFile.readlines()

outputName = listName + ".out"
outputFile = open (outputName, "w")

vanishVector = list()
equalVector = list()

for i in range(0,len(listLines)) :
	line1 = listLines[i]
	sign1 = line1[0]

	line1 = line1[1:] #Remove the sign
	auxLine1 = line1.split("\delt") # Split the deltas
	del auxLine1[0] #Remove the blank space before the first delta

	for j in range(i+1,len(listLines)):

		if (i not in vanishVector and j not in vanishVector) and \
		(i not in equalVector and j not in equalVector): # We do not need to consider the terms that will vanish
			line2 = listLines[j]
			sign2 = line2[0]
			line2 = line2[1:] #Remove the sign
			auxLine2 = line2.split("\delt") # Split the deltas
			del auxLine2[0] #Remove the blank space before the first delta

			auxVector = list() 

			for delta1 in auxLine1 :
			
				index1 = index(delta1)
				for delta2 in auxLine2 :
					index2 = index(delta2)
					if index1 == index2 : 
						equalIndexes = True
						auxVector.append(equalIndexes)
						break
			# If the amount of equalIndexes found it is the same number of kronecker delta with opposite signs, the
			# these terms will vanish
			if len(auxVector) == len(auxLine1) and valueOfSign(sign1) == -valueOfSign(sign2) :	
				## print i,sign1,auxLine1,j,sign2,auxLine2 # These terms will vanish
				# Save the index of those terms
				vanishVector.append(i) 
				vanishVector.append(j) 

			# these terms are equak
			if len(auxVector) == len(auxLine1) and valueOfSign(sign1) == valueOfSign(sign2) :	
				## print i,sign1,auxLine1,j,sign2,auxLine2 # These terms will vanish
				# Save the index of those terms
				equalVector.append(i) 
				equalVector.append(j) 


##print vanishVector


if len (vanishVector) == 0  :
	print "There are no opposite terms"
else :
	for i in range(0,len(listLines)) :

		if i not in vanishVector :
			line1 = listLines[i]
			line1 = line1.replace("\n","")
			print line1
			outputFile.write ( line1 + "\n" )

equalVector = equalVector [0::2]

if len (equalVector) == 0  :
	print "There are no equal terms"
else :
	for i in range(0,len(listLines)) :

		if i in equalVector :
			line1 = listLines[i]
			line1 = line1.replace("\n","")
			sign = line1[0]
			line1 = line1[1:]
			line1 = sign + "2" + line1

			print line1
			outputFile.write ( line1 + "\n" )


listFile.close()
outputFile.close()
