#!/usr/bin/python
# Module wick

import copy
import removeDeltas

# Global variables
typeOfCombination = {
0:"Zero",
1:"Singles",
2:"Doubles",
3:"Triples, not tested!",
4:"Quadruples, not tested!",
}

global fermions
global bosons
global printZeroValues 
global occupiedIndexes 
global dummyIndexes 
global virtualIndexes 
global occupiedIndexesB 
global virtualIndexesB 

fermions = True
bosons = False
printZeroValues = False
occupiedIndexes = ("i","j","k","l","m","n","o","pi","qi","ri","si")
dummyIndexes = ("p","q","r","s")
#dummyIndexes = ()
virtualIndexes = ("a","b","c","d","e","f","g","h","pa","qa","ra","sa")
occupiedIndexesB = ("I","J","K","L","M","N","O","P","Q","R","S")
virtualIndexesB = ("A","B","C","D","E","F","G","H")


## subOperators
class subOperators(object):
	def __init__(self,sign,string,scalar):
		self.sign = sign
		self.string = string
		self.scalar = scalar

## Convert a list to a string
def longformat ( vector ) :
	string = ""
	for i in vector :
		string = string + i
	string = string[0:]
	return string

def transformToFermiSpace ( vector ) :
	auxVector = list()
	for i in range(0,len(vector)) :
		auxIndex = index(vector[i])		
		if lower(auxIndex) in occupiedIndexes :
			if dagger(vector[i]) == 1 :
				auxVector.append ("b_"+"{"+auxIndex+"}")
			elif dagger(vector[i]) == 0 :
				auxVector.append ("b_"+"{"+auxIndex+"}^{\dagger}")
		elif lower(auxIndex) in virtualIndexes :
			if dagger(vector[i]) == 1 :
				auxVector.append ("b_"+"{"+auxIndex+"}^{\dagger}")
			elif dagger(vector[i]) == 0 :
				auxVector.append ("b_"+"{"+auxIndex+"}")
		elif lower(auxIndex) in dummyIndexes :
			if dagger(vector[i]) == 1 :
				auxVector.append ("b_"+"{"+auxIndex+"}^{\dagger}")
			elif dagger(vector[i]) == 0 :
				auxVector.append ("b_"+"{"+auxIndex+"}")


	return auxVector

## Return the subindex of the operator
def index ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")
	return auxindex[initial+1:final]

def lower(String):
	String = String.lower()
	return String

def upper(String):
	String = String.upper()
	return String

## Creation operator = 1
## Annhiliation operator = 0
def dagger ( operator ) :
	if "^{\dagger}" in operator: 
		return 1
	else :
		return 0

