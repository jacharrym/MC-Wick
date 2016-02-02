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

def lower(String):
	String = String.lower()
	return String

def indexDelta ( delta ) :
	
	auxindex = delta.split("_")[1]
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

listName = sys.argv[1]
listFile = open (listName, "r")
listLines = listFile.readlines()

outputName = listName + ".out"
outputFile = open (outputName, "w")

integral = "pqrs"
integral = "pQrS"
includeExchange = False

for i in range(0,len(listLines)) :
	line1 = listLines[i]
	sign1 = valueOfSign(line1[0])

	line1 = line1[1:] #Remove the sign
#	print line1
	auxLine1 = line1.split("\delt") # Split the deltas
#	print auxLine1
	del auxLine1[0] #Remove the blank space before the first delta
	auxIntegral = integral
	addDelta = " "
	for j in auxLine1 :	
		if ( indexDelta(j)[1] in auxIntegral or indexDelta(j)[0] in auxIntegral ) : 
			auxIntegral = auxIntegral.replace( indexDelta(j)[1], indexDelta(j)[0] )
		else :
			addDelta = addDelta + "\delta_{"+indexDelta(j)+"}"
		
	int1 = auxIntegral[0:2]
	int2 = auxIntegral[2:4]
	auxInt1 = indexDelta("_{"+int1+"}")
	auxInt2 = indexDelta("_{"+int2+"}")
		
	if auxInt1 == int1 :
		sign1 = sign1
	else :
		sign1 = -1*sign1
	if auxInt2 == int2 :
		sign1 = sign1
	else :
		sign1 = -1*sign1
			

	print symbolOfSign(sign1)+"\\langle "+auxInt1+"||"+auxInt2+" \\rangle"+addDelta
					

listFile.close()
outputFile.close()
