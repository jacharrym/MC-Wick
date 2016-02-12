#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import signal
import copy
import sys
import wick

## subOperators
class subOperators(object):
	def __init__(self,sign,string,scalar):
		self.sign = sign
		self.string = string
		self.scalar = scalar

## Return the subindex of the operator
def index ( operator ) :
	auxindex = operator.split("_")[1]
	initial = auxindex.find("{")
	final = auxindex.find("}")
	return auxindex[initial+1:final]


V0 = subOperators (+1,["a_{p}^{\dagger}", "a_{Q}^{\dagger}","\hat{H}","a_{r}","a_{S}" ], "" )
# wX \hat{A} yZ
# = [X^\dagger w^\dagger , \hat{A} y Z ]_+
# = X^\dagger w^\dagger \hat{A} y Z + \hat{A} y Z  X^\dagger w^\dagger
# = X^\dagger w^\dagger y Z A (1) - X^\dagger w^\dagger A y Z (2)  + 
# y Z A  X^\dagger w^\dagger (3) - A y Z  X^\dagger w^\dagger (4)

V1 = subOperators (+1,[V0.string[1], V0.string[0], V0.string[3], V0.string[4], V0.string[2]], "" )
if "{H}" in V1.string[4] :
	V1.scalar = "E"
	del V1.string[4]
V2 = subOperators (-1,[V0.string[1], V0.string[0], V0.string[2], V0.string[3], V0.string[4]], "" )
if "{H}" in V2.string[2] :
	V2.scalar = "E" + "-\epsilon_{" + index(V2.string[3]) + "}" + "-\epsilon_{" + index(V2.string[4])
	del V2.string[2]
V3 = subOperators (+1,[V0.string[3], V0.string[4], V0.string[2], V0.string[1], V0.string[0]], "" )
if "{H}" in V3.string[2] :
	V3.scalar = "E" + "+\epsilon_{" + index(V3.string[0]) + "}" + "+\epsilon_{" + index(V3.string[1])
	del V3.string[2]
V4 = subOperators (-1,[V0.string[2], V0.string[3], V0.string[4], V0.string[1], V0.string[0]], "" )
if "{H}" in V4.string[0] :
	V4.scalar = "E"
	del V4.string[0]

allV = [V1,V2,V3,V4]
#V1.string.append("a_{t}")
#V1.string.append("a_{u}")
#allV = [V1]
	
for Vi in allV :
	print "##", Vi.string, Vi.scalar
	wick.wick(Vi)

## =====================
## END PROGRAM
## ====================
