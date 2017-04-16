'''Generate the trace according to the Project's requirment'''
import os
import subprocess as sp
import numpy as np
import heapq as hq
from datetime import datetime
from datetime import timedelta

K = 64
B = 1024

class Job:
    def __init__(self):
        self.arrival_time = 0
        self.service_time = 0
        self.start_time = 0
        self.end_time = 0
        self.delay = 0
        self.wait = 0

def generate_trace_sjf(trace_file):
    '''Generate the trace with Shortest Job First queue'''
    global K
    global B
    origin = list()
    k_batch = K
    b_size = B
    num = k_batch * b_size
    now = 0.0
    # Arrival times and service times
    for i in range(num):
        job = Job()
        job.arrival_time = now
        # now += np.random.poisson(10.0)
        now += np.random.exponential(1/10.0)
        job.service_time = np.random.gamma(4, 0.02)
        origin.append(job)
    # print(origin)

    # Generate the trace
    trace = list()
    queue = list()
    i = 0
    now = 0.0
    while i < num:
        if len(queue) != 0:
            job = Job()
            job.service_time, job.arrival_time = hq.heappop(queue)
            # print('job:', 'job.service_time:', job.service_time,\
            #     'job.arrival_time:', job.arrival_time)#test
            # print('queue:')#test
            # print('++++++++++++++++++++++++++++++++++')
            # for j in queue:
            #     print('(st:{}, at:{})'.format(j[0],
            #         j[1]))#test
            # print('++++++++++++++++++++++++++++++++++')
        else:
            job = origin[i]
            i += 1
            now = job.arrival_time
        job.start_time = now
        job.end_time = job.start_time + job.service_time
        job.delay = job.start_time - job.arrival_time
        job.wait = job.end_time - job.arrival_time
        trace.append(job)
        now = job.end_time

        while i < num:
            job = origin[i]
            if job.arrival_time > now:
                break
            hq.heappush(queue, \
                (job.service_time, job.arrival_time))
            i += 1
    while len(queue) != 0:
        job = Job()
        job.service_time, job.arrival_time = hq.heappop(queue)
        job.start_time = now
        job.end_time = job.start_time + job.service_time
        job.delay = job.start_time - job.arrival_time
        job.wait = job.end_time - job.arrival_time
        trace.append(job)
        now = job.end_time

    # Save the origin
    with open(trace_file, 'w') as output:
        for job in trace:
            attris = list()
            attris.append(str(job.arrival_time))
            attris.append(str(job.service_time))
            attris.append(str(job.start_time))
            attris.append(str(job.end_time))
            attris.append(str(job.delay))
            attris.append(str(job.wait))
            line = ' '.join(attris)
            output.write(line + '\n')

def generate_trace_fcfs(trace_file):
    '''Generate the trace with First Come First Serve queue'''
    global K
    global B
    origin = list()
    k_batch = K
    b_size = B
    num = k_batch * b_size
    now = 0.0
    # Arrival times and service times
    for i in range(num):
        job = Job()
        job.arrival_time = now
        # now += np.random.poisson(10.0)
        now += np.random.exponential(1/10.0)
        job.service_time = np.random.gamma(4, 0.02)
        origin.append(job)
    # print(origin)

    # Generate the trace
    trace = list()
    queue = list()
    i = 0
    now = 0.0
    while i < num:
        if len(queue) != 0:
            job = queue.pop(0)
            # job = Job()
            # job.service_time, job.arrival_time = hq.heappop(queue)
            # print('job:', 'job.service_time:', job.service_time,\
            #     'job.arrival_time:', job.arrival_time)#test
            # print('queue:')#test
            # print('++++++++++++++++++++++++++++++++++')
            # for j in queue:
            #     print('(st:{}, at:{})'.format(j.service_time,
            #         j.arrival_time))#test
            # print('++++++++++++++++++++++++++++++++++')
        else:
            job = origin[i]
            i += 1
            now = job.arrival_time
        job.start_time = now
        job.end_time = job.start_time + job.service_time
        job.delay = job.start_time - job.arrival_time
        job.wait = job.end_time - job.arrival_time
        trace.append(job)
        now = job.end_time

        while i < num:
            job = origin[i]
            if job.arrival_time > now:
                break
            # hq.heappush(queue, \
            #     (job.service_time, job.arrival_time))
            queue.append(job)
            i += 1
    while len(queue) != 0:
        # job = Job()
        # job.service_time, job.arrival_time = hq.heappop(queue)
        job = queue.pop(0)
        job.start_time = now
        job.end_time = job.start_time + job.service_time
        job.delay = job.start_time - job.arrival_time
        job.wait = job.end_time - job.arrival_time
        trace.append(job)
        now = job.end_time

    # Save the origin
    with open(trace_file, 'w') as output:
        for job in trace:
            attris = list()
            attris.append(str(job.arrival_time))
            attris.append(str(job.service_time))
            attris.append(str(job.start_time))
            attris.append(str(job.end_time))
            attris.append(str(job.delay))
            attris.append(str(job.wait))
            line = ' '.join(attris)
            output.write(line + '\n')

def main():
    directory = 'outputs/'

    # SJF
    file_name = 'trace_sjf.csv'
    trace_file = directory + file_name
    # generate_trace_sjf(trace_file)

    # FCFS
    file_name = 'trace_fcfs.csv'
    trace_file = directory + file_name
    generate_trace_fcfs(trace_file)

if __name__ == '__main__':
    main()

