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
		if "h" in i.lower() :
			numberOfParticles = numberOfParticles - 1
		if "p" in i.lower() :
			numberOfParticles = numberOfParticles + 1
	return numberOfParticles
				

## one particle one species

#selectedMatrix = "xHx"
selectedMatrix = "xHxyz"
#selectedMatrix = "xyzHxyz"


selectedMatrix = "gamma"

## two particles one species

#selectedMatrix = "xxHxx"
#selectedMatrix = "xxHwxyz"
#selectedMatrix = "wxyzHwxyz"


## one particle two species

#selectedMatrix = "xHXyZ"

## two particles two species

#selectedMatrix = "xXHxX"
selectedMatrix = "xXHwyzZ"
#selectedMatrix = "xXHWYZz"
#selectedMatrix = "xXyYzZHxXyYzZ"

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

			indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
			indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)

			#indexi = "a_{"+indexi+"}^{\dagger}"
			#indexj = "a_{"+indexj+"}^{\dagger}"

			indexi = "a_{"+indexi+"}"
			indexj = "a_{"+indexj+"}"

			superOperator = "\hat{H}"
			superOperator = "\hat{V}^{aa}"
			#solves ther ji-lk term 
			V0 = subOperators (+1,[[indexi],[superOperator,indexj ]], "" )
			finalTerms = solveTerm.solveTerm (nmax,V0)
	print ""

if selectedMatrix == "xHxyz":

	nmax = 1
	alphaSpecies = ("h","p")
	betaSpecies = ("H","P") 

	# (a|HF) 
	for i in alphaSpecies: 
		for j in betaSpecies: 
			for k in betaSpecies: 
				for l in alphaSpecies: 
					if abs(checkNumberOfParticles( [l] ))==1 and \
					abs(checkNumberOfParticles( [i] ))==1 :
						nOccup = 0
						nVirtual = 0
						indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
						indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
						indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
						indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)


						indexi = "a_{"+indexi+"}"
						indexj = "a_{"+indexj+"}^{\dagger}"
						indexk = "a_{"+indexk+"}"
						indexl = "a_{"+indexl+"}"


						if (j+k) == "HP" or (j+k) == "PH" : #only excitations
						#if (j+k) == "hp" or (j+k) == "ph" : #only excitations
							print i+"-"+j+k+l

							#superOperator = "\hat{V}^{aa}"
							superOperator = "\hat{V}^{ab}"
							#superOperator = "\hat{H}"

							print "("+indexi+"|"+superOperator+indexj+indexk+indexl+")"

							# (a | X f)		
							V0 = subOperators (+1,[[indexi],[superOperator,\
								indexj,indexk,indexl] ], "" )

							finalTerms = solveTerm.solveTerm (nmax,V0)

#if twoParticles :
if selectedMatrix == "gamma":
	nmax = 2
	alphaSpecies = ("h","p")
	betaSpecies = ("h","p") 
	twoParticles = True

	for i in alphaSpecies: 
		for j in alphaSpecies: 
			for k in alphaSpecies: 
				for l in alphaSpecies: 
					nOccup = 0
					nVirtual = 0

					indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
					indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
					indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
					indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)

					indexi = "a_{"+indexi+"}^{\dagger}"
					indexj = "a_{"+indexj+"}"
					indexk = "a_{"+indexk+"}^{\dagger}"
					indexl = "a_{"+indexl+"}"

					superOperator = "\hat{H}"
					#superOperator = "\hat{V}^{aa}"


					if ((k+l) == "hp" or (k+l) == "ph") and ((i+j) == "hp" or (i+j) == "ph")  : #only excitations
						print "\\bf \hat{H}_{"+i+j+"-"+k,l+"} &",
						print "("+indexi+indexj+"|"+superOperator+indexk+indexl+")"

						#solves the term
						V0 = subOperators (+1,[[indexi,indexj],[superOperator,indexk,indexl ]], "" )
						finalTerms = solveTerm.solveTerm (nmax,V0)

