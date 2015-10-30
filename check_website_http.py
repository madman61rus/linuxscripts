#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import urllib2
import sys

def createParser():
    parser = argparse.ArgumentParser()
    # The Address of a site
    parser.add_argument('-a', '--address', nargs='?')
    # The phrase to search
    parser.add_argument('-p', '--phrase', nargs='?')

    return (parser)


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    try:
        site = urllib2.urlopen(namespace.address)
        responce = site.read()

    except urllib2.URLError as e:
        print (" WARNING ! Error {}").format(e.reason)
        sys.exit(1)

    except urllib2.HTTPError as e:
        print (" WARNING ! Error {}").format(e.reason)
        sys.exit(1)

    else:

        if namespace.phrase in responce:
            print ('OK ! The site is online ')
            sys.exit(0)
        else:
            print ('ALERT ! The site is down')
            sys.exit(2)
