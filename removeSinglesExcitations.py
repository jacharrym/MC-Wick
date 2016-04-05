#!/usr/bin/python

global occupiedIndexes 
global virtualIndexes 
global dummyIndexes 

global occupiedIndexesA
global virtualIndexesA
global dummyIndexesA

global occupiedIndexesB 
global virtualIndexesB 
global dummyIndexesB

occupiedIndexesA = ("i","j","k","l","m","n","o","pi","qi","ri","si")
virtualIndexesA = ("a","b","c","d","e","f","g","h","pa","qa","ra","sa")
dummyIndexesA = ("p","q","r","s")

occupiedIndexesB = ("I","J","K","L","M","N","O","P","Q","R","S")
virtualIndexesB = ("A","B","C","D","E","F","G","H")
dummyIndexesB = ("P","Q","R","S")

def removeSinglesExcitations ( iterm ):

	global occupiedIndexes 
	global virtualIndexes 
	global dummyIndexes 

	removeiterm = False
	auxVector = (list(),list())

	for element in iterm.chain :
		if len ( index(element) ) == 1 :
			if dagger(element ) == 1 :
				if index(element) in (occupiedIndexesA + virtualIndexesA + dummyIndexesA ) :
					auxVector[0].append (element)
				if index(element) in (occupiedIndexesB + virtualIndexesB + dummyIndexesB ) :
					auxVector[1].append (element)

	for i in range(0,len(auxVector)):
		if len(auxVector[i])%2 == 0 and len(auxVector[i]) > 0 :
			index1 = index(auxVector[i][0] )
			index2 = index(auxVector[i][1] )
			if index1 in (occupiedIndexesA + virtualIndexesA + dummyIndexesA ) and \
				index2 in (occupiedIndexesA + virtualIndexesA + dummyIndexesA ) :

				occupiedIndexes = occupiedIndexesA
				virtualIndexes = virtualIndexesA 
				dummyIndexes = dummyIndexesA

			if index1 in (occupiedIndexesB + virtualIndexesB + dummyIndexesB ) and \
				index2 in (occupiedIndexesB + virtualIndexesB + dummyIndexesB ) :

				occupiedIndexes = occupiedIndexesB
				virtualIndexes = virtualIndexesB
				dummyIndexes = dummyIndexesB


			if ( index1 in occupiedIndexes and index2 in virtualIndexes ) or \
			   ( index1 in virtualIndexes and index2 in occupiedIndexes ) : 
				# A product of operators b^{\dagger}_i b^{\dagger}_a corresponds to an excitation operator. 
				# According to Brillouin's theorem given a self-consistent optimized Hartree-Fock wavefunction,
				# the matrix element of the Hamiltonian between the ground state and a single excited
				#determinant is zero. 

				# \langle \Psi_0 | H | \Psi_i^a \rangle = 0
				# \langle \Psi_0 | H b^{\dagger}_i b^{\dagger}_a | \Psi_0 \rangle = 0
				# \langle \Psi_0 | H a_i a^{\dagger}_a | \Psi_0 \rangle = 0
				removeiterm = True
				return removeiterm	
			else :
				removeiterm = False
		else :
			removeiterm = False
	

	return removeiterm

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

## Chain of operator object
class operatorchain(object):
	def __init__(self,sign,chain,scalar):
		self.sign = sign
		self.chain = chain
		self.scalar = scalar


