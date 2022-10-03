#!/usr/bin/env python3

import datetime
import glob
import json
import os
import random
import sys
import time

pid = os.getpid()

while True:
    candidates = []
    qfile_map = {}

    qlist = glob.glob('/your/input/path/*/*.json')

    for qfile in qlist:
        with open(qfile) as f:
            # List of jobs in queue file
            data = json.load(f)

        for job in data:
            destination = job['Job']['Destination']['File']

            # Remap Destination File
            filename = os.path.basename(destination)
            destination = os.path.join('/your/output/path', filename)
            job['Job']['Destination']['File'] = destination

            # Skip job if we've already done it/are doing it
            if os.path.exists(destination):
                continue

            source = job['Job']['Source']['Path']

            # Add map entry for later reference
            qfile_map[source] = qfile

            # Ignore if the file isn't present here, as we can't do anything (yet)
            if not os.path.exists(source):
                # Also look "next to" the queue file, in case the directory was moved
                source = os.path.join(os.path.dirname(qfile), os.path.basename(source))
                job['Job']['Source']['Path'] = source
                qfile_map[source] = qfile
                if not os.path.exists(source):
                    continue

            candidates.append(job)

    if candidates:
        #job = random.choice(candidates)
        # Probably better to do it in a deterministic fashion
        job = candidates[0]

        # Write out this job to a temp file
        with open('hbq.json', 'w') as f:
            json.dump([job], f)

        # Write out a little status note
        qfile_target = qfile_map[job['Job']['Source']['Path']]
        qfile_name = os.path.splitext(qfile_target)[0]
        with open(qfile_name + '.' + str(pid) + '.doing', 'w') as f:
            f.write(job['Job']['Source']['Path'])

        procstart = datetime.datetime.now()
        os.system('HandBrakeCLI --queue-import-file hbq.json')
        procend = datetime.datetime.now()

        # Fuse
        if procend - procstart < datetime.timedelta(seconds=15):
            print('I think something is wrong')
            sys.exit(2)

        os.unlink(qfile_name + '.' + str(pid) + '.doing')

        # Analyze the map file to figure out what we still need to do
        with open(qfile_name + '.todo', 'w') as f:
            for source, qfile in qfile_map.items():
                # Assume the job we just ran is successful
                if source == job['Job']['Source']['Path']:
                    continue

                # If we find a different source in the same queue file, note it down
                if qfile == qfile_target:
                    f.write(source + '\n')

    else:
        print('Bored...')
        time.sleep(60)
