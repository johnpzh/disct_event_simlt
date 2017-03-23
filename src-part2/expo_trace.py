'''Generate the exponential trace'''
import os
import subprocess as sp
from datetime import datetime
from datetime import timedelta
from rvgs import Exponential as Expo

def expo_trace(trace_path, generated):
    MEAN_EXPO = 16.412899
    with open(trace_path) as trace, \
        open(generated, 'w') as output:
        count = 0
        for line in trace:
            count += 1
            attris = line.split()
            service_time = Expo(MEAN_EXPO)
            # Need to change: Service End Time,
            #                 Service Time, and
            #                 Job Delay Time (end time - arril time)
            arrival_time = float(attris[0])
            service_start_time = float(attris[1])
            service_end_time = service_start_time + service_time
            lag_time = service_end_time - arrival_time
            attris[2] = str(service_end_time)
            attris[5] = str(service_time)
            attris[6] = str(lag_time)
            new_line = ' '.join(attris)
            output.write(new_line + '\n')
            if count % 100000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

def main():
    # from_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_lag_time/'
    # file_name = 'examples_times.csv'

    from_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_lag_time/'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    trace_path = from_direct + file_name

    to_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/expo_service_time/'
    generated = to_direct + file_name

    expo_trace(trace_path, generated)

if __name__ == '__main__':
    main()