## Return the chain of operators in its normal order
def normalOrder ( vector, auxSign, fixIndex ) :
	
	## Build an initial auxiliary vector of 1 and 0
	auxVector = list()
	outputVector = list(vector) #Copy the initial vector
	for i in outputVector :
		auxVector.append(dagger(i))

	## Search which elements are disordered
	while not evaluateOrder(auxVector, True):
		for j in range(0,len(auxVector)) :
			if auxVector[j] == 0:
				for k in range(j,len(auxVector)):
					if auxVector[k] == 1:
						break
	
				indexToSwap = (j,k)
				break
		## Swap
		outputVector[indexToSwap[0]], outputVector[indexToSwap[1]] = outputVector[indexToSwap[1]], outputVector[indexToSwap[0]] 			

		## Build the new auxiliary vector
		auxVector = list()
		for i in outputVector :
			auxVector.append(dagger(i))

		if fermions == True :
			auxSign = auxSign * -1
		if bosons == True :
			auxSign = auxSign * 1

	if fixIndex :
		# establish the order Cre(occupied,virtual,dummy) annih(occupied,virtual,dummy)
		creationVector = list()
		annihilationVector = list()
		# "allocate a list of lists, occupied, virtul, dummy
		for i in range(0,3):	
			creationVector.append(list())
			annihilationVector.append(list())

		# split the operator product
		for operator in outputVector :
			#print operator
			i = index(operator)
			# creation
			if dagger(operator) == 1 :

				if i in occupiedIndexes :
					ii = occupiedIndexes.index(i)
					creationVector[0].append(ii)

				if i in virtualIndexes :
					ii = virtualIndexes.index(i)
					creationVector[1].append(ii)

				if i in dummyIndexes :
					ii = dummyIndexes.index(i)
					creationVector[2].append(ii)

			if dagger(operator) == 0 :

				if i in occupiedIndexes :
					ii = occupiedIndexes.index(i)
					annihilationVector[0].append(ii)

				if i in virtualIndexes :
					ii = virtualIndexes.index(i)
					annihilationVector[1].append(ii)

				if i in dummyIndexes :
					ii = dummyIndexes.index(i)
					annihilationVector[2].append(ii)

		# swap the indexes
		for i in range(0,3):

			creationVector[i], auxSign = swapVector(creationVector[i],auxSign)
			annihilationVector[i], auxSign = swapVector(annihilationVector[i], auxSign)
		
		# rebuild the output vector
		outputVector = list()
		for i in range(0,3):
			for j in creationVector[i] :
				if i == 0 :
					outputVector.append("b_{"+occupiedIndexes[j]+"}^{\dagger}")
				if i == 1 :
					outputVector.append("b_{"+virtualIndexes[j]+"}^{\dagger}")
				if i == 2 :
					outputVector.append("b_{"+dummyIndexes[j]+"}^{\dagger}")

		for i in range(0,3):
			for j in annihilationVector[i] :
				if i == 0 :
					outputVector.append("b_{"+occupiedIndexes[j]+"}")
				if i == 1 :
					outputVector.append("b_{"+virtualIndexes[j]+"}")
				if i == 2 :
					outputVector.append("b_{"+dummyIndexes[j]+"}")

	return outputVector, auxSign

def swapVector ( vector, auxSign ) :

	auxVector = list()
	outputVector = list(vector) #Copy the initial vector
	for i in outputVector :
		auxVector.append(i)

	while not evaluateOrder (auxVector, False):
		for j in range(0,len(auxVector)) :
			jj = auxVector[j]
			for k in range(j+1,len(auxVector)):
				kk = auxVector[k]
				if jj > kk :
		
					indexToSwap = (j,k)
					break
	
		## Swap
		outputVector[indexToSwap[0]], outputVector[indexToSwap[1]] = outputVector[indexToSwap[1]], outputVector[indexToSwap[0]] 			
		## Build the new auxiliary vector
		auxVector = list()
		for i in outputVector :
			auxVector.append(i)

		if fermions == True :
			auxSign = auxSign * -1
		if bosons == True :
			auxSign = auxSign * 1


	return outputVector, auxSign


## Evaluate if the vector is sorted in reverse form
def evaluateOrder ( vector, reverseMode ):
	
	sortedVector = sorted(vector, reverse=reverseMode)

	isSorted = True
	for i in range(0, len(vector)) :
		if vector[i] != sortedVector[i] :
			isSorted = False

	return isSorted

## Chain of operator object
class operatorchain(object):
	def __init__(self,sign,chain,scalar):
		self.sign = sign
		self.chain = chain
		self.scalar = scalar

## Contraction object
class contraction(object):
	def __init__(self,sign,string):
		self.sign = sign
		self.string = string