#			print ""



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


								indexi = "a_{"+indexi+"}^{\dagger}"
								indexj = "a_{"+indexj+"}"
								indexk = "a_{"+indexk+"}"
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

#if twoParticles :
if selectedMatrix == "xxHxx":
	nmax = 2
	alphaSpecies = ("h","p")
	betaSpecies = ("h","p") 
	twoParticles = True

	for i in alphaSpecies: 
		for j in alphaSpecies: 
			for k in alphaSpecies: 
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
						superOperator = "\hat{V}^{aa}"

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
								superOperator = "\hat{V}^{aa}"


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



if selectedMatrix == "xHXyZ":
	nmax = 1
	alphaSpecies = ("h","p")
	betaSpecies = ("H","P") 
	twoParticles = True

	for i in alphaSpecies: 
		for j in betaSpecies: 
			for k in alphaSpecies: 
				for l in betaSpecies: 
					nOccup = 0
					nVirtual = 0
					if abs(checkNumberOfParticles( [i] ))==1 and \
						abs(checkNumberOfParticles( [k] ))==1 :

						indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
						indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
						indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
						indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)

						indexi = "a_{"+indexi+"}"
						indexj = "a_{"+indexj+"}^{\dagger}"
						indexk = "a_{"+indexk+"}"
						indexl = "a_{"+indexl+"}"

						superOperator = "\hat{H}"
						superOperator = "\hat{V}^{aa}"
						superOperator = "\hat{V}^{ab}"

						#if (i+j+k+l) == "hHhP" :
						#if (i+j+k+l) == "pPpH" :

						print "\\bf "+superOperator+"_{"+i+"-"+j+k+l+"} &",
						print "("+indexi+"|"+superOperator+indexj+indexk+indexl+")"

						#solves the term
						V0 = subOperators (+1,[[indexi],[superOperator,indexj,indexk,indexl ]], "" )
						finalTerms = solveTerm.solveTerm (nmax,V0)

#if twoParticles :
if selectedMatrix == "xXHxX":
	nmax = 2
	alphaSpecies = ("h","p")
	betaSpecies = ("H","P") 
	twoParticles = True

	for i in alphaSpecies: 
		for j in betaSpecies: 
			for k in alphaSpecies: 
				for l in betaSpecies: 
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
						#superOperator = "\hat{V}^{aa}"
						#superOperator = "\hat{V}^{ab}"

						print "\\bf \hat{H}_{"+i+j+"-"+k,l+"} &",
						print "("+indexi+indexj+"|"+superOperator+indexk+indexl+")"

						#solves the term
						V0 = subOperators (+1,[[indexi,indexj],[superOperator,indexk,indexl ]], "" )
						finalTerms = solveTerm.solveTerm (nmax,V0)

#			print ""


