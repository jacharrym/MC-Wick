#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import solveTerm

global occupiedIndexesAlpha
global virtualIndexesAlpha
global occupiedIndexesBeta
global virtualIndexesBeta

occupiedIndexesAlpha = ("i","j","k","l","m","n","o")
virtualIndexesAlpha  = ("a","b","c","d","e","f","g","h")
occupiedIndexesBeta  = ("I","J","K","L","M","N","O")
virtualIndexesBeta  = ("A","B","C","D","E","F","G","H")


## subOperators
class subOperators(object):
	def __init__(self,sign,string,scalar):
		self.sign = sign
		self.string = string
		self.scalar = scalar

def getIndexForParticleHole ( i, nOcc, nVir ) :

	if i.isupper() : # beta species
		if i == "H" : #hole
			index = occupiedIndexesBeta[nOcc]
			nOcc = nOcc + 1
		if i == "P" : #particle
			index = virtualIndexesBeta[nVir]
			nVir = nVir + 1

	if i.islower() : # alpha species
		if i == "h" : #hole
			index = occupiedIndexesAlpha[nOcc]
			nOcc = nOcc + 1
		if i == "p" : #particle
			index = virtualIndexesAlpha[nVir]
			nVir = nVir + 1

	return index, nOcc, nVir

def checkNumberOfParticles ( vector ) :
	numberOfParticles = 0
	for i in vector:
		if "h" in i:
			numberOfParticles = numberOfParticles - 1
		if "p" in i:
			numberOfParticles = numberOfParticles + 1
	return numberOfParticles
				


#selectedMatrix = "xHx"
#selectedMatrix = "xHxyz"
#selectedMatrix = "xyzHxyz"

#selectedMatrix = "xxHxx"
#selectedMatrix = "xxHwxyz"
selectedMatrix = "wxyzHwxyz"
#selectedMatrix = "xyHxy"

twoParticles = False
oneParticle = False


if selectedMatrix == "xHx":
	nmax = 1
	alphaSpecies = ("h","p")
	betaSpecies = ("h","p") 

	print "One Particle"
	#(a|Ha)
	for i in alphaSpecies: 
		for j in betaSpecies: 
			nOccup = 0
			nVirtual = 0
			print j+"-"+i,
			indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
			indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)

			indexj = "a_{"+indexj+"}^{\dagger}"
			indexi = "a_{"+indexi+"}"
			#superOperator = "\hat{H}"
			superOperator = "\hat{V}"
			#solves ther ji-lk term 
			V0 = subOperators (+1,[[indexj],[superOperator,indexi ]], "" )
			finalTerms = solveTerm.solveTerm (nmax,V0)
	print ""

if selectedMatrix == "xHxyz":

	nmax = 1
	alphaSpecies = ("h","p")
	betaSpecies = ("h","p") 

	# (a|HF) 
	for i in betaSpecies: 
		for j in alphaSpecies: 
			for k in betaSpecies: 
				for l in alphaSpecies: 
					if abs(checkNumberOfParticles( [j,l,k] ))==1 and \
					abs(checkNumberOfParticles( [i] ))==1 :
						nOccup = 0
						nVirtual = 0
						indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
						indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
						indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)
						indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)


						indexi = "a_{"+indexi+"}^{\dagger}"
						indexj = "a_{"+indexj+"}"
						indexl = "a_{"+indexl+"}^{\dagger}"
						indexk = "a_{"+indexk+"}"


						#print indexj, "-", indexl, indexi, indexk
						#print l+"^{\dagger}"+ i+k
						print i+"-"+l+j+k

						#solves ther ji-lk term 
						superOperator = "\hat{V}"
						#superOperator = "\hat{H}"

						print "("+indexi+"|"+superOperator+indexl+indexj+indexk+")"

						# (a | X f)		
						V0 = subOperators (+1,[[indexi],[superOperator,\
							indexl,indexj,indexk] ], "" )
						# (f | X a)		
						#V0 = subOperators (+1,[[indexl, indexi, indexk],\
						#	[superOperator, indexj ]], "" )

						finalTerms = solveTerm.solveTerm (nmax,V0)