## Evaluate the contraction pair
def evaluateContraction ( operator1, operator2 ) :
		index1 = index(operator1)
		index2 = index(operator2)

		dagger1 = dagger(operator1)
		dagger2 = dagger(operator2)
		#print "dagger ", dagger1, dagger2
		if dagger1 == dagger2 :
			## \contraction{a_i}{a_j} = \contraction{a_i^{\dagger}}{a_j^{\dagger}} = 0
			outputContraction = contraction (0,"")
		else : 	
			## \contraction{a_i}{a_j^{\dagger}} = \delta_{ij}
			if dagger1 == 0 and dagger2 == 1 :
				if ( index1 in virtualIndexes and index2 in virtualIndexes ) :

					outputContraction = contraction (1,["\delta_{"+index1+","+index2+"}"])

				elif ( index1 in virtualIndexes and index2 in dummyIndexes ) :
					outputContraction = contraction (1,["\delta_{"+index1+","+index2+"}",\
					"\delta_{"+index2+","+index2+"a"+"}"] )

				elif ( index1 in dummyIndexes and index2 in virtualIndexes ) :

					outputContraction = contraction (1,["\delta_{"+index1+","+index2+"}",\
					"\delta_{"+index1+","+index1+"a"+"}"])

				elif ( index1 in dummyIndexes and index2 in dummyIndexes ):

					outputContraction = contraction (1,["\delta_{"+index1+","+index2+"}",\
					"\delta_{"+index1+","+index1+"a"+"}", "\delta_{"+index2+","+index2+"a"+"}",])

				else :
					outputContraction = contraction (0,[""])

			## \contraction{a_i^{\dagger}}{a_j} = 0
			elif dagger1 == 1 and dagger2 == 0 :
				if ( index1 in occupiedIndexes and index2 in occupiedIndexes ) :

					outputContraction = contraction (1,["\delta_{"+index1+","+index2+"}"])

				elif ( index1 in occupiedIndexes and index2 in dummyIndexes ) :

					outputContraction = contraction (1,["\delta_{"+index1+","+index2+"}",\
					"\delta_{"+index2+","+index2+"i"+"}"] )

				elif ( index1 in dummyIndexes and index2 in occupiedIndexes ) :

					outputContraction = contraction (1,["\delta_{"+index1+","+index2+"}",\
					"\delta_{"+index1+","+index1+"i"+"}"])

				elif ( index1 in dummyIndexes and index2 in dummyIndexes ):

					outputContraction = contraction (1,["\delta_{"+index1+","+index2+"}",\
					"\delta_{"+index1+","+index1+"i"+"}", "\delta_{"+index2+","+index2+"i"+"}",])

				else :
					outputContraction = contraction (0,[""])
		return outputContraction

## Remove an operator from the vector
def removeOperator ( vector, index ) :
	del vector[index]

## Return the subindex of the operator
def checkDoubleIndex ( operator ) :
	auxindex = operator.split("_")[1]
	twoindex = auxindex.split(",")
	#initial = twoindex[0].find("{")
	#final = twoindex[1].find("}")

	index1 = twoindex[0][1]
	index2 = twoindex[1][0]

	if index1.isupper() and index2.isupper() :
		#if index1 in occupiedIndexesB and index2 in occupiedIndexesB :
		#	return True
		#elif index1 in virtualIndexesB and index2 in virtualIndexesB :
		#	return True
		#else :
		#	return False

		return True
	elif index1.islower() and index2.islower() :
		#if index1 in occupiedIndexes and index2 in occupiedIndexes :
		#	return True
		#elif index1 in virtualIndexes and index2 in virtualIndexes :
		#	return True
		#else :
		#	return False
		return True
	else :
		return False

## Generate all the posible combinations of the Wick's theorem with a recursive method: singles, doubles, triplets...
def generateCombinations ( matrixOfCombinations, ncombination, ntype, vector, outputValue ):

	for m in range (0,len(vector)):
		for n in range (m+1,len(vector)):

			ncombination = ncombination - 1
			ntype = ntype + 1
			outputV = list(vector) 
			sign = 1
			auxSign = 1

			auxContraction = evaluateContraction ( vector[m], vector[n] )
			removeOperator(outputV,m)
			removeOperator(outputV,n-1)
			
			auxOutputV = list(outputV) ## Not ordered

			sign = sign * auxContraction.sign

			# Rule C of Wick's theorem for fermions:
			#   rearrange the operators (introducing minus signs whenever the order of two fermionic operators is swapped) to ensure the contracted terms are adjacent in the string.
			if fermions == True :
				if (n - m)%2 == 1 : # Odd number -> odd distance between operators -> even number of permutations -> same sign
					sign = sign
				elif (n - m)%2 == 0 : # even number -> even distance between operators -> odd number of permutations -> opposite sign
					sign = -sign

			auxSign = sign
			fixIndex = False
			outputV, auxSign = normalOrder(outputV,auxSign,fixIndex) ## Ordered, only it is used for the ncombination-1
			if auxSign == 0:
				value = operatorchain (0,["+0"],"")
			else :
				value = operatorchain (auxSign,auxContraction.string,"")

			auxvalue = copy.deepcopy(value)

			auxvalue.sign =  outputValue.sign*auxvalue.sign
			sign =  sign*outputValue.sign

