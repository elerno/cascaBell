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

## Contains classes that collect frequency domain methods.

# Import user modules
import algorithmicTools

# Instantiate utility classes.
Series = algorithmicTools.Series()

class Spctrm(object):
	""" Contains the methods to generate harmonic-based notes.
	"""
	def mkPartls(self, spectType, numOfPartls):
		""" Generates a list of partials that will be used to generate
		spectra.
		spectType	---> type of spectrum (0=all partials, 1=odd
						partls, 2=even partls,	3=fibonacci partls and
						4=prime partls)
		numOfPartls	---> number of partials to generate
		return		--> a partial-series list
		"""
		if spectType == 3:
			numOfPartls += 1
		kinds		= ['pa', Series.odd, Series.even,
						Series.fibo, Series.prime]
		if not spectType:
			partls	= range(1, numOfPartls + 1)
		else:
			kindChoice	= kinds.pop(spectType)
			partls		= kindChoice(numOfPartls)
		if spectType == 3:
			partls.pop(0)
		return partls


	def dSpect(self, fundFreq, partls, distor):
		""" Constructs a distorted harmonic spectrum based on the 
		iteration of the function "s = f*p to the d", where s is the
		spectrum, f is de fundamental frequency, p is the partial
		number, and d is a distortion factor.
		fundFreq	---> the fundamental frequency
		partls		---> the partials present in the spectrum
		distor		---> the distortion factor
		return		---> a distorted-harmonic-spectrum list
		"""
		spect	= []
		for x in xrange(len(partls)):
			onePartl = partls[x]
			distorPartl = pow(onePartl, distor)
			onePartlFreq = fundFreq * distorPartl
			# Control that harmonics over the audible range are not
			#generated.
			if  onePartlFreq < 20000 :
				onePartlFreq = round(onePartlFreq, 3)
				spect.append(onePartlFreq)
			else:
				print 'Exceeded audible range!!!'
				break
		return spect


class EqTmpr(object):
	"""
	"""
	def __init__(self, strtFreq=53, mod=12):
		"""
		"""
		self.strtFreq	= strtFreq
		self.maxFreq	= 20000
		self.mod		= mod
		self.pitchFreqDict, self.pitchnumPitchDict, self.pitchPitchnumDict	= self.modNDicts()


	def temperPitch(self, pitchNo):
		"""
		"""
		step = math.pow(math.e, math.log(2) / self.mod)
		pitch = self.strtFreq * math.pow(step, pitchNo)
		return pitch


	def octsModN(self):
		"""
		"""
		pitches	= []
		counter	= 0

		while 1:
			pitch = self.temperPitch(counter)
			if pitch < self.maxFreq:
				pitches.append(pitch)
			else:
				break
			counter += 1
		return pitches


	def modNDicts(self):
		"""
		"""
		allPitches			= self.octsModN()
		counter				= 0
		modStr				= str(self.mod)
		divisorRem			= decimal.Decimal(1)
		pithcFreqDict		= {'mod': self.mod}
		pitchnumPitchDict	= {}
		pitchPitchnumDict	= {}

		for x in modStr:
			divisorRem = divisorRem * decimal.Decimal('0.1')


		for x in allPitches:
			compKey = divmod(counter, self.mod)
			key = str(decimal.Decimal(str(compKey[0])) + (decimal.Decimal(str(compKey[1])) * divisorRem))
			pithcFreqDict[key] = x
			pitchnumPitchDict[str(counter)] = key
			pitchPitchnumDict[key] = counter
			counter += 1
		return pithcFreqDict, pitchnumPitchDict, pitchPitchnumDict


	def makePitchFile(self):
		"""
		"""
		allPitches		= self.octsModN()
		counter		= 0
		modStr			= str(self.mod)
		divisorRem		= decimal.Decimal(1)
		modNDict	= {'mod': self.mod}

		for x in modStr:
			divisorRem = divisorRem * decimal.Decimal('0.1')


		for x in allPitches:
			compKey = divmod(counter, self.mod)
			key = str(decimal.Decimal(str(compKey[0])) + (decimal.Decimal(str(compKey[1])) * divisorRem))
			modNDict[key] = x
			counter += 1
		return modNDict


	def numToFreq(self, number):
		"""
		"""
		pitchPrts = divmod(number, self.mod)
		if pitchPrts[1] < 10:
			pitch	= ''.join([str(pitchPrts[0]), '.0', str(pitchPrts[1])])
		else:
			pitch	= ''.join([str(pitchPrts[0]), '.', str(pitchPrts[1])])
		freq = self.dict[pitch]
		return freq
