import copy
import sys

## General Funtions 
## =====================

## Return the sign "1" for "+" and "-1" for "-"
def valueOfSign (sign) :
	if sign >= 1 :
		return 1
	elif sign <= -1:
		return -1


def sumTerms ( vectorOfCombinations ) :

	#print "initial vector"
	#for i in range(0,len(vectorOfCombinations)):
	#	print  vectorOfCombinations[i].sign, vectorOfCombinations[i].scalar,vectorOfCombinations[i].chain

	vanishVector = dict()
	equalVector = dict()

	for i in range(0,len(vectorOfCombinations)) :
		line1 = vectorOfCombinations[i].chain
		scalar1 = vectorOfCombinations[i].scalar
		sign1 = vectorOfCombinations[i].sign

		for j in range(i+1,len(vectorOfCombinations)):

			if (i not in vanishVector and j not in vanishVector) and \
			(i not in equalVector and j not in equalVector): # We do not need to consider the terms that will vanish

				line2 = vectorOfCombinations[j].chain
				scalar2 = vectorOfCombinations[j].scalar
				sign2 = vectorOfCombinations[j].sign

				auxVector = list() 

				if scalar1 == scalar2 and line1 == line2 and valueOfSign(sign1) == -valueOfSign(sign2) :	
					# Save the index of those terms
					vanishVector[i] = j #vanishVector.append(i) 
					vanishVector[j] = i #vanishVector.append(j) 

				# these terms are equal
				if scalar1 == scalar2 and line1 == line2 and valueOfSign(sign1) == valueOfSign(sign2) :	
					# Save the index of those terms
					equalVector[i] = j	#equalVector.append(i) 
					equalVector[j] = i	#equalVector.append(j) 


	auxVectorOfCombinations = list()
	if len (equalVector) == 0 and len(vanishVector) == 0  :
		#print "There are no equal terms"
		# Nothing to do, just return the original vector
		auxVectorOfCombinations = vectorOfCombinations
	else :
		for i in range(0,len(vectorOfCombinations)) :
			if i in equalVector and equalVector[i] >= 0 :
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
		auxVectorOfCombinations = sumTerms ( auxVectorOfCombinations ) 

	return auxVectorOfCombinations

	#listFile.close()
	#outputFile.close()