#			adjointAuxValue = operatorchain (auxvalue.sign,  symbolOfSign(auxvalue.sign) + value.chain + outputValue.chain + longformat(outputV))
			#print ". ",ntype,outputValue.chain, auxvalue.chain
			#auxvalue.chain =  outputValue.chain + auxvalue.chain

			if outputValue.chain is not "" :
				for auxdelta in outputValue.chain :
				#auxvalue.chain.append(outputValue.chain[0])
					if "delta" in auxdelta :
						auxvalue.chain.append(auxdelta)
			
			## Check if the chain was already added in the matrix
#			if not auxvalue.chain in matrixOfCombinations[ntype] and not adjointAuxValue.chain in matrixOfCombinations[ntype] or "+0" in adjointAuxValue.chain :

			if not "+0" in auxvalue.chain :
				for element in outputV :
					#print ".e", element
					auxvalue.chain.append( longformat(element) )
					#print "..", auxvalue.chain
				matrixOfCombinations[ntype].append( auxvalue) 
#			elif "+0" in auxvalue.chain and printZeroValues == True :
#				matrixOfCombinations[ntype].append( "+0" )

			auxvalue2 = copy.deepcopy(auxvalue)
			auxvalue2.sign = sign

			## Recursion
			if ncombination > 0 :
				matrixOfCombinations, ncombination, ntype, auxOutputV, auxvalue2 = generateCombinations ( matrixOfCombinations, ncombination, ntype, auxOutputV, auxvalue2)

			ncombination = ncombination + 1
			ntype = ntype - 1

	return matrixOfCombinations, ncombination, ntype, outputV, outputValue



