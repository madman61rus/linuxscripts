#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from datetime import datetime
from os.path import getmtime
from os.path import getsize


def createParser():
    parser = argparse.ArgumentParser()
    # The minimum age of file to searc
    parser.add_argument('-t', '--time', nargs='?', default='+0')
    # Minimum size of the file to search
    parser.add_argument('-s', '--size', nargs='?', default='+0')
    parser.add_argument('-n', '--name', nargs='+',  # File name
                        required=True, help='Name of a file to check')
    # Directory where shell we look for the file
    parser.add_argument(
        '-w', '--where', nargs='+',
        required=True, help='Path to a file to check')
    parser.add_argument('-a', '--allContent',
                        required=False,
                        help='All directory should contain a file')

    return (parser)


def setParameters(allContent, size, time, name, where):

    return {
        'allContent': allContent,
        'size': int(size),
        'time': int(time),
        'name': "".join(name),
        'where': "".join(where),
        'counter': 0,
        'allCounter': 0,
        'sizeCounter': 0,
        'lastTimeOfFile': datetime(2015, 01, 01, 0, 0),
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
        namespace.where,
    )

    listOfDirs = []
    listWithout = []

    for dirName in os.walk(unicode(parameters['where'], 'utf-8')):

        parameters['allCounter'] += 1

        if parameters['name'] in dirName[2]:

            file = {
                'pathToFile': dirName[0],
                'filesInPath': dirName[2],
                'timeOfFile': datetime.fromtimestamp(
                        getmtime(dirName[0] + "/" + parameters['name'])),
                'sizeOfFile': getsize(dirName[0] + "/" + parameters['name']),
            }
            parameters['counter'] += 1
            listOfDirs.append(file)

            if parameters['lastTimeOfFile'] < file['timeOfFile']:
                parameters['lastTimeOfFile'] = file['timeOfFile']
            if parameters['sizeCounter'] < file['sizeOfFile']:
                parameters['sizeCounter'] = file['sizeOfFile']
        else:

            listWithout.append(dirName[0])
    
    if (parameters['allContent'] == 'True') and not \
       (parameters['allCounter'] == parameters['counter']):
        print 'WARNING !!! In '+"and".join(listWithout)+" file is not exist"
        sys.exit(1)

    if (((datetime.now()
       - parameters['lastTimeOfFile']).days) > parameters['time']):
        print "ALERT ! The last file %s was written %i day(s) ago." % \
            ("".join(parameters['name']),
             (datetime.now() - parameters['lastTimeOfFile']).days)
        sys.exit(2)
    elif (parameters['sizeCounter'] < parameters['size']):
        print "WARNING ! The size of file is %i" % parameters['sizeCounter']
        sys.exit(1)
    else:
        print "OK. The last file %s was written %i day(s) ago." % \
         ("".join(parameters['name']),
          (datetime.now() - parameters['lastTimeOfFile']).days)
        sys.exit(0)

