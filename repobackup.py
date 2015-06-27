#!/usr/bin/env python

import json
import os
import re
import subprocess

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

def is_hg_repo(dirpath, dirnames, filenames):
    ishg = False
    bare = False
    if '.hg' in dirnames:
        ishg = True
        try:
            p = subprocess.Popen(['hg', 'id'], stdout=subprocess.PIPE,
                    cwd=dirpath)
            out, err = p.communicate()
            if '000000000000' in out:
                bare = True
        except OSError:
            bare = 'undefined'
    return ishg, bare

repos = []
for dirpath, dirnames, filenames in os.walk(os.path.join(os.environ.get('HOME'),
    'repo')):
    isgit, bare, conform = is_git_repo(dirpath, dirnames, filenames)
    if isgit:
        d = {
                'path': dirpath,
                'type': 'git',
                'bare': bare,
                'conform': conform
                }
        repos.append(d)
    ishg, bare = is_hg_repo(dirpath, dirnames, filenames)
    if ishg:
        d = {
                'path': dirpath,
                'type': 'hg',
                'bare': bare,
                'conform': 'n/a'
                }
        repos.append(d)
print json.dumps({
    'repos': repos
    })
