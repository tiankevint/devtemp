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

# Let them go
for i in xrange(instances):
    task = Task(task_args, out_dir = outpath)
    task.run(wait=False, verbose=False)