if selectedMatrix == "xXHwyzZ":
	nmax = 1
	alphaSpecies = ("h","p")
	betaSpecies = ("H","P") 
	twoParticles = True

	for i in alphaSpecies: 
		for j in betaSpecies: 
			for k in alphaSpecies: 
				for l in alphaSpecies: 
					for m in alphaSpecies: 
						for n in betaSpecies: 

							nOccup = 0
							nVirtual = 0
							if abs(checkNumberOfParticles( [i,j] ))==2 and \
								abs(checkNumberOfParticles( [m,n] ))==2 :

								indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
								indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
								indexm, nOccup, nVirtual = getIndexForParticleHole(m,nOccup,nVirtual)
								indexn, nOccup, nVirtual = getIndexForParticleHole(n,nOccup,nVirtual)
								indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
								indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)


								indexi = "a_{"+indexi+"}"
								indexj = "a_{"+indexj+"}"
								indexk = "a_{"+indexk+"}^{\dagger}"
								indexl = "a_{"+indexl+"}"
								indexm = "a_{"+indexm+"}"
								indexn = "a_{"+indexn+"}"

								#superOperator = "\hat{H}"
								superOperator = "\hat{V}^{aa}"
								#superOperator = "\hat{V}^{ab}"

								#if (i+j+k+l) == "hHhP" :
								if (k+l) == "hp" or (k+l) == "ph" : #only excitations

									print "\\bf "+superOperator+"_{"+i+j+"-"+k+l+m+n+"} &",
									print "("+indexi+indexj+"|"+superOperator+indexk+indexl+\
									indexm+indexn+")"

									#solves the term
									V0 = subOperators (+1,[[indexi,indexj], \
										[superOperator,indexk,indexl,indexm,indexn ]], "" )
									finalTerms = solveTerm.solveTerm (nmax,V0)

			print "\\\\"
	print "f_4 |  a)"
	for i in alphaSpecies: 
		for j in betaSpecies: 
			for k in alphaSpecies: 
				for l in alphaSpecies: 
					for m in alphaSpecies: 
						for n in betaSpecies: 

							nOccup = 0
							nVirtual = 0
							if abs(checkNumberOfParticles( [i,j] ))==2 and \
								abs(checkNumberOfParticles( [m,n] ))==2 :

								indexm, nOccup, nVirtual = getIndexForParticleHole(m,nOccup,nVirtual)
								indexn, nOccup, nVirtual = getIndexForParticleHole(n,nOccup,nVirtual)
								indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
								indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
								indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
								indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)


								indexi = "a_{"+indexi+"}"
								indexj = "a_{"+indexj+"}"
								indexk = "a_{"+indexk+"}^{\dagger}"
								indexl = "a_{"+indexl+"}"
								indexm = "a_{"+indexm+"}"
								indexn = "a_{"+indexn+"}"

								#superOperator = "\hat{H}"
								superOperator = "\hat{V}^{aa}"
								#superOperator = "\hat{V}^{ab}"

								#if (i+j+k+l) == "hHhP" :
								if (k+l) == "hp" or (k+l) == "ph" : #only excitations

									print "\\bf "+superOperator+"_{"+i+j+"-"+k+l+m+n+"} &",
									print "("+indexk+indexl+indexm+indexn+"|"+superOperator+indexi+indexj+")"

									#solves the term
									V0 = subOperators (+1,[[indexk,indexl,indexm,indexn ], \
										[superOperator, indexi,indexj ]], "" )
									finalTerms = solveTerm.solveTerm (nmax,V0)

			print "\\\\"


if selectedMatrix == "xXHWYZz":
	nmax = 1
	alphaSpecies = ("h","p")
	betaSpecies = ("H","P") 
	twoParticles = True

	for i in alphaSpecies: 
		for j in betaSpecies: 
			for k in betaSpecies: 
				for l in betaSpecies: 
					for m in alphaSpecies: 
						for n in betaSpecies: 

							nOccup = 0
							nVirtual = 0
							if abs(checkNumberOfParticles( [i,j] ))==2 and \
								abs(checkNumberOfParticles( [m,n] ))==2 :

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
								#superOperator = "\hat{V}^{aa}"
								superOperator = "\hat{V}^{ab}"

								#if (i+j+k+l) == "hHhP" :
								if (k+l) == "HP" or (k+l) == "PH" : #only excitations

									print "\\bf "+superOperator+"_{"+i+j+"-"+k+l+m+n+"} &",
									#print "("+indexi+indexj+"|"+superOperator+indexk+indexl+\
									indexm+indexn+")"

									#solves the term
									V0 = subOperators (+1,[[indexi,indexj], \
										[superOperator,indexk,indexl,indexm,indexn ]], "" )
									#finalTerms = solveTerm.solveTerm (nmax,V0)

			print "\\\\"


