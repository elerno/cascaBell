#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Normalize soundfiles in a folder, and write them to a new folder
# called normalized/

# Import Python modules
import contextlib
import os
import shutil
import sys
import wave
# Import user modules

def normalize():
	""" Normalizes a set of sound files to norm-To dB
	return		-->> 1
	"""
	# Get the names of the files in sortFolder.
	files	= os.listdir(folderToSort)
	# Make a directory for the renamed sorted files:
	dirname = folderToSort + 'normalized/'
	try:
		os.makedirs(dirname)
	except OSError:
		if os.path.exists(dirname):
			pass
		else:
			raise
	for singleFile in files:
		#Only work with .wav files
		if singleFile[-4:] == '.wav':
			inputFile = folderToSort + singleFile
			outfile = dirname + singleFile
			command = 'sox --norm={0} {1} {2}'.format(normalizeTo, inputFile,
														outfile)
		os.system(command)
	return 1


def inputCheck(argValues):
	""" Check whether the input data is valid. If not print usage
	information.
	argValues	---> a list of the scripts command-line parameters.
	"""
	return 1


# Check that the input parameters are valid. Get the name of the folder
# that contains the sound files and the sort type from the command-line
# arguments.
argValues		= sys.argv
inputCheck(argValues)
folderToSort	= argValues[1]
try:
	normalizeTo		= argValues[2]
except IndexError:
	normalizeTo = -3
	print 'Normalizing to -3dB'
# Exectue the script.
normalize()
