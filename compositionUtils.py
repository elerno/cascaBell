# -*- coding: UTF-8 -*-

# Copyright Ernesto Illescas-Peláez 2009-2013

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
	def even(self, numOfElements):
		""" Constructs an even-number series of numOfElements.
		numOfElements	---> length of the returned list
		return			-->> a list of even numbers
		"""
		evenList	= []
		even		= 2
		for x in xrange(numOfElements):
			evenList.append(even)
			even = even + 2
		return evenList
	
	
	def odd(self, numOfElements):
		""" Constructs an odd-number series of numOfElements.
		numOfElements	---> length of the returned list
		return			-->> a list of odd numbers
		"""
		oddList	= []
		odd		= 1
		counter	= 0
		for x in xrange(numOfElements):
			oddList.append(odd)
			odd = odd + 2
		return oddList
	
	
	def fibo(self, numOfElements):
		""" Constructs a fibonacci-number series of numOfElements.
		numOfElements	---> length of the returned list
		return			-->> a list of fibonacci numbers
		"""
		fiboList	= []
		a			= 0
		b			= 1
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
		primeList	= []
		candidate	= 2
		counter		= 0
		while counter < numOfElements:
			maxTest = int(sqrt(candidate)) + 1
			for x in range(2, maxTest):
				if candidate % x == 0:
					candidate += 1
					break
			else:
				primeList.append(candidate)
				candidate += 1
				counter += 1
		return primeList
	
	
	def geometric(self, growFactor, numOfElements):
		""" Constructs a list of geometric values, starting at growFactor.
		growFactor		---> the ratio between succesive terms
		numOfElements	---> length of the returned list
		return			-->> a list of geometric values
		"""
		geoList	= [growFactor]
		for x in xrange(numOfElements - 1):
			lastVal = geoLst[-1]
			newVal = lastVal * growFactor
			geoList.append(newVal)
		return geoList
	
	
	def logarithmic(self, limit, numOfElements):
		""" Constructs a list of numOfElements logarithmic values, with
		limit maximum value.
		limit			---> list's maximum value
		numOfElements	---> length of the returned list
		return			-->> a list of prime numbers
		"""
		steps			= numOfElements - 1
		power			= 1.0 / steps
		oneStep			= pow(limit, power)
		logarithmicList	= [1]
		for x in range(steps):
			newValue = logarithmicList[-1] * oneStep
			logarithmicList.append(newValue)
		return logarithmicList
	
	
	def seriesToIntervals(self, points):
		""" Converts a list of points into a list of intervals.
		points	---> a list of points.
		return	-->> a list of intervals.
		"""
		intrvals	= []
		a			= points[0]
		for x in points:
			newIntrval = x - a
			intrvals.append(newIntrval)
			a = x
		intrvals.pop(0)
		return intrvals
	
	
	def intervalsToSeries(self, intervals, start, modulo=None):
		""" Constructs a list of values from a list of intervals.
		intervals	---> a list of intervals.
		start		---> the starting ponit of the returned series.
		return		-->> a list
		"""
		series	= [start]
		for x in intervals:
			element = x + series[-1]
			if modulo:
				element = element % 12
			series.append(element)
		return series
	
	
	def aureusSer(self, start, numOfElements, reverse=0):
		""" Constructs a series of numOfElements elements where each
		point is the Aureus point of the former.
		start			---> value to be subdivided
		numOfElements	---> the number of elements.
		reverse		---> if 1, reverses the constructed series.
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



class Scaling(object):
	""" Contains methods for scaling values and for scaling lists.
	"""
	def valueToRange(self, value, oldMin, oldMax, newMin, newMax):
		"""Scales a value within a range to it's equivalent in a new range.
		value	---> the value to be scaled.
		oldMin	---> the minimum of the old range
		oldMax	---> the maximum of the old range
		newMin	---> the minimum of the new range
		newMax	---> the maximum of the new range
		return 	--> a scaled value
		"""
		oldRange = (oldMax*1.0) - oldMin
		newRang = newMax - newMin
		ratio = newRange/oldRange
		scaledValue	= ((value - oldMin) * ratio + newMin)
		return scaledValue
	
	
	def normalize(self, toNormalize, normalizeTo=1):
		""" Normalize values of a list to make its max = normalizeTo.
		toNormalize	---> list to normalize
		normalizeTo	---> maximum value
		return		-->> a list
		"""
		largestValue = max(toNormalize) * 1.0
		normList = []
		for x in toNormalize:
			newVal = x / largestValue * normalizeTo
			normList.append(newVal)
		return normList
	
	
	
class ListTools(object):
	""" Contains methods to manipulate lists.
	"""
	def addConstant(self, constant, originalList):
		""" Adds a constant to all elements in a list.
		constant	---> a number
		originalList	---> a list
		return		-->> a list with the constant added to its elements
		"""
		newList = []
		for x in originalList:
			newValue = x + constant
			newList.append(newValue)
		return newList

##========================================================================
	def normListSumTo(self, L, sumTo=1):
	    '''normalize values of a list to make it sum = sumTo'''
	
	    sum = reduce(lambda x,y:x+y, L)
	    return [ x/(sum*1.0)*sumTo for x in L]
##========================================================================
