'''Get the record of waiting queue length, 
then get its distribution by the form of 
histogram.'''
import os
import subprocess as sp
import numpy as np
import heapq as hq
import statistics as stat
import scipy.stats as ss
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
from datetime import datetime
from datetime import timedelta

def do_queue_length(arrivals, departures, output):
    '''Generic function to calculate queue length'''
    i = 0
    j = 0
    queue_lengths = list()
    time_q = arrivals[0]
    i += 1
    length = 1
    while i < len(arrivals) and j < len(departures):
        if arrivals[i] < departures[j]:
            period = arrivals[i] - time_q
            queue_lengths.append([length, period])
            time_q = arrivals[i]
            length += 1
            i += 1
        elif departures[j] < arrivals[i]:
            period = departures[j] - time_q
            queue_lengths.append([length, period])
            time_q = departures[j]
            length -= 1
            j += 1
        else:
            i += 1
            j += 1
    while j < len(departures):
        period = departures[j] - time_q
        queue_lengths.append([length, period])
        time_q = departures[j]
        length -= 1
        j += 1

    # Calculate the mean queue length
    queue_record = list()
    precision = 1000
    length_v = 0.0
    count = 0
    for l, p in queue_lengths:
        # length_v += l * p
        p = int(p * precision)
        count += p
        if count > 1000000:
            print('.', end='', flush=True)
            count = count % 1000000
        record_v = [l for i in range(p)]
        queue_record.extend(record_v)

    # Save to file
    # with open(to_file, 'w') as output:
    for r in queue_record:
        output.write(str(r) + '\n')

def get_wait_queue_lengths(trace_file, to_file):
    with open(trace_file) as trace, \
        open(to_file, 'w') as output:
        arrival_times = list()
        start_times = list()
        for line in trace:
            attris = line.split()
            arv_t = float(attris[0])
            arrival_times.append(arv_t)
            stt_t = float(attris[2])
            start_times.append(stt_t)
        arrival_times.sort()
        start_times.sort()
        do_queue_length(arrival_times, start_times, output)

def get_histogram(record_file, to_file):
    with open(record_file) as record:
        queue_lengths = list()
        for line in record:
            length = int(line)
            queue_lengths.append(length)

    x = queue_lengths
    count = len(x)
    # k = math.floor(1 + math.log(count, 2))
    k = 13 # for SJF
    # k = 26 # for FIFO
    plt.figure(1)
    n, bins, patches = plt.hist(x, k, normed=True, edgecolor='k')
    print('bins:', bins)#test
    print('n:', n)#test
    print('k:', k)#test
    print('sum(n):', sum(n))#test

    plt.tick_params(direction='in')

    plt.xlabel('Waiting Queue Length')
    plt.ylabel('Probability')
    # fig_file = 'outputs/queue_dist.pdf'
    plt.savefig(to_file, format='pdf')

def main():
    directory = 'outputs/'
    # file_name = 'trace_sjf.csv'
    file_name = 'trace_fcfs.csv'
    trace_file = directory + file_name

    file_name = 'queue_dist_sjf.csv'
    # file_name = 'queue_dist_fcfs.csv'
    record_file = directory + file_name
    # get_wait_queue_lengths(trace_file, record_file)

    file_name = 'queue_hist_sjf.pdf'
    # file_name = 'queue_hist_fcfs.pdf'
    figure_file = directory + file_name
    get_histogram(record_file, figure_file)

if __name__ == '__main__':
    main()