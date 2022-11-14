#!/usr/bin/env python3

import glob
import json
import os
import sys

concolor = {
        'red': '\033[91m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'end': '\033[0m',
    }

filestates = {
        'todo': concolor['red'] + '✗' + concolor['end'],
        'doing': concolor['blue'] + '→' + concolor['end'],
        'done': concolor['green'] + '✓' + concolor['end'],
    }

# Files I think might be in progress
inprogress = []

doinglist = glob.glob('/your/input/path/*/*.*.doing')
for doingfile in doinglist:
    with open(doingfile) as f:
        inprogress.append(f.read())

if len(sys.argv) > 1:
    qlist = [sys.argv[1]]
else:
    qlist = glob.glob('/your/input/path/*/*.json')

for qfile in qlist:
    with open(qfile) as f:
        # List of jobs in queue file
        data = json.load(f)

    for job in data:
        destination = job['Job']['Destination']['File']
        jobstate = 'todo'

        # Remap Destination File
        filename = os.path.basename(destination)
        destination = os.path.join('/your/output/path', filename)
        if os.path.exists(destination):
            jobstate = 'done'

            # But it might actually be in progress
            source = job['Job']['Source']['Path']
            localsource = os.path.join(os.path.dirname(qfile), os.path.basename(source))
            if source in inprogress or localsource in inprogress:
                jobstate = 'doing'

        try:
            print('{result}{destination}'.format(
                    result='[' + filestates[jobstate] + '] ',
                    destination=destination,
                ))
        except (BrokenPipeError, IOError):
            sys.exit(0)
