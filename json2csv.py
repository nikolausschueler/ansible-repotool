#!/usr/bin/python

import csv
import json
import sys

w = csv.writer(open('results.csv', 'w'))

s = sys.stdin.read()
repos = json.loads(s)
for r in repos[:1]:
    header = list()
    for k in r.keys():
        header.append(k)
    w.writerow(header)
for r in repos:
    row = list()
    for k, v in r.iteritems():
        row.append(v)
    w.writerow(row)


