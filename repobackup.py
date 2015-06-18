#!/usr/bin/env python

import json
import os

def is_git_repo(dirpath, dirnames, filenames):
    if '.git' in dirnames:
        return True

repos = []
for dirpath, dirnames, filenames in os.walk(os.path.join(os.environ.get('HOME'),
    'repo')):
    if is_git_repo(dirpath, dirnames, filenames):
        repos.append(dirpath)
print json.dumps({
    'repos': repos
    })