if selectedMatrix == "xXyYzZHxXyYzZ":
	nmax = 1
	alphaSpecies = ("h","p")
	betaSpecies = ("H","P") 
	twoParticles = True
	count = 0 

	#f_4^a H f_4^a
	for i in alphaSpecies: 
		for j in alphaSpecies: 
			for k in alphaSpecies: 
				for l in betaSpecies: 
					for m in alphaSpecies: 
						for n in alphaSpecies: 
							for o in alphaSpecies: 
								for p in betaSpecies: 

									nOccup = 0
									nVirtual = 0
									if abs(checkNumberOfParticles( [k,l] ))==2 and \
										abs(checkNumberOfParticles( [o,p] ))==2 :

										if ((i+j) == "hp" or (i+j) == "ph") and ((m+n) == "hp" or (m+n) == "ph") : #only excitations

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

											superOperator = "\hat{H}"
											#superOperator = "\hat{V}^{aa}"
											#superOperator = "\hat{V}^{ab}"

											#if (i+j+k+l) == "hHhP" :

											print "\\bf "+superOperator+"_{"+i+j+k+l+"-"+m+n+o+p+"} &",
											print "("+indexi+indexj+indexk+indexl+"|"+superOperator+indexm+indexn+\
											indexo+indexp+")"

											#solves the term
											V0 = subOperators (+1,[[indexi,indexj,indexk,indexl], \
												[superOperator,indexm,indexn,indexo,indexp ]], "" )
											finalTerms = solveTerm.solveTerm (nmax,V0)
											count = count + 1
											print count

					print "\\\\"

		
	print "f_4^a H f_4^b"
	#f_4^a H f_4^b
	for i in alphaSpecies: 
		for j in alphaSpecies: 
			for k in alphaSpecies: 
				for l in betaSpecies: 
					for m in betaSpecies: 
						for n in betaSpecies: 
							for o in alphaSpecies: 
								for p in betaSpecies: 

									nOccup = 0
									nVirtual = 0
									if abs(checkNumberOfParticles( [k,l] ))==2 and \
										abs(checkNumberOfParticles( [o,p] ))==2 :

										if ((i+j) == "hp" or (i+j) == "ph") and ((m+n) == "HP" or (m+n) == "PH") : #only excitations

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

											superOperator = "\hat{H}"
											#superOperator = "\hat{V}^{aa}"
											#superOperator = "\hat{V}^{ab}"

											#if (i+j+k+l) == "hHhP" :

											print "\\bf "+superOperator+"_{"+i+j+k+l+"-"+m+n+o+p+"} &",
											print "("+indexi+indexj+indexk+indexl+"|"+superOperator+indexm+indexn+\
											indexo+indexp+")"

											#solves the term
											V0 = subOperators (+1,[[indexi,indexj,indexk,indexl], \
												[superOperator,indexm,indexn,indexo,indexp ]], "" )
											finalTerms = solveTerm.solveTerm (nmax,V0)

			print "\\\\"

	print "f_4^b H f_4^b"
	#f_4^b H f_4^b

	count = 0 
	for i in betaSpecies: 
		for j in betaSpecies: 
			for k in alphaSpecies: 
				for l in betaSpecies: 
					for m in betaSpecies: 
						for n in betaSpecies: 
							for o in alphaSpecies: 
								for p in betaSpecies: 

									nOccup = 0
									nVirtual = 0
									if abs(checkNumberOfParticles( [k,l] ))==2 and \
										abs(checkNumberOfParticles( [o,p] ))==2 :

										if ((i+j) == "HP" or (i+j) == "PH") and ((m+n) == "HP" or (m+n) == "PH") : #only excitations

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

											superOperator = "\hat{H}"
											#superOperator = "\hat{V}^{aa}"
											#superOperator = "\hat{V}^{ab}"

											#if (i+j+k+l) == "hHhP" :

											print "\\bf "+superOperator+"_{"+i+j+k+l+"-"+m+n+o+p+"} &",
											print "("+indexi+indexj+indexk+indexl+"|"+superOperator+indexm+indexn+\
											indexo+indexp+")"

											#solves the term
											V0 = subOperators (+1,[[indexi,indexj,indexk,indexl], \
												[superOperator,indexm,indexn,indexo,indexp ]], "" )
											finalTerms = solveTerm.solveTerm (nmax,V0)

											count = count + 1
											print count


			print "\\\\"




