#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Sort the soundfiles in a folder, renaming by number. Optionally, add a
# suffix to the new filename.

# Import Python modules
import contextlib
import os
import sys
import wave
# Import user modules


# Get the name of the folder that contains the sound files and the sort
# type from the command-line arguments.
argValues		= sys.argv
folderToSort	= argValues[1]
sortType		= argValues[2]


def length(sortType):
	""" Sorts the sound files by length.
	sortType	---> a string determining ascending or descending order
	return		-->> 1
	"""
	# Check that the sort type is valid. If not, raise an error.
	if sortType == 'ascending' or sortType == 'descending':
		pass
	else:
		raise RuntimeError('Invalid sortType. possible sortTypes are \'ascending\' or \'descending\'')
	# Get the names of the files in sortFolder.
	files	= os.listdir(folderToSort)
	# Check that the sample rate in all files is the same. If not,
	# return an error and exit.
	for filename in files:
		#Only work with .wav files
		if filename[-4:] == '.wav':
			with contextlib.closing(wave.open(folderToSort + filename,'r')) as f:
				frames=f.getnframes()
				rate=f.getframerate()
				duration=frames/float(rate)
				print filename +' = ' + str(duration)
	# Create a dictionary with key=duration and entry=filename.
	
	# Loop the dictionary by key (ascending or descending), and rename
	# the files according to a counter.
	
	return 1
	
# Exectue the script.
length(sortType)
