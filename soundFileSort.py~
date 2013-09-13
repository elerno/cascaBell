#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Sort the soundfiles in a folder, renaming by number. Optionally, add a
# suffix to the new filename.

# Import Python modules
import contextlib
import os
import shutil
import sys
import wave
# Import user modules

def length(sortType, suffix):
	""" Sorts the sound files by length, creates a new directory called
	sorted, and writes renamed files 01.wav, 02.wav, etc.
	sortType	---> a string determining ascending or descending order
	suffix		---> a string to attach to the end of the filenames
	return		-->> 1
	"""
	# Get the names of the files in sortFolder.
	files	= os.listdir(folderToSort)
	# Check that the sample rate in all files is the same. If not,
	# return an error and exit.
	# Create a dictionary of key=duration value=filename.
	durationFilenameDict = {}
	for filename in files:
		#Only work with .wav files
		if filename[-4:] == '.wav':
			with contextlib.closing(wave.open(folderToSort + filename,'r')) as f:
				frames = f.getnframes()
				rate = f.getframerate()
				duration = frames/float(rate)
				durationFilenameDict[str(duration)] = filename
	# Make a directory for the renamed sorted files:
	dirname = folderToSort + 'sorted/'
	try:
		os.makedirs(dirname)
	except OSError:
		if os.path.exists(dirname):
			pass
		else:
			raise
	sortedKeys = sorted(durationFilenameDict)
	# Apply the sort order to the keys.
	if sortType == 'descending':
		sortedKeys.reverse()
	order = len(str(len(sortedKeys)))
	counter = 1
	# Write copies of the files with their new names in dirname/.
	for key in sortedKeys:
		newName = str(counter)
		while len(newName) < order:
			newName = '0' + newName
		newName += suffix + '.wav'
		originalFile = folderToSort + durationFilenameDict[key]
		newFile = dirname + newName
		print newFile
		shutil.copy2(originalFile,newFile)
		counter += 1
	return 1


def inputCheck(argValues):
	""" Check whether the input data is valid. If not print usage
	information.
	argValues	---> a list of the scripts command-line parameters.
	"""
	# Check that the input parameters are complete. If not, raise an
	# error.
	firstPart = False
	if len(argValues) > 4:
		firstPart = 'Too many arguments.'
	elif len(argValues) < 4:
		firstPart = 'Too few arguments.'
	if firstPart:
		print """{0} This script takes exactly three arguments: a path to the folder containing the .wav files, a sort type (ascending or desceding) and a suffix to attach to the end of the filenames.
Example:
python soundFileSort.py path/contentFolder/ ascending vlc
		""".format(firstPart)
		sys.exit()
	# Check that the sort type is valid. If not, raise an error.

	if argValues[2] == 'ascending':
		print argValues[2]
	if argValues[2] == 'ascending' or argValues[2] == 'descending':
		pass
	else:
		raise RuntimeError('Invalid sortType. Possible sortTypes are \'ascending\' or \'descending\'')
	return 1


# Check that the input parameters are valid. Get the name of the folder
# that contains the sound files and the sort type from the command-line
# arguments.
argValues		= sys.argv
inputCheck(argValues)
folderToSort	= argValues[1]
sortType		= argValues[2]
suffix			= argValues[3]
# Exectue the script.
length(sortType, suffix)
