# -*- coding: UTF-8 -*-


# Import user modules
import csdComponents

class PyOrcCsd(object):
	""" Generate a Csound .csd file out of a csd.Components and a .orc file. 
	"""
	def __init__(self, orcFile, outFile):
		"""
		orcFile			---> a string representing a filename.
		outFile			---> a string representing a filename.
		"""
		# Open read-write files
		orc = open(orcFile, 'r')
		self.outFile = open(outFile, 'w')
		# Write options, orchestra, functions, p-field examples,
		#extra-duration function and tempo to .csd file.
		self.outFile.write(csdComponents.options)
		orcLines = orc.readlines()
		for line in orcLines:
			self.outFile.write(line)
		orc.close() # Close no longer used file to save memory.
		self.outFile.write(csdComponents.endOrcStartSco)
		self.outFile.write(csdComponents.functionTables)
		self.outFile.write(csdComponents.durationFunction)
	
	
	def insertAdvance(self, performanceStart):
		""" Insert an advance socre statement.
		"""
		self.outFile.write('\n; Advance statement\n')
		aStatement = 'a 0 0 {0}\n'.format(performanceStart)
		self.outFile.write(aStatement)
					
					
	def writeEndOfCsd(self):
		""" This method needs to be executed after the score has been
		processed. Otherwise, the produced .csd will be incomplete!!!
		"""
		self.outFile.write(csdComponents.endFile)



class RoseOrcCsd(object):
	""" Generate a Csound .csd file out of a csd.Components, a midi->csd
	from  Rosegarden and a .orc file. 
	"""
	def __init__(self, rosegardenFile, orcFile, outFile):
		"""
		rosegardenFile	---> a string representing a filename.
		orcFile			---> a string representing a filename.
		outFile			---> a string representing a filename.
		"""
		# Open read-write files
		rosegarden = open(rosegardenFile, 'r')
		orc = open(orcFile, 'r')
		self.outFile = open(outFile, 'w')
		# Get score lines from rosegardenFile and close it.		
		self.scoLines = rosegarden.readlines()
		rosegarden.close()
		# Write options, orchestra, functions, p-field examples,
		#extra-duration function and tempo to .csd file.
		self.outFile.write(csdComponents.options)
		orcLines = orc.readlines()
		for line in orcLines:
			self.outFile.write(line)
		orc.close() # Close no longer used file to save memory.
		self.outFile.write(csdComponents.endOrcStartSco)
		self.outFile.write(csdComponents.functionTables)
		self.outFile.write(csdComponents.pFieldExplaination)
		self.outFile.write(csdComponents.durationFunction)
		for line in self.scoLines:	
			if line[0] == 't':
				tempoStatement = line
				self.outFile.write('; Tempo statement\n')
				self.outFile.write(tempoStatement)
				self.outFile.write('\n; Note statements\n')
	
	
	def insertAdvance(self, performanceStart):
		""" Insert an advance socre statement.
		"""
		self.outFile.write('\n; Advance statement\n')
		aStatement = 'a 0 0 {0}\n'.format(performanceStart)
		self.outFile.write(aStatement)
	
		
	def scoreProcessing(self):
		""" Example method that writes only i-statements to the .csd out
		file. 
		"""
		for line in scoLines:
			if line[0] != ';':	# Only deal with non-comment lines.
				#Convert score line into a list of p-fields. 
				stringList = line.split()
				if len(stringList) == 5: # Only deal with i-statements.
					###
					# Processing of score statemnts could happen here.
					iNumber	= stringList[0]
					iStart	= stringList[1]
					iDur	= stringList[2]
					iPch	= stringList[3] # rosegarden converts from
											#midi note-number to octave
											#point pitch-class
					iVel	= stringList[4] # midi velocity.
					###
					# Since this is an example method, just re-build the
					#score statement and write it to file.
					iStatement = '{0}\t{1}\t{2}\t{3}\t{4}'.format(iNumber,
																	iStart,
																	iDur,
																	iPch,
																	iVel
																	)
					self.outFile.write(iStatement)
		self.writeEndOfCsd()
					
					
	def writeEndOfCsd(self):
		""" This method needs to be executed after the score has been
		processed. Otherwise, the produced .csd will be incomplete!!!
		"""
		self.outFile.write(csdComponents.endFile)
