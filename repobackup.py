#!/usr/bin/env python

import json
import os

repos = []
for dirpath, dirnames, filenames in os.walk(os.path.join(os.environ.get('HOME'),
    'repo')):
    if '.git' in dirnames:
        repos.append(dirpath)
print json.dumps({
    'repos': repos
    })
