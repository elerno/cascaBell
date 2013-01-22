# -*- coding: UTF-8 -*-

# Copyright Ernesto Illescas-Peláez 2007-2013

# This file is part of cascaBell.

# cascaBell is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# cascaBell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
#along with cascaBell.  If not, see <http://www.gnu.org/licenses/>.

## Contains classes that collect numeric utilities.

# Import python modules 
from math import sqrt

class Series(object):
	""" Contains methods to generate and work with numeric series.
	"""
	def __init__(self):
		""" Initialization of the class does nothing.
		"""
		pass

	def even(self, numOfElements):
		""" Constructs an even-number series of numOfElements.
		numOfElements	---> length of the returned list
		return			-->> a list of even numbers
		"""
		evenList    = []
		even        = 2
		for x in xrange(numOfElements):
			evenList.append(even)
			even = even + 2
		return evenList
	
	
	def odd(self, numOfElements):
		""" Constructs an odd-number series of numOfElements.
		numOfElements	---> length of the returned list
		return			-->> a list of odd numbers
		"""
		oddList    = []
		odd         = 1
		counter     = 0
		for x in xrange(numOfElements):
			oddList.append(odd)
			odd = odd+2
		return oddList
	
	
	def fibo(self, numOfElements):
		""" Constructs a fibonacci-number series of numOfElements.
		numOfElements	---> length of the returned list
		return			-->> a list of fibonacci numbers
		"""
		fiboList    = []
		a           = 0
		b           = 1
		for x in xrange(numOfElements):
			fiboList.append(b)
			a = b
			b = a + b
		return fiboList
	
	
	def prime(self, numOfElements):
		""" Constructs a prime-number series of numOfElements.
		numOfElements	---> length of the returned list
		return			-->> a list of prime numbers
		"""
		primeLst    = []
		candidate   = 2
		counter     = 0
		while counter < numOfElements:
			maxTest = int(sqrt(candidate)) + 1
			for x in range(2, maxTest):
				if candidate % x == 0:
					candidate += 1
					break
			else:
				primeLst.append(candidate)
				candidate += 1
				counter += 1
		return primeLst


	def geometric(self, growFactor, numOfElements):
		""" Constructs a list of geometrical values, where the starting
		point is the power.
		growFactor		---> a number from which to begin.
		numOfElements	---> numOfElements	---> the desired elements in the
						series
		return		--> a geometrical list
		"""
		geoLst	= [growFactor]

		for x in xrange(numOfElements - 1):
			lastVal = geoLst[-1]
			newVal = lastVal * growFactor
			geoLst.append(newVal)
		return geoLst


	def logarithmic(self, hastaNo, noDeElementos, reverse=0):
		"""
		"""
		pasos	= noDeElementos - 1
		poder	= 1.0 / pasos
		unPaso	= pow(hastaNo, poder)

		logaritmicos = [1]

		for x in range(pasos):
			nuevoValor = logaritmicos[-1] * unPaso
			logaritmicos.append(nuevoValor)

		if reverse == 1:
			intrvls = self.serToIntrvl(logaritmicos)
			intrvls.reverse()
			retrgrdSeries = self.intrvlsToSer(intrvls, logaritmicos[0])
			logaritmicos = retrgrdSeries
		return logaritmicos


	def serToIntrvl(self, lst):
		""" Converts a list of points into a list of intervals.
		"""
		intrvls = []

		a = lst[0]
		for x in lst:
			newIntrvl = x - a
			intrvls.append(newIntrvl)
			a = x
		intrvls.pop(0)
		return intrvls


	def intrvlsToSer(self, intrvls, strt):

		newLst	= [strt]

		for x in intrvls:
			elmnt = x + newLst[-1]
			newLst.append(elmnt)
		return newLst


	def aureusSer(self, start, numOfElements, reverse=0):
		""" Constructs a series of numOfElements elements where each
		point is the Aureus point of the former.
		start			---> value to be subdivided
		numOfElements	---> the number of elements.
		reverse		---> if 1, reverses the series.
		return		-->> a list
		"""
		aureus = start
		aureusSer = []
		for x in xrange(numOfElements):
			aureusSer.append(aureus)
			aureus *= 0.618
		if reverse:
			aureusSer.reverse()
		return aureusSer