def wick (Vi) :


	##print "== Initial"
	#print "\t",Vi.sign, longformat(Vi.string)

	##print "== Fermi vacuum"
	#Vi.string = transformToFermiSpace ( Vi.string )
	#print "\t",longformat(Vi.string)

	## Zero 
	#sign = Vi.sign
	sign = 1.0 # We will add the right sign later
	scalar = Vi.scalar
	NV, sign = normalOrder (Vi.string,sign, True)

	matrixOfCombinations = list()
	totalCombinations = len(Vi.string)/2

	# "Allocating" a list of lists
	for i in range(0, totalCombinations+1):
		matrixOfCombinations.append( list() )

	# add the zero term to the matrix
	matrixOfCombinations[0].append ( operatorchain ( sign,NV,scalar ) )

	auxint = 0
	matrixOfCombinations, auxint, auxint, outputVector, outputValue = generateCombinations ( \
		matrixOfCombinations, totalCombinations, 0, Vi.string, operatorchain (1,"",""))

	#print "wick"
	#for i in range(0,len(matrixOfCombinations)):
	#	for j in range(0, len(matrixOfCombinations[i])):
	#		print i,j,matrixOfCombinations[i][j].sign, matrixOfCombinations[i][j].chain


	## Save the sign and "scalar"
	for i in range(0, totalCombinations+1):
		for j in range(0,len(matrixOfCombinations[i])):
			matrixOfCombinations[i][j].sign = matrixOfCombinations[i][j].sign * Vi.sign
			#print "sign", matrixOfCombinations[i][j].sign 
			matrixOfCombinations[i][j].scalar = scalar

	## Transform to Fermi Vacuum and apply normar order
	for i in range(0, totalCombinations+1):
		# Select only the non-zero terms after operates over the HF wavefunction in the fermi vacuum
		if len (matrixOfCombinations[i]) > 0 :
			for j in range(0,len(matrixOfCombinations[i])):

				auxdelta = list()
				auxvector = list()

				# transform to Fermi vacuum
				for k in range(0,len(matrixOfCombinations[i][j].chain)):
					if "delta" in matrixOfCombinations[i][j].chain[k]: 
						auxdelta.append(matrixOfCombinations[i][j].chain[k])	
					if not "delta" in matrixOfCombinations[i][j].chain[k]: 
						auxvector.append(matrixOfCombinations[i][j].chain[k])	

				auxsign = 1

				# normal order
				if len(auxvector) > 0 :
					auxvector = transformToFermiSpace ( auxvector )
					auxsign = 1
					auxvector, auxsign = normalOrder (auxvector,auxsign,True)

				matrixOfCombinations[i][j].chain = auxdelta + auxvector
				matrixOfCombinations[i][j].sign = matrixOfCombinations[i][j].sign * auxsign

	## Checking the zero terms. Anhilitation operators to the rigth or kronecker delta with mixed index
	auxMatrixOfCombinations = copy.deepcopy(matrixOfCombinations)

	for i in range(0, totalCombinations+1):
		# Select only the non-zero terms after operates over the HF wavefunction in the fermi vacuum
		if len (matrixOfCombinations[i]) > 0 :
			for j in range(0,len(matrixOfCombinations[i])):

				# Remove all terms with "sign" = 0
				if matrixOfCombinations[i][j].sign == 0  :

					auxMatrixOfCombinations[i][j] = None

				# It will remove all the kronecker deltas between diferent species, and between occupied - virtual index
				for k in range(0,len(matrixOfCombinations[i][j].chain)):
					if "\delta_{" in matrixOfCombinations[i][j].chain[k] and \
					not ( checkDoubleIndex( matrixOfCombinations[i][j].chain[k]) ) :

						auxMatrixOfCombinations[i][j] = None
						break

					# It will remove all terms with an anhiliation operator to the left
					if not "\delta_{" in matrixOfCombinations[i][j].chain[k] :
						if dagger(matrixOfCombinations[i][j].chain[k]) == 0 and \
						index(matrixOfCombinations[i][j].chain[k]) not in dummyIndexes :	

							auxMatrixOfCombinations[i][j] = None
							break



	##print "Remove zero terms"

	# Clean all zero terms for each type of combinations
	for i in range(len(auxMatrixOfCombinations)-1,-1, -1):
		auxMatrixOfCombinations[i] = filter (None,  auxMatrixOfCombinations[i] )
	# Clean all zero combinations 	
	auxMatrixOfCombinations = filter (None,  auxMatrixOfCombinations )

	#print "non zero wick"
	#for i in range(0,len(auxMatrixOfCombinations)):
	#	for j in range(0, len(auxMatrixOfCombinations[i])):
	#		print auxMatrixOfCombinations[i][j].sign, auxMatrixOfCombinations[i][j].chain

	# Sum terms	
	repeated = True
	for i in range(0,len(auxMatrixOfCombinations)):
		auxMatrixOfCombinations[i] = removeDeltas.removeDeltas ( auxMatrixOfCombinations[i], repeated ) 

	#print "Wick, Sum terms"
	#for i in range(0,len(auxMatrixOfCombinations)):
	#	for j in range(0, len(auxMatrixOfCombinations[i])):
	#		print  auxMatrixOfCombinations[i][j].sign, auxMatrixOfCombinations[i][j].chain


	return auxMatrixOfCombinations


################################################

#V0 = subOperators(-0.25, ['a_{i}^{\dagger}', 'a_{j}', 'a_{p}^{\dagger}', 'a_{q}^{\dagger}', 'a_{s}', 'a_{r}'],"")
#V0 = subOperators(0.25, ['a_{i}^{\\dagger}', 'a_{p}^{\\dagger}', 'a_{q}^{\\dagger}', 'a_{s}', 'a_{r}', 'a_{j}'],"")

#V0 = subOperators(-0.25, ['a_{j}', 'a_{p}^{\dagger}', 'a_{q}^{\dagger}', 'a_{s}', 'a_{r}'],"")
#V0 = subOperators(0.25, ['a_{p}^{\dagger}', 'a_{q}^{\dagger}', 'a_{s}', 'a_{r}', 'a_{j}'],"")
#
#V0 = subOperators(1.0, ['a_{j}', 'a_{p}^{\dagger}', 'a_{r}'],"")
#V0 = subOperators(-1.0, ['a_{p}^{\dagger}', 'a_{r}', 'a_{j}'],"")


#wick (V0)
#V0 = subOperators (+1,['a_{a}^{\dagger}', 'a_{m}'],"")
#wick (V0)

#V1 = subOperators (-1,[V0.string[1], V0.string[0], V0.string[3], V0.string[4], V0.string[2]], "" )
#if "{H}" in V1.string[4] :
#	V1.scalar = "E"
#	del V1.string[4]

# call wick



