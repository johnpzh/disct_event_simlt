'''Extract the trace for a single server'''
import os
import subprocess as sp
import numpy as np
from datetime import datetime
from datetime import timedelta

def extract_trace(trace_path, generated):
    SERVER_NUM = 92
    with open(trace_path) as trace, \
        open(generated, 'w') as output:
        count = 0
        is_first = True
        for line in trace:
            count += 1
            if (count - 1) % SERVER_NUM != 0:
                continue
            attris = line.split()
            arrival_time = float(attris[0])
            end_time = float(attris[2])
            if is_first:
                arrival_time_q = arrival_time
                end_time_q = end_time
                # output.write(line)
                attris.append('0')
                result = ' '.join(attris)
                output.write(result + '\n')
                is_first = False
                continue
            if not (arrival_time > arrival_time_q \
                and end_time > end_time_q):
                continue
            i_a_time = arrival_time - arrival_time_q
            i_d_time = end_time - end_time_q
            # output.write(line)
            arrival_time_q = arrival_time
            end_time_q = end_time
            attris[4] = str(i_a_time)
            attris.append(str(i_d_time))
            result = ' '.join(attris)
            output.write(result + '\n')


            if count % 10 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

def main():
    from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_lag_time/'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    trace_path = from_direct + file_name

    to_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time/'
    # file_name = 'UCB-Trace.csv'
    generated = to_direct + file_name
    extract_trace(trace_path, generated)

if __name__ == '__main__':
    main()