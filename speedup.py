#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from turkey import Task

apps = [
    'dedup'#, 'swaptions'
]

iterations = 1
core_counts = [8, 16, 32, 64]
#threads = [1, 2, 4, 8, 12, 16, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64]

conf = 'simdev'

def get_output_path(app, cores, threads, iteration):
    return os.path.join('out', '%s_c%d_n%d_i%d' % (app, cores, threads, iteration))

if __name__ == '__main__':
    # data collections
    results = dict()

    taskcounter = -1

    for app in apps:
        results[app] = dict()
        for cores in core_counts:
            results[app][cores] = dict()
            for i in xrange(iterations):
                output = dict()
                results[app][cores][i] = output

                taskcounter  = taskcounter+1

                # number of threads = number of cores
                threads = cores

                task_args = {
                    'app': app,
                    'conf': conf,
                    'threads': threads,
                    'taskset': '0-%d' % (cores-1),
                    'mode': 'pthread',
                    'diagnostic': 'perf'
                }

                outpath = get_output_path(app, cores, threads, 0)

                task = Task(task_args, out_dir = outpath)
                task.run(wait=True, verbose=False)

                fpath = os.path.join(outpath, '%d' % taskcounter, 'task.out')

                f = open(fpath)
                for l in f:
                    if l.find('cache-misses') > -1:
                        output['cache-misses'] = l.split()[0]
                    elif l.find('seconds time elapsed') > -1:
                        output['time'] = l.split()[0]

                print('%s,\t%d,\t%d,\t%s,\t%s' % (app, cores, i, output['cache-misses'], output['time']))
