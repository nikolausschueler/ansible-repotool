#!/usr/bin/env python

import json
import os
import re

# Check if repo is a git repo and return this fact and additional info.
#
# Returns:
#   bool: Is it a git repo?
#   bool: Is it bare?
#   bool: Does it conform to the Git convention that bare repos end on .git?
def is_git_repo(dirpath, dirnames, filenames):
    if '.git' in dirnames:
        return True, True, True
    isgit = False
    bare = False
    conform = False
    if 'config' in filenames:
        f = open(os.path.join(dirpath, 'config'), 'r')
        for line in f.readlines():
            if re.match('.*bare\s+=\s+true.*', line):
                isgit = True
                bare = True
        filename, extension = os.path.splitext(dirpath)
        if extension == '.git':
            conform = True
    return isgit, bare, conform

repos = []
for dirpath, dirnames, filenames in os.walk(os.path.join(os.environ.get('HOME'),
    'repo')):
    isgit, bare, conform = is_git_repo(dirpath, dirnames, filenames)
    if isgit:
        d = {
                'path': dirpath,
                'isgit': isgit,
                'bare': bare,
                'conform': conform
                }
        repos.append(d)
print json.dumps({
    'repos': repos
    })
