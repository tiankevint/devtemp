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

processes = [None] * instances

print('Starting instances... (%d)' % instances)

# Let them go
for i in xrange(instances):
    task = Task(task_args, out_dir = outpath)
    print('\tstarting process %d of %d' % (i, instances))
    processes[i] = task.run(wait=False, verbose=False)

exitcodes = [p.wait() for p in processes]

print('Instances completed')
print(exitcodes)

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
        print('%d missing results' % i)
    else:
        print('%s,\t%s,\t%s' % (i, output['cache-misses'], output['time']))
