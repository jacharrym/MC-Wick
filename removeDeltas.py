import copy
import sys

## General Funtions 
## =====================

## Return the subindex of the operator
def lower(String):
	String = String.lower()
	return String

def index ( operator ) :

	auxindex = operator.split("_")

	#initial = auxindex.find("{")
	#final = auxindex.find("}")

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

	if "delta" in auxindex[0] :

		index1 = auxindex[1][1]
		index2 = auxindex[1][2]
		order1 = order[lower(index1)]
		order2 = order[lower(index2)]

		if order1 > order2:
			output = index2+index1
		else :
			output = index1+index2

	else :

		output = auxindex[1][1]

	return output

## Return the sign "1" for "+" and "-1" for "-"
def valueOfSign (sign) :
	if sign >= 1 :
		return 1
	elif sign <= -1:
		return -1

def removeDeltas ( vectorOfCombinations, repeated ) :

	#print "initial vector"
	#for i in range(0,len(vectorOfCombinations)):
	#	print  vectorOfCombinations[i].sign, vectorOfCombinations[i].chain

	vanishVector = dict()
	equalVector = dict()

	for i in range(0,len(vectorOfCombinations)) :
		line1 = vectorOfCombinations[i].chain
		#print "l1", line1
		sign1 = vectorOfCombinations[i].sign
		for j in range(i+1,len(vectorOfCombinations)):
			if (i not in vanishVector and j not in vanishVector) and \
			(i not in equalVector and j not in equalVector): # We do not need to consider the terms that will vanish
				line2 = vectorOfCombinations[j].chain

				sign2 = vectorOfCombinations[j].sign

				#print "l2", line2
				auxVector = list() 

				for delta1 in line1 :
					index1 = index(delta1)
					for delta2 in line2 :
						index2 = index(delta2)
						#print index1, index2
						if index1 == index2 : 
							equalIndexes = True
							auxVector.append(equalIndexes)
							break
				# If the amount of equalIndexes found it is the same number of kronecker delta with opposite signs, the
				# these terms will vanish
				if len(auxVector) == len(line1) and valueOfSign(sign1) == -valueOfSign(sign2) :	
					## print i,sign1,auxLine1,j,sign2,auxLine2 # These terms will vanish
					# Save the index of those terms
					vanishVector[i] = j #vanishVector.append(i) 
					vanishVector[j] = i #vanishVector.append(j) 

				# these terms are equal
				if len(auxVector) == len(line1) and valueOfSign(sign1) == valueOfSign(sign2) :	
					## print i,sign1,auxLine1,j,sign2,auxLine2 # These terms will vanish
					# Save the index of those terms
					equalVector[i] = j	#equalVector.append(i) 
					equalVector[j] = i	#equalVector.append(j) 


#	print "equalvector", equalVector
#	print "vanishvector", vanishVector

	auxVectorOfCombinations = list()
	if len (equalVector) == 0 and len(vanishVector) == 0  :
		#print "There are no equal terms"
		# Nothing to do, just return the original vector
		auxVectorOfCombinations = vectorOfCombinations
	else :
		for i in range(0,len(vectorOfCombinations)) :
			if i in equalVector and equalVector[i] >= 0 :
				
				## Here we want to remove repeated terms	
				if repeated :
					vectorOfCombinations[i].sign= vectorOfCombinations[i].sign 
				## Here we want to sum terms
				else:
					vectorOfCombinations[i].sign= vectorOfCombinations[i].sign + \
					vectorOfCombinations[equalVector[i]].sign 
				#print vectorOfCombinations[i].sign, vectorOfCombinations[i].chain
				# copy the objet 
				auxObject = copy.deepcopy (vectorOfCombinations[i])
				auxVectorOfCombinations.append(auxObject)
				equalVector[equalVector[i]] = -1

			if i in vanishVector and vanishVector[i] >= 0 :
				vectorOfCombinations[i].sign= vectorOfCombinations[i].sign + \
					vectorOfCombinations[vanishVector[i]].sign 
				#print vectorOfCombinations[i].sign, vectorOfCombinations[i].chain
				# copy the objet, if it is nonzero
				if vectorOfCombinations[i].sign != 0 :
					auxObject = copy.deepcopy (vectorOfCombinations[i])
					auxVectorOfCombinations.append(auxObject)
				vanishVector[vanishVector[i]] = -1

			elif i not in equalVector and i not in vanishVector :
				#print vectorOfCombinations[i].sign, vectorOfCombinations[i].chain
				# copy the objet 
				auxObject = copy.deepcopy (vectorOfCombinations[i])
				auxVectorOfCombinations.append(auxObject)

	#print "aux vector"
	#for i in range(0,len(auxVectorOfCombinations)) :
	#	print auxVectorOfCombinations[i].sign, auxVectorOfCombinations[i].chain

	if len(equalVector) > 0 or len(vanishVector) > 0  :
		auxVectorOfCombinations = removeDeltas ( auxVectorOfCombinations, repeated  ) 

	return auxVectorOfCombinations

	#listFile.close()
	#outputFile.close()
