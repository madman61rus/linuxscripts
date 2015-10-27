#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import os


def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t','--time', nargs = '?', default ='+0')	# The minimum age of file to search
	parser.add_argument('-s','--size', nargs = '?', default = '+0')	# Minimum size of the file to search
	parser.add_argument('-n','--name', nargs = '+' , required = True , help = 'Name of a file to check')			# File name
	parser.add_argument('-w','--where', nargs = '+' , required =True , help = 'Path to a file to check')			# Directory where shell we look for the file 
	parser.add_argument('-a', '--all_content',required = False, help = 'All directory should contain a file')

	return (parser)

def setParameters (all_content,size,time,name,where):
	return {
	'all-content': all_content,
	'size': size,
	'time': time,
	'name': name,
	'where': where
	 }

#
# Main
#

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])

	parameters = setParameters(
		namespace.all_content,
		namespace.size,
		namespace.time,
		namespace.name,
		namespace.where[0]
		)

	listOfDirs = []

	for dirName in os.walk(unicode(parameters['where'],'utf-8')):
		listOfDirs.append({ 'path': dirName[0],'files': dirName[2] })

	for path in listOfDirs[1:]:
		if parameters['name'][0] in path['files']:
			print path['path']
		else:
			print unicode(str(parameters['name']),'utf-8')

	


