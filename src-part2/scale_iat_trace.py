'''Generate traces with scaled inter-arrival times from original trace'''
import os
import subprocess as sp
import numpy as np
from datetime import datetime
from datetime import timedelta

def scale_iat_trace(trace_path, generated, scale):
    '''Generate new trace which has scaled inter-arrival time
    and other corresponding times'''
    with open(trace_path) as trace, \
        open(generated, 'w') as output:
        trace_new = list()
        count = 0
        for line in trace:
            count += 1
            attris = line.split()
            if count == 1:
                record = ' '.join(attris)
                output.write(record + '\n')
                arrival_time_q = float(attris[0])
                end_time_q = float(attris[2])
                continue
            arrival_time = float(attris[0])
            start_time = float(attris[1])
            end_time = float(attris[2])
            data_len = float(attris[3])
            i_a_time = float(attris[4])
            service_time = float(attris[5])
            job_delay = float(attris[6])

            # Scaled inter-arrival time and modified other times
            i_a_time_p = i_a_time / scale
            arrival_time_p = arrival_time_q + i_a_time_p
            
            # print('@37 arr:', arrival_time_p)#test
            offset = arrival_time_p - arrival_time
            if arrival_time_p < end_time_q:
                start_time_p = end_time_q
            else:
                start_time_p = start_time + offset
            end_time_p = start_time_p + service_time
            # data_len_p = data_len
            # service_time_p = service_time
            job_delay_p = end_time_p - arrival_time_p
            i_d_time_p = end_time_p - end_time_q
            arrival_time_q = arrival_time_p
            end_time_q = end_time_p

            attris_new = ['{0:.6f}'.format(arrival_time_p), \
                          '{0:.6f}'.format(start_time_p), \
                          '{0:.6f}'.format(end_time_p), \
                          str(data_len), \
                          str(i_a_time_p), \
                          str(service_time), \
                          str(job_delay_p), \
                          str(i_d_time_p)]
                          
            # print(attris_new) #test
            result = ' '.join(attris_new)
            output.write(result + '\n')

            if count % 100000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

def main():
    # from_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_departure/'
    # from_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/expo_service_time/'
    # from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/expo_service_time_depart/'
    from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/'
    # file_name = 'examples_times.csv'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    # file_name = 'UCB-Trace-846890339-848409417_depart.csv'
    trace_path = from_direct + file_name

    to_direct = from_direct
    # to_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/scaled_iat_traces/'
    # file_name = 'inter-depart_time_autocor.txt'
    # file_name = 'inter-depart_time_autocor_expo.txt'
    # output_file = to_direct + file_name

    # For original trace
    # scale_min = 0.14813221703 # 0.1/0.6750725939409181
    # scale_max = 1.33318995331 # 0.9/0.6750725939409181

    # For exponential-service-time trace
    scale_min = 0.14775121835 # 0.1/0.676813369903958
    scale_max = 1.32976096516 # 0.9/0.676813369903958
    # 0.1/0.676813369903958
    scales = np.linspace(scale_min, scale_max, 5)
    count = 0
    for scale in scales:
        count += 1
        to_file_name = file_name[:-4] + '_{0:02d}.csv'.format(count)
        generated = to_direct + to_file_name
        scale_iat_trace(trace_path, generated, scale)
        # input()

if __name__ == '__main__':
    main()

