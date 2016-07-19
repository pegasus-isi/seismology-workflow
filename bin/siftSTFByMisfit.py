#!/usr/bin/python
#
import sys, os, time, tarfile
from stat import *
#
# Dependency: pysacio
#
import pysacio
#
# USAGE:
#
#  siftSTFByMisfit myfile*z (UNIX wildcards work)
#
###############################################################
#
# this script reads in a SAC file and extracts the percent of
#   the signal power that is fit (stored in the SAC user5
#   file header value) and makes a list suitable for a shell
#   script to move the poorly fitting data into a subdirectory.
#
################################################################
#
#  build the file list
#
d = os.getcwd() # get the directory name
#
if len(sys.argv) > 1:
	if sys.argv[1] == '-h':
	    print '     usage: plh [myfile*?[z,r,t]]'
	    files = ''
	else:
		files = sys.argv #python expands wildcards for us
		del files[0] #delete the script name from the list
else:
	files = os.listdir(d) # default is to look at all files
#
#  this is the loop over files the above just creates a list
#     of files.
#

tar = tarfile.open('good-fits.tar.gz', 'w:gz')

for fname in files:
	#
	# here's where the SAC File is read in
	#
	[hf, hi, hs, ok] = pysacio.ReadSacHeader(fname)
	#
	# store values for the table
	#
	if ok:
		#   Get the msifit and list a mv command if
		#   the file does not fit 85% of the signal power
		q = pysacio.GetHvalue('user5',hf, hi, hs)
		if q >= 85:
			tar.add(fname)

tar.close()
#
