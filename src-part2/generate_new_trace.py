'''Generate the new trace by duplicating'''
import os
import subprocess as sp
import numpy as np
from datetime import datetime
from datetime import timedelta
from numpy.random import normal

def generate_new_trace(trace_path, generated):

    with open(trace_path) as trace, \
        open(generated, 'w') as output:
        count = 0
        for line in trace:
            count += 1
            output.write(line)
            attris = line.split()
            if count == 1:
                arrival_time_start = float(attris[0])
        end_time_end = float(attris[2])
        offset = end_time_end - arrival_time_start

    with open(trace_path) as trace, \
        open(generated, 'a') as output:
        count = 0
        for line in trace:
            count += 1
            attris = line.split()
            arrival_time = float(attris[0]) + offset + normal()
            start_time = float(attris[1]) + offset + normal()
            end_time = float(attris[2]) + offset + normal()
            data_len = float(attris[3]) + normal()
            # i_a_time = float(attris[4])
            # service_time = float(attris[5])
            # job_delay = float(attris[6])
            if count == 1:
                arrival_time_q = arrival_time
                start_time_q = start_time
                end_time_q = end_time

            while start_time < end_time_q:
                start_time = float(attris[1]) + offset + normal()

            i_a_time = arrival_time - arrival_time_q
            service_time = end_time - start_time
            job_delay = end_time - arrival_time
            i_d_time = end_time - end_time_q

            attris_new = [str(arrival_time), \
                            str(start_time), \
                            str(end_time), \
                            str(data_len), \
                            str(i_a_time), \
                            str(service_time), \
                            str(job_delay), \
                            str(i_d_time)]
            line_new = ' '.join(attris_new)
            output.write(line_new + '\n')

def main():
    from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    trace_path = from_direct + file_name

    to_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/duplicated/'
    file_name = 'UCB-duplicated.csv'
    generated = to_direct + file_name

    generate_new_trace(trace_path, generated)



if __name__ == '__main__':
    main()
