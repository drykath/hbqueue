#!/usr/bin/env python3

import json
import os
import sys

qfile = sys.argv[1]

with open(qfile) as f:
    # List of jobs in queue file
    data = json.load(f)

for job in data:
    destination = job['Job']['Destination']['File']

    # Remap Destination File
    filename = os.path.basename(destination)
    destination = os.path.join('/your/output/path', filename)
    print(destination)
