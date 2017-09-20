#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from turkey import Task

apps = ['dedup']
app = apps[0]

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
        print('Job %d missing results' % i)
    else:
        print('%s,\t%s,\t%s' % (i, output['cache-misses'], output['time']))