########


class Scaling(object):
	""" Contains methods for scaling values or lists.
	"""
	def lstToTotl(self, aList, newTotl):
		"""Scales the values in aList so they add up to a new total.
		aList	---> the list to scale
		newTotl	---> the sum of all elements of the scaled list
		return	--> a scaled list
		"""
		oldTotl	= 0.0
		newLst		= []

		for x in aList:
			oldTotl += x

		if oldTotl:
			scaleFactor = newTotl / oldTotl
		else:
			scaleFactor = newTotl

		for x in aList:
			newVal = x * scaleFactor
			newLst.append(newVal)
		return newLst


	def valToRng(self, val, oldMin, oldMax, newMin, newMax):
		"""Scales a value within a range to it's equivalent in a new range.
		val		---> the value to be scaled.
		oldMin	---> the minimum of the old range
		oldMax	---> the maximum of the old range
		newMin	---> the minimum of the new range
		newMax	---> the maximum of the new range
		return 	--> a scaled value
		"""
		oldRng = (oldMax*1.0) - oldMin
		newRng = newMax - newMin
		ratio = newRng/oldRng
		scaledVal	= ((val - oldMin) * ratio + newMin)
		return scaledVal
########

class Interpolate(object):
	""" Contains methods for interpolation.
	"""
	def __init__(self):
		self.ListTools = ListTools()
	
	
	def gradlLstsLin(self, original, target):
		""" Returns a list where the first value comes from the original
		list, the last one from the target, and in-between values that 			incrementally approach the target. The interpolation is linear.
		"""
		newLst		= []
		noOfStps	= len(target)
		counter		= 0

		for x in xrange(noOfStps):
			if len(original) != len(target):
				print 'Interpol: lists must be the same size'
				break
			dist = target[counter] - original[counter]
			oneStp = float(dist) / noOfStps
			partlInrpl = original[counter] + (oneStp * (counter + 1))
			newLst.append(partlInrpl)
			counter += 1
		return newLst


	def aToBInSteps(self, a, b, numSteps):
		""" Construct a list that linearly goes from a to b in n steps.
		"""
		if a < b:
			start	= a
			end		= b
		else:
			start	= b
			end		= a
#		else:
#			print 'Start value and end value can not be the same!'
#		if numSteps < 1:
#			print 'numSteps must be greater than 1!'
		series = range(0, numSteps)
		magnitude = end - start
		scaledSeries = self.ListTools.normList(series, magnitude)
		interpolation = []
		for x  in scaledSeries:
			element = x + start
			interpolation.append(element)
		if a > b:
			interpolation.reverse()
		return interpolation



class ListTools(object):
	""" Contains methods to manipulate lists.
	"""
	def __init__(self):
		"""
		"""
		pass


	def addConstant(self, constant, lst):
		""" Adds a constant to all elements in a list.
		constatn	---> a number
		lstToTotl	---> a list
		return		-->> a list with the constant added to its elements
		"""
		newList = []
		for x in lst:
			newValue = x + constant
			newList.append(newValue)
		return newList
	
	
	def normList(self, toNormalize, normalizeTo=1):
		""" Normalize values of a list to make its max = normalizeTo.
		toNormalize	---> list to normalize
		normalizeTo	---> maximum value
		return		-->> a list
		"""

		vMax = max(toNormalize)
		normList = []
		for x in toNormalize:
			newVal = x / (vMax * 1.0) * normalizeTo
			normList.append(newVal)
		return normList

##========================================================================
	def normListSumTo(self, L, sumTo=1):
	    '''normalize values of a list to make it sum = sumTo'''
	
	    sum = reduce(lambda x,y:x+y, L)
	    return [ x/(sum*1.0)*sumTo for x in L]
##========================================================================
