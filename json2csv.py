#!/usr/bin/python

import csv
import json
import sys

w = csv.DictWriter(sys.stdout, ['conform', 'path', 'bare', 'type'])

s = sys.stdin.read()
repos = json.loads(s)
w.writeheader()
for r in repos:
    w.writerow(r)


