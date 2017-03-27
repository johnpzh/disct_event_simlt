'''Calculate Inter-departure Time and add it into the trace'''
import os
import subprocess as sp
import numpy as np
from datetime import datetime
from datetime import timedelta

def get_departure_trace(trace_path, generated):
    '''Calculate Inter-departure Time and get the new trace'''
    with open(trace_path) as trace, \
        open(generated, 'w') as output:
        count = 0
        # Sort the old trace according to Service End Time
        trace_new = list()
        for line in trace:
            count += 1
            attris = line.split()
            trace_new.append(attris)
            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

        # Sort
        trace_new.sort(key=lambda record: record[2])

        #Calculate Inter-departure Time
        count = 0
        for attris in trace_new:
            count += 1
            if count == 1:
                end_time_q = float(attris[2])
                inter_depart_time = 0
                attris.append(str(inter_depart_time))
                continue
            end_time = float(attris[2])
            inter_depart_time = end_time - end_time_q
            end_time_q = end_time
            attris.append(str(inter_depart_time))
            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

        # Write to the new trace
        count = 0
        for attris in trace_new:
            count += 1
            line = ' '.join(attris)
            output.write(line + '\n')
            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

def main():
    # from_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_lag_time/'
    from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time/'
    # file_name = 'examples_times.csv'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    trace_path = from_direct + file_name

    # to_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_departure/'
    to_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/'
    # file_name = 'UCB-Trace-846890339-848409417_depart.csv'
    generated = to_direct + file_name

    get_departure_trace(trace_path, generated)

if __name__ == '__main__':
    main()