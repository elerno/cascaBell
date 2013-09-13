# -*- coding: UTF-8 -*-

# Import python modules
import sys
# Import user Modules
import Numeric_utils as NumericUtils

# Instantiate Classes
ListTools = NumericUtils.ListTools()


class CsndNotes(object):
	""" Contains methods to construct Csound note statements.
	"""
	def __init__(self, instrNum, pFieldNum):
		""" Sets the Csound intrument number.
		instrNo	---> an integer (or string for named instruments)
		"""
		self.pFieldNum	= pFieldNum
		self.instrNum	= 'i{0}'.format(instrNum)


	def makeNote(self, parameterList):
		""" Makes a Csound note statemen from a list of parameters. The
		list should not include the instrument number!
		p4List	---> a list of parameters starting with p2
		return	-->> a string representing a note statement.
		"""
		# Test to see that the list of parameters is adequate for the
		#Csound instrument.
		if len(parameterList) + 1 != self.pFieldNum:
			sys.exit('Too little or too many parameters given ton CsndNote.makeNote()')
		# Make the note statement.
		formatString	= self.instrNum
		counter	= 0
		for x in xrange(len(parameterList)):
			formatString += ' {{{0}}}'.format(counter)
			
			counter += 1
		noteStatement = formatString.format(*parameterList) + '\n'
		return noteStatement



class CsndFunctions(object):
	""" Contains methods to construct Csound function statements.
	"""
	def __init__(self):
		"""
		"""
		pass


	def pointDistPoint(self, functNum, time, size, genRoutine, parameters, scale=True):
		""" Method to construct functions who's parameters follow the form
		[val, dist, val ...].
		functNum	---> The function number
		time		---> Function load time in seconds
		size		---> the size of the table (if size != 2^n,
							it must be negative)
		genRoutine	---> gen routine number to be used.
		parameters	---> a list of values. len() must be odd
		scale		---> if one, scales dists to add to size (default=1)
		return		-->> a function statement string.
		"""
		# Test to see that the list of parameters is odd.
		if not len(parameters) % 2:
			sys.exit('The number of values in parameters must be odd!')
		# Scale the distances if required.
		if scale:
			parameters = self.scaleDists(parameters, size)
		# Add extra parameters to ensure the f-table will nott be filled
		#with zeroes due to rounding.
		extraPars = [1000, parameters[-1]]
		parameters += extraPars
		# First part of the function definition.
		funct1	= 'f{0} {1} {2} {3}'.format(functNum, time, size, genRoutine)
		# Make second part of the definition.
		formatString	= ''
		counter	= 0
		for x in xrange(len(parameters)):
			formatString += ' {{{0}}}'.format(counter)
			
			counter += 1
		funct2 = formatString.format(*parameters)
		#Make function definition.
		functStatement	= funct1 + funct2 + '\n'
		return functStatement
		
		
	def pointsValsToTable(self, points, values):
		""" Merges a list of points and a list of values into a list
		of [point, interval point, ...].
		points	---> a list of points (x-axis)
		values	---> a list of values (y-axis)
		return	-->> a list of [point, interval, point, ...]
		"""
		# Check that the input data is valid.
		if len(points) != len(values):
			sys.exit('Length of points and values should be equal!')
		if points[0]:
			sys.exit('Table\'s first point should be zero!')
		# Make the intervals.
		intervals		= []
		previousPoint	= points.pop(0)
		for point in points:
			interval = point - previousPoint
			intervals.append(interval)
			previousPoint = point
		# Make the table values.
		tableValues	= []
		while len(intervals):
			tableValues.append(values.pop(0))
			tableValues.append(intervals.pop(0))
		tableValues.append(values.pop(0))
		return tableValues
	
	
	def scaleDists(self, valDistValList, total):
		""" Scale distances in a list of the form [val, dist, val...] so
		that they add up to total.
		valDistValList	---> a list
		total			---> the total the elements of the list will add
								up to
		return			-->> a new list where the odd elements sum total
		"""
		vals = []
		dists = []
		counter = 0
		# Separate values and dists.
		for x  in valDistValList:
			if counter % 2:
				dists.append(x)
			else:
				vals.append(x)
			counter += 1
		# Normalize the dists so that they add up to table size.
		distsNorm	= ListTools.normListSumTo(dists, abs(total))
		# Reconstruct the parameter list.
		parameters = []
		while len(vals):
			par = vals.pop(0)
			parameters.append(par)
			try:
				par = distsNorm.pop(0)
			except IndexError:
				break
			parameters.append(par)
		return parameters
