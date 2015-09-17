#!/usr/bin/env python

import json
import os
import re
import subprocess

from ansible.module_utils.basic import *

# Note: This module is called "repobackup", although in the moment it only does
# discovery. I kept the name because the end goal is to back up the repos this
# module detects.

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

def get_size(dirpath):
    p = subprocess.Popen(['du', '-s', '-h', '.'], stdout=subprocess.PIPE,
            cwd=dirpath)
    out, err = p.communicate()

    # Output is of the form
    # size path
    # , so we split.
    reposize = out.split()[0]
    return reposize

def main():
    module = AnsibleModule(
        argument_spec=dict(
            repodir     = dict(default=os.environ.get('HOME')),
        ),
    )

    repodir = module.params['repodir']
    if not os.path.isdir(repodir):
        module.fail_json(msg='Directory "%s" not found' % (repodir))

    repos = []
    for dirpath, dirnames, filenames in os.walk(repodir):
        isgit, bare, conform = is_git_repo(dirpath, dirnames, filenames)
        if isgit:
            reposize = get_size(dirpath)
            d = {
                    'path': dirpath,
                    'type': 'git',
                    'size': reposize,
                    'bare': bare,
                    'conform': conform
                    }
            repos.append(d)
        ishg, bare = is_hg_repo(dirpath, dirnames, filenames)
        if ishg:
            reposize = get_size(dirpath)
            d = {
                    'path': dirpath,
                    'type': 'hg',
                    'size': reposize,
                    'bare': bare,
                    'conform': 'n/a'
                    }
            repos.append(d)
    print json.dumps({
        'repos': repos
        })

main()
