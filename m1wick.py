## =====================
## Method 1
## =====================

print "="*10
print "== Method 1, available only for singles and doubles contractions until N=5 "
print "="*10

## Zero 
sign = 1
NV, sign = normalOrder (V0.string,sign)
print "Zero"
print "\t" +symbolOfSign(sign)+longformat(NV)

## Singles
print "Singles"
for m in range (0,len(V0.string)):
	for n in range (m+1,len(V0.string)):
		auxV = list()
		auxV = list(V0.string)
		auxSign = 1
		auxCommutator = evaluateContraction ( V0.string[m], V0.string[n] )

		removeOperator(auxV,m)
		removeOperator(auxV,n-1)

		auxV , auxSign = normalOrder(auxV,auxSign)
		auxSign = auxSign * auxCommutator.sign

		# Rule C of Wick's theorem for fermions:
		#   rearrange the operators (introducing minus signs whenever the order of two fermionic operators is swapped) to ensure the contracted terms are adjacent in the string.
		if fermions == True :
			if (m - n)%2 == 1 : # Odd number -> odd distance between operators -> even number of permutations -> same sign
				auxSign = auxSign
			elif (m - n)%2 == 0 : # even number -> even distance between operators -> odd number of permutations -> opposite sign
				auxSign = -auxSign

		if auxSign == 0:
			value = "\t+0"
		else :
			value = "\t"+ symbolOfSign(auxSign)+auxCommutator.string+longformat(auxV)

		print value
# Doubles
print "Doubles"
for m in range (0,len(V0.string)):
	for n in range (m+1,len(V0.string)):

		auxV1 = list()
		auxV1 = list(V0.string)
		auxSign1 = 1
		auxCommutator1 = evaluateContraction ( V0.string[m], V0.string[n] )

		removeOperator(auxV1,m)
		removeOperator(auxV1,n-1)

#		auxV1 , auxSign1 = normalOrder(auxV1,auxSign1)
		auxSign1 = auxSign1 * auxCommutator1.sign

		# Rule C of Wick's theorem for fermions:
		#   rearrange the operators (introducing minus signs whenever the order of two fermionic operators is swapped) to ensure the contracted terms are adjacent in the string.
		if fermions == True :
			if (n - m)%2 == 1 : # Odd number -> odd distance between operators -> even number of permutations -> same sign
				auxSign1 = auxSign1
			elif (n - m)%2 == 0 : # even number -> even distance between operators -> odd number of permutations -> opposite sign
				auxSign1 = -auxSign1

		for o in range (m+1,len(V0.string)):
			for p in range (o+1,len(V0.string)):
				if n != o and n != p:

					auxV2 = list()
					auxV2 = list(V0.string)
					auxSign2 = 1
					auxCommutator2 = evaluateContraction ( V0.string[o], V0.string[p] )

					removeOperator(auxV2,o)
					removeOperator(auxV2,p-1)

					auxV3 = list()
					auxV3 = list(V0.string)

					removeOperator(auxV3,m)
					removeOperator(auxV3,n-1)

					if n < o :
						removeOperator(auxV3,o-2)
					else :
						removeOperator(auxV3,o-1)
					if n < p :
						removeOperator(auxV3,p-3)
					else :
						removeOperator(auxV3,p-2)

#					auxV2 , auxSign2 = normalOrder(auxV2,auxSign2)
					auxSign2 = auxSign2 * auxCommutator2.sign

					# Rule C of Wick's theorem for fermions:
					#   rearrange the operators (introducing minus signs whenever the order of two fermionic operators is swapped) to ensure the contracted terms are adjacent in the string.
					if fermions == True :
						if (p - o)%2 == 1 : # Odd number -> odd distance between operators -> even number of permutations -> same sign
							auxSign2 = auxSign2
						elif (p - o)%2 == 0 : # even number -> even distance between operators -> odd number of permutations -> opposite sign
							auxSign2 = -auxSign2
					
					finalSign = auxSign1 * auxSign2



					if finalSign == 0:
						value = "\t+0"
					else :
						value = "\t"+ symbolOfSign(finalSign)+auxCommutator1.string+auxCommutator2.string + longformat(auxV3)

					print value



