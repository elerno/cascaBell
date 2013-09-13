# -*- coding: UTF-8 -*-

## Score generation classes.

import random
import math
import decimal

import Numeric_utils as NumericUtils


class StrtTms(object):
	""" Contains methods to generate start time lists for score
	statements. Generally, an extra iteration is needed in order to
	calculate the last duration.
	"""
	def __init__(self, spanSer, minIntrvl=1):
		""" Define the initialization attributes.
		spanSer		---> a list of (possible spans between start times
		minIntrvl	---> the equivalence of 1 in spanSer (default = 1)
		"""
		self.spanSer		= spanSer
		self.minIntrvl		= minIntrvl
		self.vals			= [self.spanSer.pop(0)]
		self.noReps			= 2
		self.reps			= 0
		self.elmsInVals 	= 1
		self.countNextval	= 0
		self.nxtStrt		= 0
		self.inPlaceVal		= 0
		self.indxMem		= 0
		self.counter		= 0

	def addtvSerPerm(self):
		""" Gradually constructs a series with next value of spanSer.
		Each series is shuffled reps time, but leaving the new
		element as first value.
		"""
		if self.reps == self.noReps and len(self.spanSer):
			frst = self.spanSer.pop(0)
			self.reps = 0
		else:
			frst = self.vals.pop(0)
			self.reps += 1
		random.shuffle(self.vals)
		self.vals.insert(0, frst)
		self.elmsInVals = len(self.vals)
		self.countNextval	= 0


	def nxtValASP(self):
		""" Extracts one value at a time from (consecutive) lists
		created by addtvSerPerm().
		"""
		if not self.elmsInVals:
			self.addtvSerPerm()
		nxtIntrvl = self.vals[self.countNextval]
		self.elmsInVals -= 1
		self.countNextval += 1
		self.nxtStrt += nxtIntrvl
		return round(self.nxtStrt * self.minIntrvl, 5)


	def linToLog(self, strtsLst, lastStrt, reverse = 0):
		""" Map start times expressed in a linear scale into a
		logarithmic one.
		"""
		sumatory	= 0

		for x in strtsLst:
			sumatory += x

		logScale	= Series.logar(lastStrt, sumatory)

		if reverse == 1:
			intrvls = Series.serToIntrvl(logScale)
			intrvls.reverse()
			retrgrdSeries = intrvlsToSer(intrvls, logScale[0])
			logScale = retrgrdSeries

		logStrts	= []

		for x in strtsLst:
			accumul	= 0
			onOff	= 1
			for y in xrange(x):
				accumul += logScale.pop(0)
				if onOff:
					logStrts.append(accumul)
					onOff = 0
		return logStrts

	def inPlaceRotation(self):
		"""
		"""
		if not self.inPlaceVal:
			self.spanSer.insert(0, self.vals[0])
			random.shuffle(self.spanSer)
			self.inPlaceVal = self.spanSer[0]
			val = self.inPlaceVal
			self.indxMem += 1
		elif self.indxMem < len(self.spanSer):
			val = self.spanSer[self.indxMem]
			self.indxMem += 1
		elif self.indxMem == len(self.spanSer):
			indexOfFixed = self.spanSer.index(self.inPlaceVal)
			self.spanSer.remove(self.inPlaceVal)
			newLast =self.spanSer.pop(0)
			self.spanSer.append(newLast)
			self.spanSer.insert(indexOfFixed, self.inPlaceVal)
			val = self.spanSer[0]
			self.indxMem = 1
		self.counter += 1
		if self.counter == len(self.spanSer) * (len(self.spanSer) -1):
			random.shuffle(self.spanSer)
			self.inPlaceVal = self.spanSer[0]
		return val * self.minIntrvl
		


class Durs(object):
	"""
	Contains methods to generate duration lists for score
	statements.
	"""
	def __init__(self):
		""" Define the initialization attributes.
		"""
		self.prevStrt	= -1

	def fullDur(self, strt):
		if self.prevStrt >= 0:
			dur = strt - self.prevStrt
			self.prevStrt = strt
			return dur
		else:
			self.prevStrt	= strt


class Envls(object):
	"""
	"""
	def __init__(self, vals, dists, totDist):
		"""
		"""
		self.vals 		= vals
		self.totDist	= totDist
		self.dists		= dists
		self.compEnv	= self.propLst()
		self.envLst		= self.complLst()


	def propLst(self):
		"""
		"""
		tstDists	= 0
		for x in self.dists:
			tstDists += x
		if tstDists != 100:
			print 'Warning the sum of totDists should tipically be 100'
		if self.vals == [] or not self.totDist or self.dists == []:
			print 'Error: Set vals, totDist and dists attributes before hand!'
		if len(self.vals) != len(self.dists) + 1:
			print 'Error vals list should have one more element than dists!'
		
		else:
			envTpl	= []

			for x, y in zip(self.vals, self.dists):
				envTpl.extend([x, (y / float(100)) * self.totDist])
			envTpl.append(self.vals[-1])
		return envTpl


	def complLst(self):
		""" If the list of tuples is not as long as required by
		instrument 4, complete it.
		"""
		compEnv	= self.envTpl

		while len(self.envTpl) != 9:
			compEnv.extend([0,0])
		return compEnv


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