if selectedMatrix == "xyzHxyz":

	nmax = 1
	alphaSpecies = ("h","p")
	betaSpecies = ("h","p") 

	# (a|HF) 
	for i in betaSpecies: 
		for j in alphaSpecies: 
			for k in betaSpecies: 
				for l in alphaSpecies: 
					for m in betaSpecies: 
						for n in alphaSpecies: 

							if abs(checkNumberOfParticles( [i,j,k] ))==1 and \
							abs(checkNumberOfParticles( [l,m,n] ))==1 :
								nOccup = 0
								nVirtual = 0
								indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
								indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
								indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
								indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)
								indexm, nOccup, nVirtual = getIndexForParticleHole(m,nOccup,nVirtual)
								indexn, nOccup, nVirtual = getIndexForParticleHole(n,nOccup,nVirtual)


								indexi = "a_{"+indexi+"}"
								indexj = "a_{"+indexj+"}^{\dagger}"
								indexk = "a_{"+indexk+"}^{\dagger}"
								indexl = "a_{"+indexl+"}^{\dagger}"
								indexm = "a_{"+indexm+"}"
								indexn = "a_{"+indexn+"}"

								print "\\bf \hat{H}_{"+i+j+k+"-"+l+m+n+"} &",

								#solves ther ji-lk term 
								#superOperator = "\hat{V}"
								superOperator = "\hat{H}"

								print "("+indexi+indexj+indexk+"|"+superOperator+indexl+indexm+indexn+")"

								V0 = subOperators (+1,[[indexi,indexj,indexk],[superOperator,\
									indexl,indexm,indexn] ], "" )

								finalTerms = solveTerm.solveTerm (nmax,V0)

				#print "\\\\"


if selectedMatrix == "xyHxy":
	nmax = 2
	alphaSpecies = ("h","p")
	betaSpecies = ("H","P") 
	twoParticles = True

#if twoParticles :
if selectedMatrix == "xxHxx":
	nmax = 2
	alphaSpecies = ("h","p")
	betaSpecies = ("h","p") 
	twoParticles = True

	for i in betaSpecies: 
		for j in alphaSpecies: 
			for k in betaSpecies: 
				for l in alphaSpecies: 
					nOccup = 0
					nVirtual = 0
					if abs(checkNumberOfParticles( [i,j] ))==2 and \
						abs(checkNumberOfParticles( [k,l] ))==2 :

						indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
						indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
						indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
						indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)

						indexi = "a_{"+indexi+"}"
						indexj = "a_{"+indexj+"}"
						indexk = "a_{"+indexk+"}"
						indexl = "a_{"+indexl+"}"

						superOperator = "\hat{H}"
						#superOperator = "\hat{V}"

						print "\\bf \hat{H}_{"+i+j+"-"+k,l+"} &",
						print "("+indexi+indexj+"|"+superOperator+indexk+indexl+")"

						#solves the term
						V0 = subOperators (+1,[[indexi,indexj],[superOperator,indexk,indexl ]], "" )
						finalTerms = solveTerm.solveTerm (nmax,V0)

#			print ""

#if twoParticles :
if selectedMatrix == "xxHwxyz":
	nmax = 2
	alphaSpecies = ("h","p")
	betaSpecies = ("h","p") 
	twoParticles = True

	for i in betaSpecies: 
		for j in alphaSpecies: 
			for k in betaSpecies: 
				for l in alphaSpecies: 
					for m in betaSpecies: 
						for n in alphaSpecies: 
							if abs(checkNumberOfParticles( [i,j] ))==2 and \
								abs(checkNumberOfParticles( [k,l,m,n] ))==2 :


								nOccup = 0
								nVirtual = 0
								#print j+i+"-"+l+k,

								indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
								indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
								indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
								indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)
								indexm, nOccup, nVirtual = getIndexForParticleHole(m,nOccup,nVirtual)
								indexn, nOccup, nVirtual = getIndexForParticleHole(n,nOccup,nVirtual)


								indexi = "a_{"+indexi+"}"
								indexj = "a_{"+indexj+"}"
								indexk = "a_{"+indexk+"}^{\dagger}"
								indexl = "a_{"+indexl+"}"
								indexm = "a_{"+indexm+"}"
								indexn = "a_{"+indexn+"}"


								#superOperator = "\hat{H}"
								superOperator = "\hat{V}"


								#print k+l+m+n+","
								print "\\bf \hat{V}_{"+i+j+"-"+k+l+m+n+"} &",
								print "("+indexi+indexj+"|"+superOperator+indexk+indexl+\
								indexm+indexn+")",

								#solves the term
								V0 = subOperators (+1,[[indexi,indexj], \
									[superOperator,indexk,indexl,indexm,indexn ]], "" )
								finalTerms = solveTerm.solveTerm (nmax,V0)

			print ""

