'''Calculate Autocorrelation of Inter-departure Time'''
import os
import subprocess as sp
import numpy as np
from datetime import datetime
from datetime import timedelta

def get_autocor_departure(trace_path, output_file):
    J_MAX = 1000
    # J_MAX = 5
    with open(trace_path) as trace, \
        open(output_file, 'w') as output:
        # Read all inter-departure time into a list
        inter_depart_times = list()
        count = 0
        for line in trace:
            count += 1
            if count == 1:
                continue
            attris = line.split()
            inter_depart_t = float(attris[7])
            inter_depart_times.append(inter_depart_t)
            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

        # Calculate mean and c0 (variance)
        n = len(inter_depart_times)
        inter_depart_times_mean = sum(inter_depart_times)/n
        c0_v = 0.0
        count = 0
        for idt in inter_depart_times:
            c0_v += (idt - inter_depart_times_mean)**2
        c0 = c0_v/n

        # Calculate autocorrelations
        autocors = list()
        for j in range(1, J_MAX + 1):
            cj_v = 0.0
            for i in range(n - j):
                cj_v += \
                    (inter_depart_times[i] - inter_depart_times_mean)\
                    *(inter_depart_times[i+j] - inter_depart_times_mean)
            cj = cj_v / (n - j)
            rj = cj / c0
            autocors.append(str(rj))
            print('.', end='', flush=True)
        print('', flush=True)

        # Write to the record file
        line = ' '.join(autocors)
        output.write(line + '\n')

def main():
    from_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_departure/'
    # file_name = 'examples_times.csv'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    trace_path = from_direct + file_name

    to_direct = 'outputs/'
    file_name = 'inter-depart_time_autocor.txt'
    output_file = to_direct + file_name

    get_autocor_departure(trace_path, output_file)

if __name__ == '__main__':
    main()

