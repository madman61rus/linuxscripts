#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import datetime


def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t','--time', nargs = '?', default ='+0')	# The minimum age of file to search
	parser.add_argument('-s','--size', nargs = '?', default = '+0')	# Minimum size of the file to search
	parser.add_argument('-n','--name', nargs = '+' , required = True , help = 'Name of a file to check')			# File name
	parser.add_argument('-w','--where', nargs = '+' , required =True , help = 'Path to a file to check')			# Directory where shell we look for the file 
	parser.add_argument('-a', '--allContent',required = False, help = 'All directory should contain a file')

	return (parser)

def setParameters (allContent,size,time,name,where):

	return {
	'all-content': allContent,
	'size': size,
	'time': int(time),
	'name': name,
	'where': where,
	'counter': 0,
	'counterPaths': 0,
	'pathes': [],
	'dateTimeOfFile': datetime.datetime(2015,01,01,0,0),
	 }

#
# Main
#

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])

	parameters = setParameters(
		namespace.allContent,
		namespace.size,
		namespace.time,
		namespace.name,
		namespace.where[0],
		)

	listOfDirs = []

	for dirName in os.walk(unicode(parameters['where'],'utf-8')):
		listOfDirs.append({ 'path': dirName[0],'files': dirName[2] })

	for path in listOfDirs[1:]:

		parameters['counterPaths'] += 1

		if ''.join(parameters['name']) in path['files']:
			parameters['counter'] += 1
			parameters['pathes'].append(path['path'])
			lastModifiedDate = datetime.datetime.fromtimestamp(os.path.getmtime(path['path'] + "/" + ''.join(parameters['name'])))
			if parameters['dateTimeOfFile'] < lastModifiedDate :
				parameters['dateTimeOfFile'] = lastModifiedDate
	

	if (((datetime.datetime.now() - parameters['dateTimeOfFile']).days) > parameters['time'] ):
			print "Oooooops  %i" % (datetime.datetime.now() - parameters['dateTimeOfFile']).days
	else:
			print "It's OK %i" % (datetime.datetime.now() - parameters['dateTimeOfFile']).days

