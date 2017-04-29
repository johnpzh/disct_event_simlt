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
        self.arrival_time = -1
        self.service_time = -1
        self.start_time = -1
        self.end_time = -1
        self.delay = -1
        self.wait = -1
        self.inter_arrival_time = -1
        # self.queue = -1 # the number of jobs in the queue when the job starts

def generate_trace_sjf(output_file):
# def generate_trace_sjf(trace_file, output_file):
    '''Generate the trace with Shortest Job First queue'''
    global K
    global B
    # origin = list()
    k_batch = K
    b_size = B
    num = k_batch * b_size
    now = 0.0
    arrival_time_q = 0.0
    arv_t = 0
    RANGE = 20

    # Arrival times and service times
    origin = list()
    # with open(trace_file) as trace:
    #     count = 0
    #     for line in trace:
    #         job = Job()
    #         attris = line.split()
    #         job.arrival_time = float(attris[0])
    #         job.service_time = np.random.gamma(4, 0.02)
    #         origin.append(job)
    #         count += 1
    #         # if count == 1:
    #         #     job.inter_arrival_time = 0
    #         # else:
    #         #     job.inter_arrival_time = job.arrival_time - arrival_time_q
    #         # arrival_time_q = job.arrival_time
    #         job.inter_arrival_time = float(attris[4])
    #         if count == num:
    #             break
    
    for i in range(num):
        job = Job()
        job.arrival_time = now
        # now += np.random.poisson(10.0)
        # now += np.random.exponential(1/10.0)
        arv_t = arv_t % (RANGE - 1) + 1
        now += arv_t / 100
        job.service_time = np.random.gamma(4, 0.02)
        job.inter_arrival_time = job.arrival_time - arrival_time_q
        arrival_time_q = job.arrival_time
        origin.append(job)
    # print(origin)

    # Generate the trace
    trace = list()
    queue = list()
    i = 0
    while i < num:
        if len(queue) != 0:
            job = Job()
            job.service_time, \
                job.arrival_time, \
                job.inter_arrival_time = hq.heappop(queue)
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
                (job.service_time, \
                job.arrival_time, \
                job.inter_arrival_time))
            i += 1
    while len(queue) != 0:
        job = Job()
        job.service_time, \
            job.arrival_time, \
            job.inter_arrival_time = hq.heappop(queue)
        job.start_time = now
        job.end_time = job.start_time + job.service_time
        job.delay = job.start_time - job.arrival_time
        job.wait = job.end_time - job.arrival_time
        trace.append(job)
        now = job.end_time

    # Save the origin
    with open(output_file, 'w') as output:
        for job in trace:
            attris = list()
            attris.append(str(job.arrival_time))
            attris.append(str(job.service_time))
            attris.append(str(job.start_time))
            attris.append(str(job.end_time))
            attris.append(str(job.delay))
            attris.append(str(job.wait))
            attris.append(str(job.inter_arrival_time))
            # attris.append(str(job.queue))
            line = ' '.join(attris)
            output.write(line + '\n')

def generate_trace_fifo(trace_file):
    '''Generate the trace with First Come First Serve queue'''
    global K
    global B
    origin = list()
    k_batch = K
    b_size = B
    num = k_batch * b_size
    now = 0.0
    arrival_time_q = 0.0
    arv_t = 0
    RANGE = 20
    # Arrival times and service times
    # for i in range(num):
    #     job = Job()
    #     job.arrival_time = now
    #     # now += np.random.poisson(10.0)
    #     now += np.random.exponential(1/10.0)
    #     job.service_time = np.random.gamma(4, 0.02)
    #     origin.append(job)
    # print(origin)

    for i in range(num):
        job = Job()
        job.arrival_time = now
        # now += np.random.poisson(10.0)
        # now += np.random.exponential(1/10.0)
        arv_t = arv_t % (RANGE - 1) + 1
        now += arv_t / 100
        job.service_time = np.random.gamma(4, 0.02)
        job.inter_arrival_time = job.arrival_time - arrival_time_q
        arrival_time_q = job.arrival_time
        origin.append(job)

    # Generate the trace
    trace = list()
    queue = list()
    i = 0
    now = 0.0
    while i < num:
        if len(queue) != 0:
            job = queue.pop(0)
        else:
            job = origin[i]
            i += 1
            now = job.arrival_time
        job.start_time = now
        job.end_time = job.start_time + job.service_time
        job.delay = job.start_time - job.arrival_time
        job.wait = job.end_time - job.arrival_time
        # job.queue = len(queue)
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
        # job.queue = len(queue)
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
            attris.append(str(job.inter_arrival_time))
            # attris.append(str(job.queue))
            line = ' '.join(attris)
            output.write(line + '\n')

def main():
    directory = 'outputs/'

    # SJF
    file_name = 'trace_sjf.csv'
    output_file = directory + file_name

    # trace_file = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/duplicated/UCB-duplicated.csv'
    # generate_trace_sjf(trace_file, output_file)
    # generate_trace_sjf(output_file)

    # FCFS
    file_name = 'trace_fifo.csv'
    trace_file = directory + file_name
    generate_trace_fifo(trace_file)

if __name__ == '__main__':
    main()

