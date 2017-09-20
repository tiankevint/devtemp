#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

import sys

from turkey import Task,apps

if len(sys.argv) < 3:
    print('Usage: %s [app] [threads]' % (sys.argv[0]))
    exit(-1)

app = sys.argv[1]

if not(app in apps):
    print('invalid app')
    exit(-1)

threads = int(sys.argv[2])
if threads < 0:
    threads = 1 # probably wrong

instances = 16
threads = 256

conf = 'native'

outpath = os.path.join('out', '%s_%d_t%d' % (app, instances, threads))

task_args = {
    'app': app,
    'conf': conf,
    'threads': threads,
    'mode': 'pthread',
    'diagnostic': 'perf'
}

print('Preparing tasks')

tasks = [Task(task_args, out_dir = outpath) for i in xrange(instances)]

print('Starting instances (%d)' % instances)

processes = [task.run(wait=False, verbose=False) for task in tasks]

print('All instances started')

exitcodes = [p.wait() for p in processes]

print('All instances completed')

errs = [(i,exitcodes[i]) for i in xrange(instances) if exitcodes[i] != 0]

for (i, code) in errs:
    print('Job %d exited with return code %d' % (i, code))

results = dict()

with open('out%d' % threads, 'w') as out:
    for i in xrange(instances):
        output = dict()
        results[i] = output
        fpath = os.path.join(outpath, '%d' % i, 'task.out')
        with open(fpath) as f:
            for l in f:
                if l.find('cache-misses') > -1:
                    output['cache-misses'] = l.split()[0]
                if l.find('seconds time elapsed') > -1:
                    output['time'] = l.split()[0]

        if not('cache-misses' in output) or not('time' in output):
            out.write('Job %d missing results\n' % i)
        else:
            out.write('%s,\t%s,\t%s\n' % (i, output['cache-misses'], output['time']))
