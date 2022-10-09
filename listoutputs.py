#!/usr/bin/env python3

import json
import os
import sys

qfile = sys.argv[1]

concolor = {
        'red': '\033[91m',
        'green': '\033[92m',
        'end': '\033[0m',
    }

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

    print('{result}{destination}'.format(
            result='[' + (concolor['green'] + '✓' + concolor['end'] if jobdone else concolor['red'] + '✗' + concolor['end']) + '] ',
            destination=destination,
        ))
