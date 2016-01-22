#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import datetime
from time import localtime


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time', nargs='?',
                        default='+0')  # The minimum age of file to search
    parser.add_argument('-s', '--size', nargs='?',
                        default='+0')  # Minimum size of the file to search
    parser.add_argument('-n', '--name', nargs='+',
                        required=True,
                        help='Name of a file to check')			# File name
    parser.add_argument('-w', '--where', nargs='+',
                        required=True,
                        # Directory where look for
                        help='Path where we\'ll check')
    parser.add_argument('-a', '--allContent', required=False,
                        help='All directory should contain a file')

    return (parser)


def setParameters(allContent, size, time, name, where):
        return {
            'allContent': allContent,
            'size': size,
            'time': int(time),
            'name': name,
            'where': where,
            'counter': 0,
            'counterPaths': 0,
            'pathes': [],
            'pathesWithout': [],
            'dateTimeOfFile': datetime.datetime(2015, 01, 01, 0, 0),
        }


def search_file(filename, search_path, pathsep=os.pathsep):
    for path in search_path.split(pathsep):
        candidate = os.path.join(path, filename)
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)
    return None

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

    findfile = search_file(parameters['name'][0], parameters['where'])

    if (findfile):
    	now = datetime.datetime.now() 
        filedate = datetime.datetime.fromtimestamp(os.path.getmtime(findfile))   
        delta = (now - filedate).days
        if (delta <= parameters['time']):
            print ( 'Ok. File is exist and its age is %d day(s)' % delta )
        else:
        	print ('ALERT ! File age is %d day(s)' % delta )
    else:
        print ("ALERT ! File not found")
