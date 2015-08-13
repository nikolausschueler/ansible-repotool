#!/usr/bin/python

import csv
import json
import sys

w = csv.DictWriter(sys.stdout, ['path', 'type', 'size', 'bare', 'conform'])

s = sys.stdin.read()
repos = json.loads(s)
w.writeheader()
for r in repos:
    w.writerow(r)


