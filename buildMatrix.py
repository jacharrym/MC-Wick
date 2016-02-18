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
#V0 = subOperators (+1,["a_{a}^{\dagger}", "a_{B}^{\dagger}","\hat{H}","a_{c}","a_{D}" ], "" )

#solves one term
#finalTerms = solveTerm.solveTerm (nmax,V0)

alphaSpecies = ("h","p")
betaSpecies = ("H","P") 
for i in betaSpecies: 
	for j in alphaSpecies: 
		for k in betaSpecies: 
			for l in alphaSpecies: 
				nOccup = 0
				nVirtual = 0
				print j+i+"-"+l+k,
				indexj, nOccup, nVirtual = getIndexForParticleHole(j,nOccup,nVirtual)
				indexi, nOccup, nVirtual = getIndexForParticleHole(i,nOccup,nVirtual)
				indexl, nOccup, nVirtual = getIndexForParticleHole(l,nOccup,nVirtual)
				indexk, nOccup, nVirtual = getIndexForParticleHole(k,nOccup,nVirtual)
				print indexj, indexi, indexl, indexk
				V0 = subOperators (+1,["a_{"+indexj+"}^{\dagger}", "a_{"+indexi+"}^{\dagger}",\
							"\hat{H}","a_{"+indexl+"}","a_{"+indexk+"}" ], "" )
				finalTerms = solveTerm.solveTerm (nmax,V0)
		print ""