if selectedMatrix == "wxyzHwxyz":

	nmax = 2
	alphaSpecies = ("h","p")
	betaSpecies = ("h","p") 

	# (a|HF) 
	for i in betaSpecies: 
		for j in alphaSpecies: 
			for k in betaSpecies: 
				for l in alphaSpecies: 
					for m in betaSpecies: 
						for n in alphaSpecies: 
							for o in betaSpecies: 
								for p in alphaSpecies: 

									if abs(checkNumberOfParticles( [i,j,k,l] ))==2 and \
									abs(checkNumberOfParticles( [m,n,o,p] ))==2 :
										nOccup = 0
										nVirtual = 0
										indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
										indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
										indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
										indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)
										indexm, nOccup, nVirtual = getIndexForParticleHole(m,nOccup,nVirtual)
										indexn, nOccup, nVirtual = getIndexForParticleHole(n,nOccup,nVirtual)
										indexo, nOccup, nVirtual = getIndexForParticleHole(o,nOccup,nVirtual)
										indexp, nOccup, nVirtual = getIndexForParticleHole(p,nOccup,nVirtual)


										indexi = "a_{"+indexi+"}^{\dagger}"
										indexj = "a_{"+indexj+"}"
										indexk = "a_{"+indexk+"}"
										indexl = "a_{"+indexl+"}"
										indexm = "a_{"+indexm+"}^{\dagger}"
										indexn = "a_{"+indexn+"}"
										indexo = "a_{"+indexo+"}"
										indexp = "a_{"+indexp+"}"


										print "\\bf \hat{H}_{"+i+j+k+l+"-"+m+n+o+p+"} &",

										#solves ther ji-lk term 
										#superOperator = "\hat{H}"
										superOperator = "\hat{V}"


										print "("+indexi+indexj+indexk+indexl+"|"+superOperator+indexm+indexn+indexo+indexp+")"

										V0 = subOperators (+1,[[indexi,indexj,indexk,indexl],[superOperator,\
											indexm,indexn,indexo,indexp] ], "" )

										finalTerms = solveTerm.solveTerm (nmax,V0)

				#print "\\\\"




# two electrons
#for i in betaSpecies: 
#	for j in alphaSpecies: 
#		for k in betaSpecies: 
#			for l in alphaSpecies: 
#				for m in alphaSpecies: 
#					for n in alphaSpecies: 
#
#						if abs(checkNumberOfParticles( [l,k,m,n] ))==2 and \
#						abs(checkNumberOfParticles( [j,i] ))==2 :
#							print j+i+"-"+l+k+m+n
#							nOccup = 0
#							nVirtual = 0
#							indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
#							indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
#							indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)
#							indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
#							indexm, nOccup, nVirtual = getIndexForParticleHole(m,nOccup,nVirtual)
#							indexn, nOccup, nVirtual = getIndexForParticleHole(n,nOccup,nVirtual)
#							print indexj, indexi, "-",indexl, indexk,indexm,indexn
#
#
#							indexj = "a_{"+indexj+"}^{\dagger}"
#							indexi = "a_{"+indexi+"}^{\dagger}"
#							indexl = "a_{"+indexl+"}"
#							indexk = "a_{"+indexk+"}"
#							indexm = "a_{"+indexm+"}"
#							indexn = "a_{"+indexn+"}"
#							superOperator = "\hat{H}"
#
#							#solves ther ji-lk term 
#							superOperator = "\hat{V}"
#							#superOperator = "\hat{H}"
#							#solves ther ji-lk term 
#							V0 = subOperators (+1,[indexj,indexi,superOperator,\
#								indexl,indexk,indexm,indexn ], "" )
#							finalTerms = solveTerm.solveTerm (nmax,V0)



