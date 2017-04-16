'''Generate the exponential trace'''
import os
import subprocess as sp
import numpy as np
from datetime import datetime
from datetime import timedelta
from rvgs import Exponential as Expo

def expo_trace(trace_path, generated):
    # MEAN_EXPO = 25.015432078075502
    MEAN_EXPO = 16.750031612867385
    # MEAN_EXPO = 0.1
    # MEAN_EXPO = 16.412899
    with open(trace_path) as trace, \
        open(generated, 'w') as output:
        count = 0
        for line in trace:
            count += 1
            attris = line.split()
            # service_time = Expo(MEAN_EXPO)
            # print('count:', count, service_time)#test
            service_time = np.random.exponential(MEAN_EXPO)
            # Need to change: Service End Time,
            #                 Service Time, and
            #                 Job Delay Time (end time - arril time)
            if count == 1:
                arrival_time = float(attris[0])
                service_start_time = float(attris[1])
                service_end_time = service_start_time + service_time
                delay_time = service_end_time - arrival_time
                attris[2] = str(service_end_time)
                attris[5] = str(service_time)
                attris[6] = str(delay_time)
                new_line = ' '.join(attris)
                output.write(new_line + '\n')
                service_end_time_q = service_end_time

            else:
                arrival_time = float(attris[0])
                # print('arrival_time:', arrival_time, 'service_end_time_q:', service_end_time_q)#test
                if arrival_time < service_end_time_q:
                    service_start_time = service_end_time_q
                    attris[1] = str(service_start_time)
                    # print('@39 count:', count)#test
                else:
                    service_start_time = float(attris[1])
                service_end_time = service_start_time + service_time
                delay_time = service_end_time - arrival_time
                attris[2] = str(service_end_time)
                attris[5] = str(service_time)
                # print('attris[5]:', attris[5])#test
                attris[6] = str(delay_time)
                attris[7] = str(service_end_time - service_end_time_q)
                new_line = ' '.join(attris)
                output.write(new_line + '\n')
                service_end_time_q = service_end_time

            # arrival_time = float(attris[0])
            # service_start_time = float(attris[1])
            # service_end_time = service_start_time + service_time
            # if count == 1:
            #     service_end_time_q = service_end_time
            # lag_time = service_end_time - arrival_time
            # attris[2] = str(service_end_time)
            # attris[5] = str(service_time)
            # attris[6] = str(lag_time)
            # new_line = ' '.join(attris)
            # output.write(new_line + '\n')
            if count % 100000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

def main():
    # from_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_lag_time/'
    # file_name = 'examples_times.csv'

    # from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/'
    from_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/'
    # file_name = 'UCB-Trace-846890339-848409417.csv'
    file_name = 'UCB-Trace.csv'
    trace_path = from_direct + file_name

    # to_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/expo_service_time_depart/'
    to_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/expo_service_time_depart/'
    generated = to_direct + file_name

    expo_trace(trace_path, generated)

if __name__ == '__main__':
    main()
