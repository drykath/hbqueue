#!/usr/bin/env python3

import glob
import json
import os
import sys

if len(sys.argv) > 1:
    qlist = [sys.argv[1]]
else:
    qlist = glob.glob('/your/input/path/*/*.json')

concolor = {
        'red': '\033[91m',
        'green': '\033[92m',
        'end': '\033[0m',
    }

for qfile in qlist:
    with open(qfile) as f:
        # List of jobs in queue file
        data = json.load(f)

    for job in data:
        destination = job['Job']['Destination']['File']
        jobdone = False

        # Remap Destination File
        filename = os.path.basename(destination)
        destination = os.path.join('/your/output/path', filename)
        if os.path.exists(destination):
            jobdone = True

        try:
            print('{result}{destination}'.format(
                    result='[' + (concolor['green'] + '✓' + concolor['end'] if jobdone else concolor['red'] + '✗' + concolor['end']) + '] ',
                    destination=destination,
                ))
        except (BrokenPipeError, IOError):
            sys.exit(0)
