import os
import subprocess

apps = [
    'dedup', 'swaptions'
]

iterations = 1
core_counts = [8,16,32,64]
#threads = [1, 2, 4, 8, 12, 16, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64]

def get_output_path(app, cores, threads, iteration):
    return os.path.join('out/%s_c%d_n%d_i%d' % (app, cores, threads, iteration))


def get_args(app, cores, threads, iteration, conf='native'):
    args = 'taskset -c 0-%(cores)d ./bin/run.py one %(app)s -n %(thread)d -c %(conf)s -o %(outputs)s' % {
        'app': app,
        'cores': cores-1,
        'thread': threads,
        'outputs': get_output_path(app, cores, threads, iteration),
        'conf': conf
    }

    return args.split()


if __name__ == '__main__':
    for app in apps:
        for cores in core_counts:
            for i in xrange(iterations):
                # number of threads = number of cores
                threads = cores
                args = get_args(app, cores, threads, i)
                #print(' '.join(args))
                subprocess.call(args)
