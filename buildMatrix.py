#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import solveTerm

global occupiedIndexesAlpha
global virtualIndexesAlpha
global occupiedIndexesBeta
global virtualIndexesBeta

occupiedIndexesAlpha = ("i","j","k","l","m","n","o","p","q","r","s")
virtualIndexesAlpha  = ("a","b","c","d","e","f","g","h")
occupiedIndexesBeta  = ("I","J","K","L","M","N","O","P","Q","R","S")
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


nmax = 2
alphaSpecies = ("h","p")
betaSpecies = ("H","P") 
#alphaSpecies = ("h")
#betaSpecies = ("H") 

#####
#j = "p"
#i = "P"
#l = "p"
#k = "P"
#nOccup = 0
#nVirtual = 0
#print j+i+"-"+l+k,
#indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
#indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
#indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)
#indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
#print indexj, indexi, indexl, indexk
#
#indexj = "a_{"+indexj+"}^{\dagger}"
#indexi = "a_{"+indexi+"}^{\dagger}"
#indexl = "a_{"+indexl+"}"
#indexk = "a_{"+indexk+"}"
#superOperator = "\hat{H}"
#
##solves ther ji-lk term 
##V0 = subOperators (+1,[indexj,indexi,superOperator,indexl,indexk ], "" )
##finalTerms = solveTerm.solveTerm (nmax,V0)
#
#superOperator = "\hat{V}"
##solves ther ji-lk term 
#V0 = subOperators (+1,[indexj,indexi,superOperator,indexl,indexk ], "" )
#finalTerms = solveTerm.solveTerm (nmax,V0)

######




#for i in betaSpecies: 
#	for j in alphaSpecies: 
#		for k in betaSpecies: 
#			for l in alphaSpecies: 
#				nOccup = 0
#				nVirtual = 0
#				print j+i+"-"+l+k,
#				indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
#				indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
#				indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)
#				indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
#				print indexj, indexi, indexl, indexk
#
#				indexj = "a_{"+indexj+"}^{\dagger}"
#				indexi = "a_{"+indexi+"}^{\dagger}"
#				indexl = "a_{"+indexl+"}"
#				indexk = "a_{"+indexk+"}"
#				superOperator = "\hat{H}"
#
#				#solves ther ji-lk term 
#				#V0 = subOperators (+1,[indexj,indexi,superOperator,indexl,indexk ], "" )
#				#finalTerms = solveTerm.solveTerm (nmax,V0)
#
#
#				superOperator = "\hat{V}"
#				#solves ther ji-lk term 
#				V0 = subOperators (+1,[indexj,indexi,superOperator,indexl,indexk ], "" )
#				finalTerms = solveTerm.solveTerm (nmax,V0)
#
#		print ""

nmax = 1
alphaSpecies = ("h")
betaSpecies = ("p") 

print "One Particle"

for i in alphaSpecies: 
	for j in betaSpecies: 
		nOccup = 0
		nVirtual = 0
		print j+"-"+i,
		indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
		indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
		print indexj, indexi

		indexj = "a_{"+indexj+"}^{\dagger}"
		indexi = "a_{"+indexi+"}"
		#superOperator = "\hat{H}"
		superOperator = "\hat{V}"
		#solves ther ji-lk term 
		V0 = subOperators (+1,[indexj,superOperator,indexi ], "" )
		finalTerms = solveTerm.solveTerm (nmax,V0)
print ""

